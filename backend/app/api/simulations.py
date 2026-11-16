import asyncio
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from backend.app.schemas.simulations import SimulationRequest, SimulationResponse
from backend.app.schemas.topology import TopologyConfig
from backend.app.simulation.engine import SimulationEngine
from backend.app.scenarios.scenario_definitions import get_default_scenarios

router = APIRouter(prefix="/simulations", tags=["Simulations"])

# In-memory storage for active simulation runs
_SIMULATION_CACHE: Dict[str, SimulationResponse] = {}

def _get_topology(req: SimulationRequest) -> TopologyConfig:
    if req.custom_topology:
        return req.custom_topology
    if req.topology_id:
        for s in get_default_scenarios():
            if s["topology"].id == req.topology_id or s["id"] == req.topology_id:
                return s["topology"]
    # Fallback to first default scenario topology
    return get_default_scenarios()[0]["topology"]

@router.post("", response_model=SimulationResponse)
def create_and_run_simulation(req: SimulationRequest):
    try:
        topo = _get_topology(req)
        engine = SimulationEngine(topo, random_seed=req.random_seed)
        res = engine.execute_simulation(req)
        _SIMULATION_CACHE[res.simulation_id] = res
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{sim_id}", response_model=SimulationResponse)
def get_simulation(sim_id: str):
    if sim_id in _SIMULATION_CACHE:
        return _SIMULATION_CACHE[sim_id]
    raise HTTPException(status_code=404, detail="Simulation not found")

@router.get("/{sim_id}/events")
def get_simulation_events(sim_id: str):
    if sim_id in _SIMULATION_CACHE:
        return _SIMULATION_CACHE[sim_id].events
    raise HTTPException(status_code=404, detail="Simulation not found")

@router.get("/{sim_id}/packets")
def get_simulation_packets(sim_id: str):
    if sim_id in _SIMULATION_CACHE:
        return _SIMULATION_CACHE[sim_id].packets
    raise HTTPException(status_code=404, detail="Simulation not found")

