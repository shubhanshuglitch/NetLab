from typing import Dict, Tuple, Optional, List
from pydantic import BaseModel


class NATEntry(BaseModel):
    internal_ip: str
    internal_port: int
    external_ip: str
    external_port: int
    protocol: str = "TCP"
    created_at_sec: float = 0.0


class NATRouter:
    """
    Simulates Network Address Translation & Port Address Translation (NAT / NAPT / PAT).
    """
    def __init__(self, public_ip: str, port_start: int = 50000):
        self.public_ip = public_ip
        self.current_port = port_start
        self.table: List[NATEntry] = []

    def translate_outbound(self, internal_ip: str, internal_port: int, protocol: str = "TCP") -> Tuple[str, int, bool]:
        """
        Translates outbound packet from private LAN to public WAN.
        Returns (translated_src_ip, translated_src_port, is_new_entry)
        """
        # Check existing mapping
        for entry in self.table:
            if (entry.internal_ip == internal_ip and 
                entry.internal_port == internal_port and 
                entry.protocol == protocol):
                return entry.external_ip, entry.external_port, False

        # Allocate new external port
        ext_port = self.current_port
        self.current_port += 1
        entry = NATEntry(
            internal_ip=internal_ip,
            internal_port=internal_port,
            external_ip=self.public_ip,
            external_port=ext_port,
            protocol=protocol
        )
        self.table.append(entry)
        return self.public_ip, ext_port, True

    def translate_inbound(self, dst_ip: str, dst_port: int, protocol: str = "TCP") -> Optional[Tuple[str, int]]:
        """
        Translates inbound packet from public WAN to private LAN.
        Returns (internal_dst_ip, internal_dst_port) or None if no mapping exists.
        """
        if dst_ip != self.public_ip:
            return None

        for entry in self.table:
            if entry.external_port == dst_port and entry.protocol == protocol:
                return entry.internal_ip, entry.internal_port

        return None

    def get_table_snapshot(self) -> List[Dict[str, Any]]:
        return [e.model_dump() for e in self.table]

