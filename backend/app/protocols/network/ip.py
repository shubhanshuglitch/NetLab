from typing import Dict, Any
from backend.app.schemas.packets import NetworkHeader


def compute_ip_checksum(header: NetworkHeader) -> str:
    """
    Computes standard RFC 791 16-bit one's complement Internet Checksum for IPv4 header.
    """
    # Create 16-bit words
    ver_ihl = (header.version << 4) | (header.ihl & 0x0F)
    ver_ihl_tos = (ver_ihl << 8) | (header.tos_dscp & 0xFF)
    tot_len = header.total_length & 0xFFFF
    ident = header.identification & 0xFFFF
    
    flags_frag = 0
    if header.flags_df:
        flags_frag |= (1 << 14)
    if header.flags_mf:
        flags_frag |= (1 << 13)
    flags_frag |= (header.fragment_offset & 0x1FFF)
    
    ttl_proto = (header.ttl << 8) | (6 if header.protocol == "TCP" else (17 if header.protocol == "UDP" else 1))
    
    # Parse IPs to 32-bit ints
    def ip_to_words(ip_str: str):
        try:
            parts = [int(p) for p in ip_str.split('.')]
            return ((parts[0] << 8) | parts[1]), ((parts[2] << 8) | parts[3])
        except Exception:
            return 0xC0A8, 0x0101

    src1, src2 = ip_to_words(header.src_ip)
    dst1, dst2 = ip_to_words(header.dst_ip)

    words = [ver_ihl_tos, tot_len, ident, flags_frag, ttl_proto, 0, src1, src2, dst1, dst2]
    
    total = sum(words)
    # Add carry bits
    while (total >> 16) > 0:
        total = (total & 0xFFFF) + (total >> 16)
        
    checksum = (~total) & 0xFFFF
    return f"0x{checksum:04X}"


def create_ipv4_header(
    src_ip: str,
    dst_ip: str,
    total_length: int,
    protocol: str = "TCP",
    identification: int = 1,
    flags_df: bool = False,
    flags_mf: bool = False,
    fragment_offset: int = 0,
    ttl: int = 64
) -> NetworkHeader:
    header = NetworkHeader(
        version=4,
        ihl=5,
        tos_dscp=0,
        total_length=total_length,
        identification=identification,
        flags_df=flags_df,
        flags_mf=flags_mf,
        fragment_offset=fragment_offset,
        ttl=ttl,
        protocol=protocol,
        header_checksum="0x0000",
        src_ip=src_ip,
        dst_ip=dst_ip
    )
    header.header_checksum = compute_ip_checksum(header)
    return header

