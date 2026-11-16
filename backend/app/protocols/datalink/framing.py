from typing import Tuple, Dict, Any
from backend.app.schemas.packets import DataLinkHeader
from backend.app.protocols.datalink.crc import compute_crc32, verify_crc32


def create_ethernet_frame(src_mac: str, dst_mac: str, payload_bytes: bytes, ethertype: str = "0x0800") -> Tuple[DataLinkHeader, bytes]:
    """Encapsulates payload into an Ethernet frame with calculated CRC-32."""
    crc = compute_crc32(payload_bytes)
    header = DataLinkHeader(
        src_mac=src_mac,
        dst_mac=dst_mac,
        ethertype=ethertype,
        crc32=crc,
        is_corrupted=False,
        frame_type="Ethernet II",
        frame_status="VALID"
    )
    return header, payload_bytes


def decapsulate_frame(header: DataLinkHeader, payload_bytes: bytes) -> Dict[str, Any]:
    """Decapsulates and verifies Ethernet frame CRC."""
    is_valid = verify_crc32(payload_bytes, header.crc32)
    header.is_corrupted = not is_valid
    header.frame_status = "VALID" if is_valid else "CORRUPTED"
    return {
        "valid": is_valid,
        "header": header,
        "payload": payload_bytes
    }

