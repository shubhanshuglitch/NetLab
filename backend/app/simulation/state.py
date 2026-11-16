from typing import Dict, Any, List, Optional
from backend.app.schemas.topology import TopologyConfig, DeviceConfig, LinkConfig
from backend.app.schemas.packets import PacketModel, SimulationEventModel
from backend.app.schemas.simulations import SimulationStats


class SimulationState:
    """Encapsulates the entire state of a simulation instance."""
    def __init__(self, topology: TopologyConfig):
        self.topology = topology
        self.devices: Dict[str, DeviceConfig] = {d.id: d for d in topology.devices}
        self.links: Dict[str, LinkConfig] = {l.id: l for l in topology.links}
        self.current_time_ms: float = 0.0
        self.events: List[SimulationEventModel] = []
        self.packets: List[PacketModel] = []
        self.stats = SimulationStats()
        self.status: str = "IDLE"  # IDLE, RUNNING, PAUSED, COMPLETED
        self.current_step_index: int = 0

