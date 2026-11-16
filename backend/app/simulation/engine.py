import random
import uuid
from typing import Dict, Any, List, Optional, Tuple
import networkx as nx

from backend.app.schemas.packets import (
    LayerType, PacketModel, SimulationEventModel, EventExplanation,
    ApplicationHeader, TransportHeader, NetworkHeader, DataLinkHeader,
    TCPFlags, AppProtocol, TransportProtocol
)
from backend.app.schemas.topology import TopologyConfig, DeviceConfig, LinkConfig
from backend.app.schemas.simulations import SimulationRequest, SimulationResponse, SimulationStats
from backend.app.simulation.state import SimulationState
from backend.app.explanations.engine import ExplanationEngine
from backend.app.protocols.network.ip import create_ipv4_header
from backend.app.protocols.network.fragmentation import fragment_ipv4_packet
from backend.app.protocols.datalink.framing import create_ethernet_frame
from backend.app.protocols.datalink.crc import compute_crc32, inject_bit_error
from backend.app.protocols.transport.tcp import TCPConnection
from backend.app.protocols.transport.udp import create_udp_header
from backend.app.protocols.application.http import create_http_request, create_http_response
from backend.app.protocols.application.dns import DNSResolver, create_dns_query_packet, create_dns_response_packet
from backend.app.protocols.network.nat import NATRouter


class SimulationEngine:
    """
    Independent event-driven network simulation engine.
    Executes actual protocol logic across all 5 layers.
    """
    def __init__(self, topology: TopologyConfig, random_seed: int = 42):
        self.state = SimulationState(topology)
        self.random = random.Random(random_seed)
        self.dns_resolver = DNSResolver()
        self.graph = nx.Graph()
        self._build_graph()

    def _build_graph(self):
        self.graph.clear()
        for d in self.state.topology.devices:
            self.graph.add_node(d.id, data=d)
        for l in self.state.topology.links:
            if l.is_active:
                self.graph.add_edge(l.source_id, l.target_id, id=l.id, config=l, weight=l.latency_ms)

    def find_path(self, src_id: str, dst_id: str) -> List[str]:
        """Calculates shortest path through topology graph."""
        try:
            return nx.shortest_path(self.graph, source=src_id, target=dst_id, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def get_link_between(self, node_a: str, node_b: str) -> Optional[LinkConfig]:
        if self.graph.has_edge(node_a, node_b):
            edge_data = self.graph.get_edge_data(node_a, node_b)
            return edge_data.get("config")
        return None

    def execute_simulation(self, req: SimulationRequest) -> SimulationResponse:
        """
        Executes complete end-to-end multi-layer network simulation deterministically.
        """
        src_dev = self.state.devices.get(req.sender_id)
        dst_dev = self.state.devices.get(req.receiver_id)

        if not src_dev or not dst_dev:
            raise ValueError(f"Sender {req.sender_id} or Receiver {req.receiver_id} not found in topology")

        path = self.find_path(req.sender_id, req.receiver_id)
        if not path or len(path) < 2:
            raise ValueError(f"No active network route between {req.sender_id} and {req.receiver_id}")

        self.state.events.clear()
        self.state.packets.clear()
        self.state.stats = SimulationStats()
        self.state.current_time_ms = 0.0

        src_ip = src_dev.interfaces[0].ip_address if src_dev.interfaces else "192.168.1.10"
        src_mac = src_dev.interfaces[0].mac_address if src_dev.interfaces else "00:AA:BB:CC:DD:01"
        dst_ip = dst_dev.interfaces[0].ip_address if dst_dev.interfaces else "142.250.190.46"
        dst_mac = dst_dev.interfaces[0].mac_address if dst_dev.interfaces else "00:AA:BB:CC:DD:02"

        src_port = 54321
        dst_port = 80 if req.app_protocol == AppProtocol.HTTP else (53 if req.app_protocol == AppProtocol.DNS else 8080)

        # Step 0: Check ARP resolution for first hop
        first_hop = path[1]
        first_hop_dev = self.state.devices.get(first_hop)
        next_hop_mac = first_hop_dev.interfaces[0].mac_address if first_hop_dev and first_hop_dev.interfaces else "00:AA:BB:CC:DD:FF"

        if src_ip not in src_dev.arp_cache and len(path) > 1:
            # Emit ARP Request
            self.state.current_time_ms += 1.0
            arp_req_exp = ExplanationEngine.explain_event("ARP_REQUEST", LayerType.DATALINK, {
                "target_ip": first_hop_dev.interfaces[0].ip_address if first_hop_dev and first_hop_dev.interfaces else "Gateway",
                "sender_ip": src_ip
            })
            self.state.events.append(SimulationEventModel(
                event_id=str(uuid.uuid4())[:8],
                timestamp_ms=self.state.current_time_ms,
                event_type="ARP_REQUEST",
                source_node=req.sender_id,
                destination_node=first_hop,
                layer=LayerType.DATALINK,
                details={"target_ip": first_hop_dev.interfaces[0].ip_address if first_hop_dev and first_hop_dev.interfaces else "Gateway", "sender_ip": src_ip},
                explanation=arp_req_exp
            ))

            # Emit ARP Reply
            self.state.current_time_ms += 2.0
            arp_rep_exp = ExplanationEngine.explain_event("ARP_REPLY", LayerType.DATALINK, {
                "target_ip": first_hop_dev.interfaces[0].ip_address if first_hop_dev and first_hop_dev.interfaces else "Gateway",
                "target_mac": next_hop_mac
            })
            self.state.events.append(SimulationEventModel(
                event_id=str(uuid.uuid4())[:8],
                timestamp_ms=self.state.current_time_ms,
                event_type="ARP_REPLY",
                source_node=first_hop,
                destination_node=req.sender_id,
                layer=LayerType.DATALINK,
                details={"learned_mac": next_hop_mac},
                explanation=arp_rep_exp
            ))
            src_dev.arp_cache[first_hop_dev.interfaces[0].ip_address if first_hop_dev and first_hop_dev.interfaces else "Gateway"] = next_hop_mac

        # Step 1: If TCP, perform 3-Way Handshake
        tcp_conn = None
        handshake_start_time = self.state.current_time_ms
        if req.transport_protocol == TransportProtocol.TCP:
            tcp_conn = TCPConnection(
                src_ip=src_ip,
                src_port=src_port,
                dst_ip=dst_ip,
                dst_port=dst_port,
                initial_seq=1000,
                algorithm=req.tcp_algorithm
            )
            # SYN
            self.state.current_time_ms += 5.0
            syn_hdr = tcp_conn.create_syn_packet()
            syn_pkt = self._create_packet(
                src_node=req.sender_id,
                dst_node=path[1],
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_mac=src_mac,
                dst_mac=next_hop_mac,
                app_hdr=None,
                trans_hdr=syn_hdr,
                payload_str=""
            )
            self._record_hop_event(
                event_type="TCP_SYN",
                layer=LayerType.TRANSPORT,
                node=req.sender_id,
                target_node=req.receiver_id,
                packet=syn_pkt,
                ctx={"seq": 1000}
            )

            # SYN-ACK
            self.state.current_time_ms += 15.0
            syn_ack_hdr = tcp_conn.receive_syn_ack(peer_seq=5000, ack_num=1001)
            syn_ack_pkt = self._create_packet(
                src_node=req.receiver_id,
                dst_node=req.sender_id,
                src_ip=dst_ip,
                dst_ip=src_ip,
                src_mac=next_hop_mac,
                dst_mac=src_mac,
                app_hdr=None,
                trans_hdr=syn_ack_hdr,
                payload_str=""
            )
            self._record_hop_event(
                event_type="TCP_SYN_ACK",
                layer=LayerType.TRANSPORT,
                node=req.receiver_id,
                target_node=req.sender_id,
                packet=syn_ack_pkt,
                ctx={"seq": 5000, "ack": 1001}
            )

            # ACK
            self.state.current_time_ms += 10.0
            ack_hdr = TransportHeader(
                protocol="TCP",
                src_port=src_port,
                dst_port=dst_port,
                seq_num=1001,
                ack_num=5001,
                flags=TCPFlags(ack=True)
            )
            ack_pkt = self._create_packet(
                src_node=req.sender_id,
                dst_node=req.receiver_id,
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_mac=src_mac,
                dst_mac=next_hop_mac,
                app_hdr=None,
                trans_hdr=ack_hdr,
                payload_str=""
            )
            self._record_hop_event(
                event_type="TCP_ACK",
                layer=LayerType.TRANSPORT,
                node=req.sender_id,
                target_node=req.receiver_id,
                packet=ack_pkt,
                ctx={"ack": 5001}
            )
            self.state.stats.connection_establishment_time_ms = round(self.state.current_time_ms - handshake_start_time, 2)

        # Step 2: Application Payload creation
        if req.app_protocol == AppProtocol.HTTP:
            app_header = create_http_request(method="GET", url="/video?v=dQw4w9WgXcQ", host="youtube.com")
        elif req.app_protocol == AppProtocol.DNS:
            app_header = create_dns_query_packet(domain="youtube.com")
        else:
            app_header = ApplicationHeader(protocol=req.app_protocol.value, payload=req.payload)

        # Transport header for data
        payload_bytes = req.payload.encode("utf-8")
        if req.transport_protocol == TransportProtocol.TCP and tcp_conn:
            trans_header = tcp_conn.create_data_packet(len(payload_bytes))
        else:
            trans_header = create_udp_header(src_port, dst_port, len(payload_bytes))

        # Check MTU across path
        effective_mtu = req.override_mtu if req.override_mtu else 1500
        for i in range(len(path) - 1):
            link = self.get_link_between(path[i], path[i+1])
            if link and link.mtu_bytes < effective_mtu:
                effective_mtu = link.mtu_bytes

        # Fragmentation check
        fragments, frag_err = fragment_ipv4_packet(
            src_ip=src_ip,
            dst_ip=dst_ip,
            payload=payload_bytes,
            mtu=effective_mtu,
            identification=2048,
            protocol=req.transport_protocol.value
        )
        self.state.stats.fragment_count = len(fragments)

        if len(fragments) > 1:
            self.state.current_time_ms += 2.0
            frag_exp = ExplanationEngine.explain_event("IP_FRAGMENTATION", LayerType.NETWORK, {
                "packet_len": 20 + len(payload_bytes),
                "mtu": effective_mtu,
                "frags": len(fragments)
            })
            self.state.events.append(SimulationEventModel(
                event_id=str(uuid.uuid4())[:8],
                timestamp_ms=self.state.current_time_ms,
                event_type="IP_FRAGMENTATION",
                source_node=req.sender_id,
                layer=LayerType.NETWORK,
                details={"fragment_count": len(fragments), "effective_mtu": effective_mtu},
                explanation=frag_exp
            ))

        # Step 3: Multi-hop packet transmission
        for frag in fragments:
            frag_pkt = self._create_packet(
                src_node=req.sender_id,
                dst_node=path[1],
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_mac=src_mac,
                dst_mac=next_hop_mac,
                app_hdr=app_header,
                trans_hdr=trans_header,
                net_hdr=frag["header"],
                payload_str=frag["payload"].decode("utf-8", errors="replace")
            )
            self._transmit_along_path(path, frag_pkt, req, tcp_conn)

        # Calculate final stats
        self._calculate_final_stats(tcp_conn)

        return SimulationResponse(
            simulation_id=str(uuid.uuid4()),
            status="COMPLETED",
            current_step=len(self.state.events),
            total_steps=len(self.state.events),
            events=self.state.events,
            packets=self.state.packets,
            stats=self.state.stats,
            topology=self.state.topology
        )

    def _transmit_along_path(
        self,
        path: List[str],
        packet: PacketModel,
        req: SimulationRequest,
        tcp_conn: Optional[TCPConnection]
    ):
        """Transmits packet hop by hop through path with loss, corruption, and NAT modeling."""
        self.state.stats.packets_transmitted += 1

        for i in range(len(path) - 1):
            curr_node = path[i]
            next_node = path[i + 1]
            curr_dev = self.state.devices.get(curr_node)
            next_dev = self.state.devices.get(next_node)
            link = self.get_link_between(curr_node, next_node)

            link_latency = link.latency_ms if link else 10.0
            link_loss = req.override_loss_rate if req.override_loss_rate is not None else (link.loss_rate if link else 0.0)
            link_ber = req.override_bit_error_rate if req.override_bit_error_rate is not None else (link.bit_error_rate if link else 0.0)

            self.state.current_time_ms += link_latency

            # Check NAT translation at router
            if curr_dev and curr_dev.nat_enabled:
                old_ip = packet.network_header.src_ip
                old_port = packet.transport_header.src_port if packet.transport_header else 50000
                pub_ip = curr_dev.interfaces[1].ip_address if len(curr_dev.interfaces) > 1 else "203.0.113.1"
                pub_port = 61001
                packet.network_header.src_ip = pub_ip
                if packet.transport_header:
                    packet.transport_header.src_port = pub_port

                nat_exp = ExplanationEngine.explain_event("NAT_TRANSLATE_OUTBOUND", LayerType.NETWORK, {
                    "priv_ip": old_ip,
                    "priv_port": old_port,
                    "pub_ip": pub_ip,
                    "pub_port": pub_port
                })
                self.state.events.append(SimulationEventModel(
                    event_id=str(uuid.uuid4())[:8],
                    timestamp_ms=self.state.current_time_ms,
                    event_type="NAT_TRANSLATE_OUTBOUND",
                    source_node=curr_node,
                    destination_node=next_node,
                    packet_id=packet.id,
                    layer=LayerType.NETWORK,
                    details={"internal": f"{old_ip}:{old_port}", "external": f"{pub_ip}:{pub_port}"},
                    explanation=nat_exp,
                    packet_snapshot=packet.model_copy()
                ))

            # Packet loss injection check
            if self.random.random() < link_loss:
                self.state.stats.packets_lost += 1
                packet.status = "DROPPED"
                drop_exp = ExplanationEngine.explain_event("PACKET_DROPPED", LayerType.DATALINK, {
                    "reason": f"link loss probability ({link_loss * 100:.1f}%) on link {curr_node}->{next_node}",
                    "seq": packet.transport_header.seq_num if packet.transport_header else 0
                })
                self.state.events.append(SimulationEventModel(
                    event_id=str(uuid.uuid4())[:8],
                    timestamp_ms=self.state.current_time_ms,
                    event_type="PACKET_DROPPED",
                    source_node=curr_node,
                    destination_node=next_node,
                    packet_id=packet.id,
                    layer=LayerType.DATALINK,
                    details={"link": f"{curr_node}->{next_node}", "reason": "Loss simulated"},
                    explanation=drop_exp,
                    packet_snapshot=packet.model_copy()
                ))

                # If TCP, handle Retransmission
                if tcp_conn:
                    self.state.current_time_ms += 100.0  # RTO timer
                    tcp_conn.on_timeout()
                    self.state.stats.retransmissions += 1
                    retrans_exp = ExplanationEngine.explain_event("TCP_RETRANSMISSION", LayerType.TRANSPORT, {
                        "seq": packet.transport_header.seq_num if packet.transport_header else 0,
                        "cwnd": tcp_conn.cwnd,
                        "ssthresh": tcp_conn.ssthresh
                    })
                    self.state.events.append(SimulationEventModel(
                        event_id=str(uuid.uuid4())[:8],
                        timestamp_ms=self.state.current_time_ms,
                        event_type="TCP_RETRANSMISSION",
                        source_node=path[0],
                        destination_node=next_node,
                        packet_id=packet.id,
                        layer=LayerType.TRANSPORT,
                        details={"retransmitted_seq": packet.transport_header.seq_num if packet.transport_header else 0},
                        explanation=retrans_exp,
                        packet_snapshot=packet.model_copy()
                    ))
                return

            # Bit error corruption injection check
            if self.random.random() < link_ber:
                self.state.stats.frames_corrupted += 1
                packet.datalink_header.is_corrupted = True
                packet.datalink_header.frame_status = "CORRUPTED"
                crc_err_exp = ExplanationEngine.explain_event("CRC_ERROR", LayerType.DATALINK, {})
                self.state.events.append(SimulationEventModel(
                    event_id=str(uuid.uuid4())[:8],
                    timestamp_ms=self.state.current_time_ms,
                    event_type="CRC_ERROR",
                    source_node=curr_node,
                    destination_node=next_node,
                    packet_id=packet.id,
                    layer=LayerType.DATALINK,
                    details={"corrupted_bits": 1},
                    explanation=crc_err_exp,
                    packet_snapshot=packet.model_copy()
                ))
                return

            # Normal Hop Forwarding
            packet.current_node = next_node
            hop_exp = EventExplanation(
                what=f"Frame forwarded from {curr_node} to {next_node} via {link.medium.value if link else 'Ethernet'}.",
                why=f"Router {curr_node} performed routing table lookup and forwarded to next-hop interface for destination {packet.network_header.dst_ip}.",
                protocol="IPv4 Forwarding / Ethernet Switching",
                data_changed=f"Hop count incremented; TTL decremented to {packet.network_header.ttl - 1}.",
                counterfactual="If routing table lacked next-hop route, packet would be dropped with ICMP Destination Net Unreachable.",
                real_world="Core internet routers (BGP/OSPF) forward millions of packets per second using hardware ASICs."
            )
            packet.network_header.ttl -= 1
            self.state.events.append(SimulationEventModel(
                event_id=str(uuid.uuid4())[:8],
                timestamp_ms=self.state.current_time_ms,
                event_type="HOP_FORWARD",
                source_node=curr_node,
                destination_node=next_node,
                packet_id=packet.id,
                layer=LayerType.NETWORK,
                details={"ttl_remaining": packet.network_header.ttl, "hop": f"{curr_node}->{next_node}"},
                explanation=hop_exp,
                packet_snapshot=packet.model_copy()
            ))

        # Destination Delivery
        packet.status = "DELIVERED"
        self.state.stats.packets_received += 1
        if tcp_conn:
            tcp_conn.on_ack_received(ack_num=packet.transport_header.seq_num + len(packet.raw_payload))

        deliv_exp = EventExplanation(
            what=f"Packet delivered to final destination {path[-1]}.",
            why="Network layer verified destination IP matches local host interface and decapsulated payload to transport socket.",
            protocol="Application & Transport Layer Decapsulation",
            data_changed="Message delivered to application receive socket buffer.",
            counterfactual="If destination port was not listening, an ICMP Port Unreachable or TCP RST would be emitted.",
            real_world="The operating system kernel delivers the packet payload to the web server process (nginx, node, python)."
        )
        self.state.events.append(SimulationEventModel(
            event_id=str(uuid.uuid4())[:8],
            timestamp_ms=self.state.current_time_ms,
            event_type="PACKET_DELIVERED",
            source_node=path[-2],
            destination_node=path[-1],
            packet_id=packet.id,
            layer=LayerType.APPLICATION,
            details={"delivered_to": path[-1]},
            explanation=deliv_exp,
            packet_snapshot=packet.model_copy()
        ))

    def _create_packet(
        self,
        src_node: str,
        dst_node: str,
        src_ip: str,
        dst_ip: str,
        src_mac: str,
        dst_mac: str,
        app_hdr: Optional[ApplicationHeader],
        trans_hdr: Optional[TransportHeader],
        net_hdr: Optional[NetworkHeader] = None,
        payload_str: str = ""
    ) -> PacketModel:
        payload_bytes = payload_str.encode("utf-8")
        data_len = len(payload_bytes)

        if not net_hdr:
            proto = trans_hdr.protocol if trans_hdr else "TCP"
            net_hdr = create_ipv4_header(
                src_ip=src_ip,
                dst_ip=dst_ip,
                total_length=20 + 20 + data_len,
                protocol=proto
            )

        dl_hdr, _ = create_ethernet_frame(
            src_mac=src_mac,
            dst_mac=dst_mac,
            payload_bytes=payload_bytes
        )

        pkt = PacketModel(
            id=str(uuid.uuid4())[:8],
            size_bytes=14 + net_hdr.total_length + 4,  # Ethernet + IP + CRC
            app_header=app_hdr,
            transport_header=trans_hdr,
            network_header=net_hdr,
            datalink_header=dl_hdr,
            raw_payload=payload_str,
            status="IN_TRANSIT",
            current_node=src_node,
            next_node=dst_node,
            creation_time=self.state.current_time_ms
        )
        self.state.packets.append(pkt)
        return pkt

    def _record_hop_event(
        self,
        event_type: str,
        layer: LayerType,
        node: str,
        target_node: str,
        packet: PacketModel,
        ctx: Dict[str, Any]
    ):
        explanation = ExplanationEngine.explain_event(event_type, layer, ctx)
        self.state.events.append(SimulationEventModel(
            event_id=str(uuid.uuid4())[:8],
            timestamp_ms=self.state.current_time_ms,
            event_type=event_type,
            source_node=node,
            destination_node=target_node,
            packet_id=packet.id,
            layer=layer,
            details=ctx,
            explanation=explanation,
            packet_snapshot=packet.model_copy()
        ))

    def _calculate_final_stats(self, tcp_conn: Optional[TCPConnection]):
        if self.state.stats.packets_transmitted > 0:
            self.state.stats.packet_delivery_ratio = round(
                (self.state.stats.packets_received / self.state.stats.packets_transmitted) * 100.0, 1
            )
        self.state.stats.average_latency_ms = round(self.state.current_time_ms, 2)
        if self.state.current_time_ms > 0:
            total_bits = sum(p.size_bytes * 8 for p in self.state.packets if p.status == "DELIVERED")
            self.state.stats.throughput_kbps = round(total_bits / self.state.current_time_ms, 2)

        if tcp_conn:
            self.state.stats.tcp_cwnd_history = tcp_conn.cwnd_history
