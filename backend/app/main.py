import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.simulations import router as simulations_router, _SIMULATION_CACHE
from backend.app.api.scenarios import router as scenarios_router
from backend.app.api.concepts import router as concepts_router
from backend.app.api.interview import router as interview_router
from backend.app.api.search import router as search_router

app = FastAPI(
    title="NetLab API",
    description="Interactive Computer Networks Learning & Real-World Simulation Platform Engine",
    version="1.0.0"
)

# Enable CORS for frontend Vite dev server & production builds
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register REST Routers
app.include_router(simulations_router, prefix="/api")
app.include_router(scenarios_router, prefix="/api")
app.include_router(concepts_router, prefix="/api")
app.include_router(interview_router, prefix="/api")
app.include_router(search_router, prefix="/api")


@app.get("/api/health")
def healthcheck():
    return {
        "status": "healthy",
        "service": "NetLab Simulation Engine",
        "version": "1.0.0"
    }


@app.websocket("/ws/simulations/{sim_id}")
async def websocket_simulation_stream(websocket: WebSocket, sim_id: str):
    """
    WebSockets for real-time simulation event streaming.
    Allows frontend clients to receive simulation events live with custom playback intervals.
    """
    await websocket.accept()
    try:
        # Check if simulation exists in cache
        if sim_id not in _SIMULATION_CACHE:
            await websocket.send_text(json.dumps({"error": "Simulation not found"}))
            await websocket.close()
            return

        sim_data = _SIMULATION_CACHE[sim_id]
        events = sim_data.events

        # Initial handshake confirmation
        await websocket.send_text(json.dumps({
            "type": "INIT",
            "simulation_id": sim_id,
            "total_events": len(events),
            "stats": sim_data.stats.model_dump()
        }))

        # Wait for client commands (PLAY, STEP, PAUSE, RESET)
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)
            cmd = data.get("command", "PLAY")
            speed_ms = data.get("speed_ms", 600)

            if cmd == "PLAY":
                for idx, event in enumerate(events):
                    await websocket.send_text(json.dumps({
                        "type": "EVENT",
                        "step_index": idx + 1,
                        "total_steps": len(events),
                        "event": event.model_dump()
                    }))
                    await asyncio.sleep(speed_ms / 1000.0)

                await websocket.send_text(json.dumps({
                    "type": "COMPLETED",
                    "simulation_id": sim_id,
                    "stats": sim_data.stats.model_dump()
                }))
            elif cmd == "STEP":
                step_idx = data.get("step_index", 0)
                if 0 <= step_idx < len(events):
                    await websocket.send_text(json.dumps({
                        "type": "EVENT",
                        "step_index": step_idx + 1,
                        "total_steps": len(events),
                        "event": events[step_idx].model_dump()
                    }))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_text(json.dumps({"error": str(e)}))
        except Exception:
            pass

