# NetLab REST & WebSocket API Reference

The NetLab backend exposes REST APIs and real-time WebSockets powered by FastAPI.

### Base URL: `http://localhost:8000/api`

---

## 1. Simulations Endpoints
- `POST /api/simulations`
  - Runs deterministic multi-layer network simulation across specified or preconfigured topology.
  - Body:
    ```json
    {
      "topology_id": "scenario-youtube-tabs",
      "sender_id": "laptop",
      "receiver_id": "youtube_server",
      "app_protocol": "HTTP",
      "transport_protocol": "TCP",
      "payload": "GET /video HTTP/1.1",
      "override_loss_rate": 0.1,
      "override_mtu": 1500,
      "tcp_algorithm": "Reno"
    }
    ```
- `GET /api/simulations/{id}`: Returns cached simulation response with events, packets, and metrics.
- `GET /api/simulations/{id}/events`: Returns chronological event list.
- `GET /api/simulations/{id}/packets`: Returns generated packet structures.

---

## 2. Real-Time WebSocket Streaming
- `WS /ws/simulations/{id}`
  - Streams simulation events live to frontend with customizable playback interval.
  - Commands: `PLAY`, `PAUSE`, `STEP`, `RESET`.

---

## 3. Real-World Scenarios
- `GET /api/scenarios`: List all 7 preconfigured realistic networking scenarios.
- `GET /api/scenarios/{id}`: Detailed scenario with full topology config and walkthrough steps.

---

## 4. Concept Visualizer
- `GET /api/concepts`: Concept catalog across all 5 layers.
- `POST /api/concepts/crc/calculate`: Interactive bitwise GF(2) XOR division.
- `POST /api/concepts/arq/simulate`: Stop-and-Wait, Go-Back-N, and Selective Repeat comparison.
- `POST /api/concepts/routing/dijkstra`: Step-by-step Dijkstra shortest-path calculations.
- `POST /api/concepts/fragmentation/calculate`: IPv4 MTU fragmentation calculator.
- `POST /api/concepts/dns/resolve`: Recursive domain resolution tree.
- `POST /api/concepts/dhcp/dora`: DHCP DORA sequence simulator.

---

## 5. Interview Lab
- `GET /api/interview/questions`: 50+ categorized questions with difficulty levels.
- `GET /api/interview/categories`: Available question categories.
- `POST /api/interview/verify`: Verifies user answer, returns full explanation, why alternatives fail, and follow-up question.

---

## 6. Global Search & Discovery
- `GET /api/search?q={query}`: Unified search returning matching concepts, scenarios, and interview questions.

