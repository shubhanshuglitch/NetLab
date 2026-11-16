from typing import Dict, Any, List, Optional
from backend.app.schemas.packets import ApplicationHeader


class DHCPServer:
    """
    Simulates DHCP Server with DORA process and dynamic address pool.
    """
    def __init__(
        self,
        server_ip: str = "192.168.1.1",
        subnet_mask: str = "255.255.255.0",
        pool_start: int = 100,
        pool_end: int = 200,
        lease_time_sec: int = 86400
    ):
        self.server_ip = server_ip
        self.subnet_mask = subnet_mask
        self.pool_start = pool_start
        self.pool_end = pool_end
        self.current_alloc = pool_start
        self.lease_time = lease_time_sec
        self.leases: Dict[str, Dict[str, Any]] = {}  # MAC -> Lease info

    def simulate_dora_exchange(self, client_mac: str, requested_hostname: str = "Parv-Laptop") -> List[Dict[str, Any]]:
        """
        Executes complete 4-step DHCP exchange:
        1. DHCP Discover (Client -> Broadcast)
        2. DHCP Offer (Server -> Client)
        3. DHCP Request (Client -> Broadcast)
        4. DHCP Ack (Server -> Client)
        """
        # Assign next IP
        assigned_ip = f"192.168.1.{self.current_alloc}"
        self.current_alloc += 1
        if self.current_alloc > self.pool_end:
            self.current_alloc = self.pool_start

        self.leases[client_mac] = {
            "ip": assigned_ip,
            "mask": self.subnet_mask,
            "gateway": self.server_ip,
            "dns": "8.8.8.8",
            "lease_sec": self.lease_time
        }

        steps = [
            {
                "step": 1,
                "type": "DHCP_DISCOVER",
                "src_ip": "0.0.0.0",
                "dst_ip": "255.255.255.255",
                "src_mac": client_mac,
                "dst_mac": "FF:FF:FF:FF:FF:FF",
                "details": f"Client {client_mac} broadcasts DISCOVER searching for DHCP servers on local broadcast domain.",
                "explanation": "Because the client does not yet have an IP address, its source IP is 0.0.0.0 and destination is the limited broadcast address 255.255.255.255 (UDP port 67)."
            },
            {
                "step": 2,
                "type": "DHCP_OFFER",
                "src_ip": self.server_ip,
                "dst_ip": "255.255.255.255",
                "src_mac": "00:1A:2B:3C:4D:01",
                "dst_mac": client_mac,
                "offered_ip": assigned_ip,
                "details": f"DHCP Server ({self.server_ip}) offers IP {assigned_ip} with lease time {self.lease_time}s.",
                "explanation": "The DHCP server reserves an IP from its pool and replies with configuration parameters: Subnet Mask, Default Gateway, DNS, and Lease Duration."
            },
            {
                "step": 3,
                "type": "DHCP_REQUEST",
                "src_ip": "0.0.0.0",
                "dst_ip": "255.255.255.255",
                "src_mac": client_mac,
                "dst_mac": "FF:FF:FF:FF:FF:FF",
                "requested_ip": assigned_ip,
                "details": f"Client broadcasts REQUEST officially requesting {assigned_ip} from server {self.server_ip}.",
                "explanation": "Client announces acceptance via broadcast so any other DHCP servers that made offers know their offers were declined and can release reserved IPs."
            },
            {
                "step": 4,
                "type": "DHCP_ACK",
                "src_ip": self.server_ip,
                "dst_ip": assigned_ip,
                "src_mac": "00:1A:2B:3C:4D:01",
                "dst_mac": client_mac,
                "assigned_ip": assigned_ip,
                "details": f"Server finalizes lease for {assigned_ip}. Client configures its local network interface.",
                "explanation": "Server confirms configuration. The client can now join the network, use the default gateway, and communicate with other hosts."
            }
        ]

        return steps

