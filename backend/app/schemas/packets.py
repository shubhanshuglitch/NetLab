from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field


class LayerType(str, Enum):
    PHYSICAL = "physical"
    DATALINK = "datalink"
    NETWORK = "network"
    TRANSPORT = "transport"
    APPLICATION = "application"


class DeviceType(str, Enum):
    LAPTOP = "laptop"
    DESKTOP = "desktop"
    MOBILE = "mobile"
    ROUTER = "router"
    SWITCH = "switch"
    SERVER = "server"
    DNS_SERVER = "dns_server"
    FIREWALL = "firewall"
    ACCESS_POINT = "access_point"
    LOAD_BALANCER = "load_balancer"
    CDN_SERVER = "cdn_server"
    CLOUD = "cloud"


class LinkMedium(str, Enum):
    ETHERNET = "ethernet"
    WIFI = "wifi"
    WAN = "wan"
    FIBER = "fiber"


class TransportProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"


class AppProtocol(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    DNS = "DNS"
    DHCP = "DHCP"
    ECHO = "ECHO"
    CUSTOM = "CUSTOM"


class TCPFlags(BaseModel):
    syn: bool = False
    ack: bool = False
    fin: bool = False
    rst: bool = False
    psh: bool = False
    urg: bool = False

    def to_string(self) -> str:
        flags = []
        if self.syn: flags.append("SYN")
        if self.ack: flags.append("ACK")
        if self.fin: flags.append("FIN")
        if self.rst: flags.append("RST")
        if self.psh: flags.append("PSH")
        if self.urg: flags.append("URG")
        return ", ".join(flags) if flags else "NONE"


class DataLinkHeader(BaseModel):
    src_mac: str
    dst_mac: str
    ethertype: str = "0x0800"  # IPv4, 0x0806 for ARP
    crc32: str = ""
    is_corrupted: bool = False
    frame_type: str = "Ethernet II"
    frame_status: str = "VALID"  # VALID, CORRUPTED, DROPPED


class NetworkHeader(BaseModel):
    version: int = 4
    ihl: int = 5
    tos_dscp: int = 0
    total_length: int = 0
    identification: int = 1
    flags_df: bool = False
    flags_mf: bool = False
    fragment_offset: int = 0
    ttl: int = 64
    protocol: str = "TCP"  # TCP, UDP, ICMP
    header_checksum: str = "0x0000"
    src_ip: str
    dst_ip: str


class TransportHeader(BaseModel):
    protocol: str = "TCP"
    src_port: int
    dst_port: int
    seq_num: int = 0
    ack_num: int = 0
    flags: TCPFlags = Field(default_factory=TCPFlags)
    window_size: int = 65535
    checksum: str = "0x0000"
    urgent_pointer: int = 0


class ApplicationHeader(BaseModel):
    protocol: str = "HTTP"
    message_type: str = "REQUEST"  # REQUEST, RESPONSE, QUERY, OFFER, etc.
    method_or_status: str = "GET"
    url_or_path: str = "/"
    dns_query_domain: Optional[str] = None
    dns_record_type: Optional[str] = None
    dns_answers: Optional[List[Dict[str, Any]]] = None
    dhcp_type: Optional[str] = None  # DISCOVER, OFFER, REQUEST, ACK
    dhcp_offered_ip: Optional[str] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    payload: str = ""


class PacketModel(BaseModel):
    id: str
    size_bytes: int = 64
    app_header: Optional[ApplicationHeader] = None
    transport_header: Optional[TransportHeader] = None
    network_header: Optional[NetworkHeader] = None
    datalink_header: Optional[DataLinkHeader] = None
    raw_payload: str = ""
    status: str = "IN_TRANSIT"  # CREATED, IN_TRANSIT, DELIVERED, DROPPED, CORRUPTED
    current_node: str = ""
    next_node: Optional[str] = None
    creation_time: float = 0.0


class EventExplanation(BaseModel):
    what: str
    why: str
    protocol: str
    data_changed: str
    counterfactual: str
    real_world: str


class SimulationEventModel(BaseModel):
    event_id: str
    timestamp_ms: float
    event_type: str
    source_node: str
    destination_node: Optional[str] = None
    packet_id: Optional[str] = None
    packet_summary: Optional[str] = None
    layer: LayerType
    details: Dict[str, Any] = Field(default_factory=dict)
    explanation: EventExplanation
    packet_snapshot: Optional[PacketModel] = None

