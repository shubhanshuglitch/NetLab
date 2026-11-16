from typing import Dict, Any, Optional
from backend.app.schemas.packets import EventExplanation, LayerType


class ExplanationEngine:
    """
    Deterministic, protocol-grounded explanation generator for every network event.
    """
    @staticmethod
    def explain_event(
        event_type: str,
        layer: LayerType,
        context: Dict[str, Any]
    ) -> EventExplanation:
        
        # 1. ARP Resolution
        if event_type == "ARP_REQUEST":
            target_ip = context.get("target_ip", "destination")
            sender_ip = context.get("sender_ip", "source")
            return EventExplanation(
                what=f"Host broadcasted an ARP request query for IP {target_ip}.",
                why="Network Layer knows the destination IP address, but the Data Link Layer (Ethernet) requires the destination physical MAC address to build an Ethernet frame.",
                protocol="ARP (RFC 826) - Data Link / Network Interface Layer",
                data_changed=f"Frame destination MAC set to FF:FF:FF:FF:FF:FF (broadcast); ARP Table remains pending for {target_ip}.",
                counterfactual=f"If the ARP cache already contained {target_ip}, this broadcast would be bypassed completely and the frame would be unicast directly.",
                real_world="Every time a laptop connects to local Wi-Fi and pings a router or local printer, ARP translates the IP to a 48-bit hardware MAC address."
            )

        if event_type == "ARP_REPLY":
            target_ip = context.get("target_ip", "")
            target_mac = context.get("target_mac", "")
            return EventExplanation(
                what=f"Target host replied with its hardware MAC address {target_mac}.",
                why="The target recognized its own IP in the ARP request and answered with a unicast ARP reply to the sender.",
                protocol="ARP (RFC 826)",
                data_changed=f"ARP Cache updated: mapped {target_ip} -> {target_mac}.",
                counterfactual="If a malicious host spoofed this reply (ARP Poisoning), traffic would be redirected to the attacker.",
                real_world="Operating systems cache this binding in their ARP cache (`arp -a` in Windows/Linux) for typically 2 to 20 minutes."
            )

        # 2. DNS Query / Response
        if event_type == "DNS_QUERY":
            domain = context.get("domain", "hostname")
            return EventExplanation(
                what=f"Client issued DNS resolution query for '{domain}'.",
                why="Humans use domain names (e.g. google.com), but routers forward packets using 32-bit IPv4 or 128-bit IPv6 numerical addresses.",
                protocol="DNS (RFC 1035) - Application Layer over UDP port 53",
                data_changed=f"DNS query message constructed with QNAME={domain}, QTYPE=A (IPv4).",
                counterfactual="If the browser or local OS DNS cache already had this entry, zero DNS packets would traverse the network.",
                real_world="When you hit Enter in your browser, DNS is the very first packet exchange before any TCP handshake or HTTP connection can start."
            )

        if event_type == "DNS_RESPONSE":
            domain = context.get("domain", "")
            resolved_ip = context.get("resolved_ip", "")
            return EventExplanation(
                what=f"DNS resolver returned IP {resolved_ip} for '{domain}'.",
                why="The authoritative nameserver answered with an A record mapping domain to IP.",
                protocol="DNS (RFC 1035)",
                data_changed=f"Local DNS Cache updated: {domain} -> {resolved_ip} with TTL=300s.",
                counterfactual="If DNS resolution fails (NXDOMAIN or timeout), browser immediately throws ERR_NAME_NOT_RESOLVED.",
                real_world="Global CDNs (Cloudflare, Akamai) return different IPs based on the client's geographical location using GeoDNS."
            )

        # 3. TCP Handshake & Flags
        if event_type == "TCP_SYN":
            seq = context.get("seq", 1000)
            return EventExplanation(
                what=f"Client transmitted TCP SYN packet (Initial Sequence Number: {seq}).",
                why="TCP is a connection-oriented, reliable protocol. Both endpoints must agree on sequence numbering and buffer capacities before sending data.",
                protocol="TCP (RFC 793) - Transport Layer",
                data_changed=f"TCP State: CLOSED -> SYN_SENT. Client ISN={seq}, Flags=[SYN], Window=65535.",
                counterfactual="If UDP were used instead of TCP, no handshake or connection state would exist; data would transmit immediately with zero overhead but no delivery guarantee.",
                real_world="Every HTTP/1.1 or HTTPS request, SSH session, and database connection begins with this exact SYN packet."
            )

        if event_type == "TCP_SYN_ACK":
            seq = context.get("seq", 5000)
            ack = context.get("ack", 1001)
            return EventExplanation(
                what=f"Server replied with TCP SYN-ACK (Seq={seq}, Ack={ack}).",
                why="Server acknowledges client's SYN (Ack = Client_Seq + 1) and advertises its own Initial Sequence Number (ISN={seq}).",
                protocol="TCP (RFC 793)",
                data_changed=f"Server TCP State: LISTEN -> SYN_RECEIVED. Flags=[SYN, ACK].",
                counterfactual="If the server port was closed or blocked by firewall, server would reply with TCP RST (Reset) or drop the packet entirely (SYN stealth timeout).",
                real_world="Firewalls inspect this state; stateful firewalls track embryonic connections to prevent SYN flood attacks."
            )

        if event_type == "TCP_ACK":
            ack = context.get("ack", 5001)
            return EventExplanation(
                what=f"Client sent TCP ACK ({ack}) completing the 3-Way Handshake.",
                why="Connection is now fully synchronized and duplex communication is unlocked.",
                protocol="TCP (RFC 793)",
                data_changed="Both client and server state: ESTABLISHED. Sockets ready for application payload transfer.",
                counterfactual="Until this ACK arrives, server retains connection in half-open SYN queue.",
                real_world="Total time to reach this state represents one Round Trip Time (1 RTT) connection latency."
            )

        # 4. NAT / PAT Translation
        if event_type == "NAT_TRANSLATE_OUTBOUND":
            priv_ip = context.get("priv_ip")
            priv_port = context.get("priv_port")
            pub_ip = context.get("pub_ip")
            pub_port = context.get("pub_port")
            return EventExplanation(
                what=f"Router translated private socket {priv_ip}:{priv_port} to public socket {pub_ip}:{pub_port}.",
                why="RFC 1918 private IPv4 addresses (192.168.x.x, 10.x.x.x) are non-routable on the public internet. The NAT router multiplexes multiple local devices onto a single public IP using ephemeral port numbers.",
                protocol="NAPT / PAT (RFC 3022) - Network Layer",
                data_changed=f"NAT Table entry created: [{priv_ip}:{priv_port} <-> {pub_ip}:{pub_port}]. IP header source rewritten.",
                counterfactual="Without NAT or IPv6, every home device would require a globally unique public IPv4 address, which were exhausted in 2011.",
                real_world="This is how 20 devices on your home Wi-Fi or two browser tabs playing YouTube simultaneously share one ISP connection without conflict."
            )

        # 5. IPv4 Fragmentation
        if event_type == "IP_FRAGMENTATION":
            packet_len = context.get("packet_len", 1500)
            mtu = context.get("mtu", 1000)
            frags = context.get("frags", 2)
            return EventExplanation(
                what=f"Router split {packet_len}-byte packet into {frags} fragments due to link MTU of {mtu} bytes.",
                why=f"The outgoing link physical medium has a Maximum Transmission Unit (MTU) of {mtu} bytes. IPv4 header total length exceeded this capacity with DF (Don't Fragment) = 0.",
                protocol="IPv4 (RFC 791) - Network Layer",
                data_changed=f"Packet sliced into {frags} fragments with matching Identification, calculated Fragment Offsets (in 8-byte units), and MF (More Fragments) flags.",
                counterfactual="If DF=1 (Don't Fragment) was set, router would drop the packet and return ICMP Type 3 Code 4 (Fragmentation Needed and DF set), enabling Path MTU Discovery (PMTUD).",
                real_world="VPN tunnels (IPsec, WireGuard) add encapsulation headers that reduce effective MTU, frequently triggering fragmentation if MSS clamping is not configured."
            )

        # 6. Packet Dropped / Loss
        if event_type == "PACKET_DROPPED":
            reason = context.get("reason", "link packet loss")
            seq = context.get("seq", 0)
            return EventExplanation(
                what=f"Packet (Seq={seq}) dropped in transit due to {reason}.",
                why="Physical medium noise, router queue buffer overflow (congestive tail drop), or simulated link loss rate caused the frame to be discarded.",
                protocol="Physical / Data Link / Network Layer",
                data_changed="Packet removed from channel buffer; receiver receives nothing; sender timer continues counting.",
                counterfactual="In UDP, dropped packets are gone forever (causing audio glitches or video frame artifacts). In TCP, the sender timeout or duplicate ACKs will trigger retransmission.",
                real_world="Bufferbloat in residential Wi-Fi routers frequently drops packets when large uploads saturate uplink queues."
            )

        # 7. TCP Retransmission / Timeout
        if event_type == "TCP_RETRANSMISSION":
            seq = context.get("seq", 0)
            cwnd = context.get("cwnd", 1.0)
            ssthresh = context.get("ssthresh", 16.0)
            return EventExplanation(
                what=f"TCP Retransmission Timeout (RTO) expired! Resending packet Seq={seq}.",
                why="The sender did not receive an ACK for this packet before the RTO timer elapsed, concluding that either the packet or its ACK was lost in the network.",
                protocol="TCP Tahoe/Reno Congestion Control (RFC 5681)",
                data_changed=f"CWND collapsed to 1 MSS (was {cwnd}); ssthresh halved to {ssthresh} MSS; slow-start re-entered.",
                counterfactual="If 3 Duplicate ACKs were received instead of timer expiration, Fast Retransmit would trigger without waiting for the full RTO timer, recovering much faster.",
                real_world="When your web browser stutters on a train or weak cellular connection, TCP RTO timeouts and cwnd collapsing are the direct cause."
            )

        # 8. CRC Corruption Detected
        if event_type == "CRC_ERROR":
            return EventExplanation(
                what="Receiver rejected Ethernet frame due to CRC-32 Frame Check Sequence (FCS) mismatch.",
                why="One or more bits were corrupted or flipped by electromagnetic interference or channel noise during physical medium propagation.",
                protocol="IEEE 802.3 Ethernet CRC-32 - Data Link Layer",
                data_changed="Frame discarded silently at the Network Interface Card (NIC); frame status marked CORRUPTED.",
                counterfactual="If CRC was disabled, the corrupt bit would pass up to the application, potentially corrupting files, executing rogue instructions, or crashing programs.",
                real_world="Ethernet NICs discard millions of corrupt frames in noisy enterprise environments without the OS kernel or CPU ever noticing."
            )

        # Default fallback
        return EventExplanation(
            what=f"Event {event_type} occurred at {layer.value} layer.",
            why=context.get("reason", "Standard protocol processing transition."),
            protocol=context.get("protocol", "Standard Networking Protocol"),
            data_changed=context.get("data_changed", "State updated."),
            counterfactual="Alternative protocol settings would alter timing or sequence of events.",
            real_world="Standard networking behavior observed in real-world packet captures."
        )

