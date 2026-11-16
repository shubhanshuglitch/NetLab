from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.app.schemas.packets import SimulationEventModel, PacketModel, TransportProtocol, AppProtocol
from backend.app.schemas.topology import TopologyConfig


class SimulationStats(BaseModel):
    packets_transmitted: int = 0
    packets_received: int = 0
    packets_lost: int = 0
    frames_corrupted: int = 0
    retransmissions: int = 0
    average_latency_ms: float = 0.0
    throughput_kbps: float = 0.0
    packet_delivery_ratio: float = 100.0
    tcp_cwnd_history: List[Dict[str, Any]] = Field(default_factory=list)  # {"time": t, "cwnd": w, "ssthresh": s}
    fragment_count: int = 0
    connection_establishment_time_ms: Optional[float] = None


class SimulationRequest(BaseModel):
    topology_id: Optional[str] = None
    custom_topology: Optional[TopologyConfig] = None
    sender_id: str
    receiver_id: str
    app_protocol: AppProtocol = AppProtocol.HTTP
    transport_protocol: TransportProtocol = TransportProtocol.TCP
    payload: str = "Hello NetLab! Requesting resource /index.html"
    packet_size_bytes: int = 500
    override_mtu: Optional[int] = None
    override_loss_rate: Optional[float] = None
    override_bit_error_rate: Optional[float] = None
    tcp_algorithm: str = "Reno"  # "Tahoe" or "Reno"
    arq_protocol: str = "Go-Back-N"  # "Stop-and-Wait", "Go-Back-N", "Selective-Repeat"
    random_seed: int = 42


class SimulationResponse(BaseModel):
    simulation_id: str
    status: str  # IDLE, RUNNING, COMPLETED, PAUSED
    current_step: int = 0
    total_steps: int = 0
    events: List[SimulationEventModel] = Field(default_factory=list)
    packets: List[PacketModel] = Field(default_factory=list)
    stats: SimulationStats = Field(default_factory=SimulationStats)
    topology: TopologyConfig

