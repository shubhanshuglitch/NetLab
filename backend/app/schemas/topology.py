from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.app.schemas.packets import DeviceType, LinkMedium


class InterfaceConfig(BaseModel):
    name: str
    ip_address: str
    subnet_mask: str = "255.255.255.0"
    mac_address: str
    is_up: bool = True


class RoutingEntry(BaseModel):
    destination_network: str
    subnet_mask: str
    next_hop: Optional[str] = None
    interface: str
    metric: int = 1


class NATMapping(BaseModel):
    internal_ip: str
    internal_port: int
    external_ip: str
    external_port: int
    protocol: str = "TCP"


class DeviceConfig(BaseModel):
    id: str
    label: str
    type: DeviceType
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 100.0, "y": 100.0})
    interfaces: List[InterfaceConfig] = Field(default_factory=list)
    default_gateway: Optional[str] = None
    dns_server: Optional[str] = None
    routing_table: List[RoutingEntry] = Field(default_factory=list)
    arp_cache: Dict[str, str] = Field(default_factory=dict)  # IP -> MAC
    open_ports: List[int] = Field(default_factory=list)
    nat_enabled: bool = False
    nat_table: List[NATMapping] = Field(default_factory=list)
    firewall_rules: List[Dict[str, Any]] = Field(default_factory=list)
    services: List[str] = Field(default_factory=list)  # e.g. ["HTTP", "DNS", "DHCP"]
    mac_table: Dict[str, str] = Field(default_factory=dict)  # Switch: MAC -> Port


class LinkConfig(BaseModel):
    id: str
    source_id: str
    target_id: str
    medium: LinkMedium = LinkMedium.ETHERNET
    bandwidth_mbps: float = 100.0
    latency_ms: float = 10.0
    mtu_bytes: int = 1500
    loss_rate: float = 0.0  # 0.0 - 1.0
    bit_error_rate: float = 0.0  # 0.0 - 1.0
    is_active: bool = True


class TopologyConfig(BaseModel):
    id: str = "default_topo"
    name: str = "Default Topology"
    description: str = ""
    devices: List[DeviceConfig] = Field(default_factory=list)
    links: List[LinkConfig] = Field(default_factory=list)

