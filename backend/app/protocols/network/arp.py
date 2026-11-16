from typing import Dict, Optional, Tuple, Any


class ARPCache:
    """Simulates an ARP table / cache mapping IP addresses to MAC addresses."""
    def __init__(self):
        self.entries: Dict[str, str] = {}  # IP -> MAC

    def lookup(self, ip: str) -> Optional[str]:
        return self.entries.get(ip)

    def learn(self, ip: str, mac: str):
        self.entries[ip] = mac

    def flush(self):
        self.entries.clear()

    def get_table(self) -> Dict[str, str]:
        return dict(self.entries)


def create_arp_request(sender_ip: str, sender_mac: str, target_ip: str) -> Dict[str, Any]:
    """Generates an ARP Request frame (broadcast destination)."""
    return {
        "operation": "ARP_REQUEST",
        "sender_mac": sender_mac,
        "sender_ip": sender_ip,
        "target_mac": "00:00:00:00:00:00",
        "target_ip": target_ip,
        "frame_dst_mac": "FF:FF:FF:FF:FF:FF",
        "explanation": f"Who has {target_ip}? Tell {sender_ip} ({sender_mac}). Broadcast to all devices on LAN."
    }


def create_arp_reply(sender_ip: str, sender_mac: str, target_ip: str, target_mac: str) -> Dict[str, Any]:
    """Generates an ARP Reply frame (unicast destination)."""
    return {
        "operation": "ARP_REPLY",
        "sender_mac": sender_mac,
        "sender_ip": sender_ip,
        "target_mac": target_mac,
        "target_ip": target_ip,
        "frame_dst_mac": target_mac,
        "explanation": f"{sender_ip} is at {sender_mac}. Unicast reply sent directly to {target_mac}."
    }

