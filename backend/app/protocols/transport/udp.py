from backend.app.schemas.packets import TransportHeader, TCPFlags


def create_udp_header(src_port: int, dst_port: int, payload_len: int) -> TransportHeader:
    """Creates a UDP Header (RFC 768). UDP is connectionless and stateless."""
    total_length = 8 + payload_len  # 8 bytes UDP header
    return TransportHeader(
        protocol="UDP",
        src_port=src_port,
        dst_port=dst_port,
        seq_num=0,
        ack_num=0,
        flags=TCPFlags(),
        window_size=0,
        checksum="0x0000"
    )

