import pytest
from backend.app.protocols.datalink.crc import compute_crc32, verify_crc32, crc_bitwise_division, inject_bit_error
from backend.app.protocols.datalink.arq import simulate_stop_and_wait, simulate_go_back_n, simulate_selective_repeat
from backend.app.protocols.network.fragmentation import fragment_ipv4_packet, reassemble_fragments
from backend.app.protocols.network.routing import calculate_dijkstra, calculate_distance_vector
from backend.app.protocols.network.nat import NATRouter
from backend.app.protocols.network.ip import compute_ip_checksum, create_ipv4_header
from backend.app.protocols.transport.tcp import TCPConnection, TCPState, CongestionState
from backend.app.protocols.application.dns import DNSResolver
from backend.app.scenarios.scenario_definitions import get_default_scenarios
from backend.app.simulation.engine import SimulationEngine
from backend.app.schemas.simulations import SimulationRequest


def test_crc32_and_bit_error():
    data = b"NetLab Reliable Packet Testing"
    crc = compute_crc32(data)
    assert verify_crc32(data, crc) is True

    # Inject bit error
    corrupted = inject_bit_error(data, bit_position=5)
    assert corrupted != data
    assert verify_crc32(corrupted, crc) is False


def test_crc_bitwise_division():
    res = crc_bitwise_division("1101011011", "10011")
    assert "remainder_crc_bits" in res
    assert len(res["remainder_crc_bits"]) == 4
    assert len(res["steps"]) > 0


def test_arq_protocols():
    # Stop-and-Wait
    snw = simulate_stop_and_wait(total_frames=3, drop_frames=[1])
    assert snw["retransmissions"] >= 1
    assert len(snw["events"]) > 3

    # Go-Back-N
    gbn = simulate_go_back_n(total_frames=6, window_size=3, drop_frame_index=1)
    assert gbn["retransmissions"] >= 1
    assert any(e["is_dropped"] for e in gbn["events"])

    # Selective Repeat
    sr = simulate_selective_repeat(total_frames=6, window_size=3, drop_frame_index=1)
    assert sr["retransmissions"] == 1


def test_ipv4_fragmentation_and_reassembly():
    original_payload = b"A" * 2500
    mtu = 1000

    fragments, err = fragment_ipv4_packet(
        src_ip="192.168.1.10",
        dst_ip="10.0.0.1",
        payload=original_payload,
        mtu=mtu,
        identification=555
    )
    assert err is None
    # 2500 bytes with 776 payload per fragment => 4 fragments
    assert len(fragments) >= 3
    assert fragments[0]["mf_flag"] is True
    assert fragments[-1]["mf_flag"] is False
    assert fragments[-1]["is_last"] is True

    # Check 8-byte alignment
    for frag in fragments[:-1]:
        assert frag["payload_bytes"] % 8 == 0

    # Reassemble
    reassembled_bytes, ok, msg = reassemble_fragments(fragments)
    assert ok is True
    assert reassembled_bytes == original_payload


def test_dijkstra_routing():
    nodes = ["A", "B", "C"]
    links = [
        {"source": "A", "target": "B", "cost": 2},
        {"source": "B", "target": "C", "cost": 3},
        {"source": "A", "target": "C", "cost": 10}
    ]
    res = calculate_dijkstra(nodes, links, source="A")
    assert res["final_distances"]["C"] == 5.0
    assert res["routing_table"][1]["next_hop"] == "B"


def test_distance_vector():
    nodes = ["A", "B", "C"]
    links = [
        {"source": "A", "target": "B", "cost": 1},
        {"source": "B", "target": "C", "cost": 2}
    ]
    res = calculate_distance_vector(nodes, links)
    assert res["converged"] is True


def test_nat_router():
    nat = NATRouter(public_ip="203.0.113.1", port_start=60000)
    pub_ip, pub_port, is_new = nat.translate_outbound("192.168.1.10", 5000)
    assert pub_ip == "203.0.113.1"
    assert pub_port == 60000
    assert is_new is True

    # Inbound return lookup
    inbound = nat.translate_inbound("203.0.113.1", 60000)
    assert inbound == ("192.168.1.10", 5000)


def test_tcp_state_and_congestion_control():
    tcp = TCPConnection(src_ip="192.168.1.5", src_port=52000, dst_ip="1.1.1.1", dst_port=80, algorithm="Reno")
    assert tcp.state == TCPState.CLOSED

    syn = tcp.create_syn_packet()
    assert tcp.state == TCPState.SYN_SENT
    assert syn.flags.syn is True

    syn_ack = tcp.receive_syn_ack(peer_seq=8000, ack_num=1001)
    assert tcp.state == TCPState.ESTABLISHED

    # Reno Slow start growth
    initial_cwnd = tcp.cwnd
    tcp.on_ack_received(ack_num=1010, is_duplicate=False)
    assert tcp.cwnd > initial_cwnd

    # 3 duplicate ACKs triggers Fast Retransmit in Reno
    tcp.on_ack_received(ack_num=1010, is_duplicate=True)
    tcp.on_ack_received(ack_num=1010, is_duplicate=True)
    tcp.on_ack_received(ack_num=1010, is_duplicate=True)
    assert tcp.cong_state == CongestionState.FAST_RECOVERY


def test_dns_resolution():
    resolver = DNSResolver()
    res = resolver.resolve_domain("youtube.com")
    assert res["resolved_ip"] == "142.250.190.78"
    assert len(res["steps"]) >= 4

    # Second lookup hits cache
    cached = resolver.resolve_domain("youtube.com")
    assert cached["from_cache"] is True


def test_end_to_end_simulation():
    scenarios = get_default_scenarios()
    first_scenario = scenarios[0]
    topo = first_scenario["topology"]

    engine = SimulationEngine(topo, random_seed=42)
    req = SimulationRequest(
        sender_id=topo.devices[0].id,
        receiver_id=topo.devices[-1].id,
        payload="Test Packet Payload"
    )
    res = engine.execute_simulation(req)
    assert res.status == "COMPLETED"
    assert len(res.events) > 0
    assert res.stats.packets_transmitted >= 1
    assert res.stats.packets_received >= 1

