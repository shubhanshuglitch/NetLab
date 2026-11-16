from typing import Dict, Any, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.protocols.datalink.crc import crc_bitwise_division, compute_crc32
from backend.app.protocols.datalink.arq import simulate_stop_and_wait, simulate_go_back_n, simulate_selective_repeat
from backend.app.protocols.network.routing import calculate_dijkstra, calculate_distance_vector
from backend.app.protocols.network.fragmentation import fragment_ipv4_packet
from backend.app.protocols.application.dns import DNSResolver
from backend.app.protocols.application.dhcp import DHCPServer

router = APIRouter(prefix="/concepts", tags=["Concepts"])

# Models for concept visualizer interactive execution
class CRCCalculateRequest(BaseModel):
    data_bits: str = "1101011011"
    generator_bits: str = "10011"

class ARQSimulateRequest(BaseModel):
    protocol: str = "Go-Back-N"  # "Stop-and-Wait", "Go-Back-N", "Selective-Repeat"
    total_frames: int = 8
    window_size: int = 4
    drop_frame_index: Optional[int] = 2

class DijkstraRequest(BaseModel):
    nodes: List[str] = ["R1", "R2", "R3", "R4", "R5"]
    links: List[Dict[str, Any]] = [
        {"source": "R1", "target": "R2", "cost": 3},
        {"source": "R1", "target": "R3", "cost": 5},
        {"source": "R2", "target": "R3", "cost": 1},
        {"source": "R2", "target": "R4", "cost": 7},
        {"source": "R3", "target": "R4", "cost": 2},
        {"source": "R4", "target": "R5", "cost": 4},
        {"source": "R3", "target": "R5", "cost": 8}
    ]
    source: str = "R1"

class FragmentationRequest(BaseModel):
    payload_size_bytes: int = 2400
    mtu: int = 1000
    flags_df: bool = False

class DNSResolveRequest(BaseModel):
    domain: str = "youtube.com"

class DHCPSimulateRequest(BaseModel):
    client_mac: str = "00:AA:22:33:44:55"


# Concept library metadata for all 5 layers
CONCEPTS_CATALOG = [
    {
        "id": "concept-crc",
        "name": "Cyclic Redundancy Check (CRC)",
        "layer": "Data Link Layer",
        "difficulty": "Intermediate",
        "summary": "Mathematical polynomial modulo-2 division used in Ethernet FCS and Wi-Fi to detect bit corruption.",
        "simple_explanation": "Imagine calculating a checksum remainder using long division, but with XOR instead of subtraction. If any bit changes on the wire, the remainder changes and the frame is rejected.",
        "technical_explanation": "CRC treats binary strings as polynomial coefficients over GF(2). Sender appends zeros, divides by generator polynomial G(x), and transmits remainder. Receiver re-divides: non-zero remainder proves transmission error.",
        "common_mistakes": "Assuming CRC can correct corrupted bits (it only detects them; Hamming codes or FEC are required for error correction).",
        "real_world_application": "Every Ethernet frame ending FCS (Frame Check Sequence) is a 32-bit CRC (IEEE 802.3).",
        "interactive_type": "crc"
    },
    {
        "id": "concept-arq",
        "name": "ARQ Protocols (Stop-and-Wait, Go-Back-N, Selective Repeat)",
        "layer": "Data Link Layer",
        "difficulty": "Intermediate",
        "summary": "Automatic Repeat reQuest sliding-window mechanisms for flow and error control over unreliable links.",
        "simple_explanation": "How to ensure all letters arrive: wait for reply after every letter (Stop-and-Wait), send 4 letters and resend all if one is lost (Go-Back-N), or resend only the missing letter (Selective Repeat).",
        "technical_explanation": "Go-Back-N uses cumulative ACKs and discards out-of-order frames, causing retransmission of the entire window upon timeout. Selective Repeat uses individual ACKs and receiver buffering to retransmit only unacknowledged frames.",
        "common_mistakes": "Confusing Go-Back-N with Selective Repeat receiver window sizes (GBN receiver window is always 1; Selective Repeat receiver window equals sender window).",
        "real_world_application": "High-latency satellite links and cellular channels implement Selective Repeat variants to prevent wasting bandwidth.",
        "interactive_type": "arq"
    },
    {
        "id": "concept-dijkstra",
        "name": "Dijkstra Link-State Routing",
        "layer": "Network Layer",
        "difficulty": "Intermediate",
        "summary": "Shortest-path algorithm used in OSPF (Open Shortest Path First) and IS-IS interior gateway protocols.",
        "simple_explanation": "Finds the fastest route from a starting router to every other router in the network, step by step.",
        "technical_explanation": "Maintains a set of visited nodes and tentative distances. In each iteration, greedily selects unvisited node with minimal metric, relaxes its neighbor edges, and updates routing table next-hops.",
        "common_mistakes": "Believing Dijkstra works with negative edge weights (requires Bellman-Ford instead).",
        "real_world_application": "Enterprise corporate networks and cloud data centers run OSPF to route traffic between server racks.",
        "interactive_type": "dijkstra"
    },
    {
        "id": "concept-fragmentation",
        "name": "IPv4 MTU & Packet Fragmentation",
        "layer": "Network Layer",
        "difficulty": "Advanced",
        "summary": "How routers slice oversized IP datagrams across links with smaller Maximum Transmission Units (MTU).",
        "simple_explanation": "When a large parcel is too big for a doorway, the postal service breaks it into smaller boxes with label numbers so you can put it back together at home.",
        "technical_explanation": "Payload is sliced into multiples of 8 bytes. Intermediate fragments have MF=1 and calculated fragment offset. Reassembly occurs solely at the destination host.",
        "common_mistakes": "Forgetting that Fragment Offset is measured in 8-byte units, not 1-byte units.",
        "real_world_application": "VPN tunnels (IPsec/WireGuard/GRE) encapsulate packets and reduce effective MTU from standard 1500 to 1420 bytes.",
        "interactive_type": "fragmentation"
    },
    {
        "id": "concept-dns",
        "name": "Hierarchical DNS Resolution",
        "layer": "Application Layer",
        "difficulty": "Beginner",
        "summary": "Recursive query walkthrough from local cache to Root (.), TLD (.com), and Authoritative nameservers.",
        "simple_explanation": "The internet's phonebook that translates human names like google.com into numerical IP addresses.",
        "technical_explanation": "Client queries local recursive resolver (port 53 UDP). If not cached, resolver queries Root Hints -> TLD servers -> Authoritative NS, caches result for TTL duration, and returns A record.",
        "common_mistakes": "Thinking DNS always talks to root servers for every query (99% of queries are served directly from recursive cache).",
        "real_world_application": "Public resolvers (8.8.8.8, 1.1.1.1) and internal corporate split-horizon DNS.",
        "interactive_type": "dns"
    },
    {
        "id": "concept-dhcp",
        "name": "DHCP Dynamic IP Configuration (DORA)",
        "layer": "Application / Network Layer",
        "difficulty": "Beginner",
        "summary": "Discover, Offer, Request, ACK four-way handshake for plug-and-play network provisioning.",
        "simple_explanation": "When your phone connects to Wi-Fi, it asks 'Can someone give me an IP address?' and the router responds with your IP, gateway, and DNS settings.",
        "technical_explanation": "Client broadcasts DHCP Discover (UDP 67/68). Server offers IP and options. Client requests IP. Server ACKs lease into its binding table.",
        "common_mistakes": "Assuming DHCP is a layer 2 protocol (it runs over UDP/IP, but uses broadcast MAC/IP before address assignment).",
        "real_world_application": "Every home router, coffee shop Wi-Fi, and cloud VPC instance uses DHCP.",
        "interactive_type": "dhcp"
    }
]

@router.get("")
def list_concepts():
    return CONCEPTS_CATALOG

@router.post("/crc/calculate")
def api_calculate_crc(req: CRCCalculateRequest):
    return crc_bitwise_division(req.data_bits, req.generator_bits)

@router.post("/arq/simulate")
def api_simulate_arq(req: ARQSimulateRequest):
    if req.protocol == "Stop-and-Wait":
        drop_list = [req.drop_frame_index] if req.drop_frame_index is not None else []
        return simulate_stop_and_wait(req.total_frames, drop_list)
    elif req.protocol == "Selective-Repeat":
        return simulate_selective_repeat(req.total_frames, req.window_size, req.drop_frame_index)
    else:
        return simulate_go_back_n(req.total_frames, req.window_size, req.drop_frame_index)

@router.post("/routing/dijkstra")
def api_calculate_dijkstra(req: DijkstraRequest):
    return calculate_dijkstra(req.nodes, req.links, req.source)

@router.post("/routing/distance-vector")
def api_calculate_distance_vector(req: DijkstraRequest):
    return calculate_distance_vector(req.nodes, req.links)

@router.post("/fragmentation/calculate")
def api_calculate_fragmentation(req: FragmentationRequest):
    dummy_payload = b"X" * req.payload_size_bytes
    frags, err = fragment_ipv4_packet(
        src_ip="192.168.1.100",
        dst_ip="10.0.0.50",
        payload=dummy_payload,
        mtu=req.mtu,
        flags_df=req.flags_df
    )
    return {
        "payload_size_bytes": req.payload_size_bytes,
        "mtu": req.mtu,
        "flags_df": req.flags_df,
        "error": err,
        "fragment_count": len(frags),
        "fragments": frags
    }

@router.post("/dns/resolve")
def api_resolve_dns(req: DNSResolveRequest):
    resolver = DNSResolver()
    return resolver.resolve_domain(req.domain)

@router.post("/dhcp/dora")
def api_simulate_dhcp(req: DHCPSimulateRequest):
    server = DHCPServer()
    return {
        "client_mac": req.client_mac,
        "steps": server.simulate_dora_exchange(req.client_mac)
    }

