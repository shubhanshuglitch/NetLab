from typing import List, Dict, Any, Optional, Tuple
from backend.app.schemas.packets import NetworkHeader
from backend.app.protocols.network.ip import create_ipv4_header


def fragment_ipv4_packet(
    src_ip: str,
    dst_ip: str,
    payload: bytes,
    mtu: int,
    identification: int = 1001,
    flags_df: bool = False,
    protocol: str = "TCP",
    ttl: int = 64
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Implements RFC 791 IPv4 Fragmentation.
    Returns: (list_of_fragments, error_message_if_any)
    """
    header_len = 20
    total_len = header_len + len(payload)

    if total_len <= mtu:
        header = create_ipv4_header(
            src_ip=src_ip,
            dst_ip=dst_ip,
            total_length=total_len,
            protocol=protocol,
            identification=identification,
            flags_df=flags_df,
            flags_mf=False,
            fragment_offset=0,
            ttl=ttl
        )
        return [{
            "fragment_index": 0,
            "header": header,
            "payload_bytes": len(payload),
            "payload": payload,
            "offset_bytes": 0,
            "is_last": True
        }], None

    # Check DF bit
    if flags_df:
        return [], f"Packet size ({total_len} bytes) exceeds MTU ({mtu} bytes) and Don't Fragment (DF) flag is SET. Packet dropped; ICMP Destination Unreachable (Fragmentation Needed) generated."

    # Must fragment into chunks that are multiples of 8 bytes
    max_payload = mtu - header_len
    slice_size = (max_payload // 8) * 8

    if slice_size <= 0:
        return [], f"MTU ({mtu} bytes) is too small to carry even an 8-byte IPv4 fragment."

    fragments = []
    byte_offset = 0
    frag_idx = 0
    total_payload_bytes = len(payload)

    while byte_offset < total_payload_bytes:
        chunk = payload[byte_offset : byte_offset + slice_size]
        is_last = (byte_offset + len(chunk)) >= total_payload_bytes
        mf_flag = not is_last

        # In IPv4 header, fragment offset is measured in units of 8-byte blocks
        offset_field = byte_offset // 8

        hdr = create_ipv4_header(
            src_ip=src_ip,
            dst_ip=dst_ip,
            total_length=header_len + len(chunk),
            protocol=protocol,
            identification=identification,
            flags_df=False,
            flags_mf=mf_flag,
            fragment_offset=offset_field,
            ttl=ttl
        )

        fragments.append({
            "fragment_index": frag_idx,
            "header": hdr,
            "payload_bytes": len(chunk),
            "payload": chunk,
            "offset_bytes": byte_offset,
            "offset_units_8b": offset_field,
            "mf_flag": mf_flag,
            "is_last": is_last
        })

        byte_offset += len(chunk)
        frag_idx += 1

    return fragments, None


def reassemble_fragments(fragments: List[Dict[str, Any]]) -> Tuple[Optional[bytes], bool, str]:
    """
    Reassembles IPv4 fragments by matching Identification and reconstructing in order of offset.
    """
    if not fragments:
        return None, False, "No fragments provided for reassembly"

    # Sort fragments by byte offset
    sorted_frags = sorted(fragments, key=lambda f: f["offset_bytes"])
    
    # Verify continuous coverage
    assembled = bytearray()
    expected_offset = 0

    for frag in sorted_frags:
        if frag["offset_bytes"] != expected_offset:
            return None, False, f"Gap in fragments: expected offset {expected_offset}, got {frag['offset_bytes']}"
        assembled.extend(frag["payload"])
        expected_offset += frag["payload_bytes"]

    # Verify last fragment has MF = False
    if not sorted_frags[-1]["is_last"]:
        return None, False, "Missing final fragment (MF flag was still 1)"

    return bytes(assembled), True, f"Successfully reassembled {len(sorted_frags)} fragments into {len(assembled)} bytes payload"

