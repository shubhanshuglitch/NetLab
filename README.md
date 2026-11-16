# NetLab — Interactive Computer Networks Learning & Real-World Simulation Platform

> **Understand Networks. See Every Packet. Learn by Experimenting.**

NetLab is a full-stack, production-quality educational networking laboratory. It bridges the gap between theoretical computer networks education (textbooks, RFCs, and static diagrams) and practical system engineering through interactive simulation, packet inspection, parameter manipulation, and deterministic causal explanations.

---

## 🌟 Why NetLab?

When students learn computer networks, they memorize protocol definitions and formulas, yet struggle with fundamental real-world questions:
- *How does YouTube differentiate two browser tabs playing different videos simultaneously?*
- *How do two laptops connected to the same home Wi-Fi communicate with the internet without their packets mixing up?*
- *What happens when you enter google.com from keystroke to rendered HTML?*
- *Why does Zoom video calling use UDP while file downloads use TCP?*
- *What causes packet fragmentation when MTU is constrained?*

NetLab answers every question using an active learning loop:
$$\text{QUESTION} \longrightarrow \text{VISUALIZATION} \longrightarrow \text{SIMULATION} \longrightarrow \text{PACKET INSPECTION} \longrightarrow \text{EXPLANATION} \longrightarrow \text{EXPERIMENT}$$

---

## 🛠️ Complete Application Modules

### 1. Module A — Learn / Concept Visualizer
Layer-by-layer exploration with real algorithmic implementations and live parameters:
- **Application Layer**: Hierarchical recursive DNS resolution tree, DHCP DORA 4-way allocation, HTTP/1.1 request/response lifecycle.
- **Transport Layer**: TCP 3-way handshake, 4-way teardown, Sliding window, Flow control, TCP Tahoe vs Reno congestion control with CWND graphs.
- **Network Layer**: Dijkstra link-state shortest path, Distance Vector (Bellman-Ford) routing, RFC 791 IPv4 fragmentation with 8-byte block alignment and destination reassembly, ARP cache resolution, NAPT/PAT port address translation.
- **Data Link Layer**: Ethernet II framing, IEEE 802.3 CRC-32 bitwise GF(2) XOR division remainder generation, Stop-and-Wait, Go-Back-N, and Selective Repeat ARQ comparisons under injected frame drops.
- **Physical Layer**: Latency modeling, transmission bandwidth, bit error rate corruption.

### 2. Module B — Real-World Scenario Simulator
Realistic scenarios with full preconfigured topologies and protocol walkthroughs:
- **Two YouTube Tabs on One Laptop**: Socket multiplexing & 5-tuple demultiplexing.
- **Two Laptops Accessing YouTube on Same Wi-Fi**: NAPT/PAT port translation table dynamics.
- **What Happens When You Enter google.com?**: Complete 5-layer journey (DNS → ARP → TCP Handshake → TLS → HTTP).
- **Device Joining Wi-Fi**: DHCP DORA 4-way handshake broadcast mechanics.
- **WhatsApp Message Delivery & Offline Store-and-Forward**: Persistent sockets and transient queueing.
- **Video Calling (WebRTC / UDP) vs File Download (TCP)**: Latency vs reliability trade-offs and Head-of-Line blocking.
- **IPv4 MTU Mismatch & Fragmentation**: Routers slicing packets across an 800-byte WAN link and reassembling at the destination.

### 3. Module C — Interview Lab
Dedicated technical interview preparation:
- **50+ Curated Questions** categorized by topic: TCP vs UDP, DNS & DHCP, NAT & PAT, Congestion Control, Routing, Subnetting, ARP, Troubleshooting, System Design.
- Predict/submit answers with instant evaluation.
- Detailed technical explanation of the correct choice.
- **Why alternative choices are wrong** breakdown.
- Interviewer follow-up questions and scenario cross-links.
- Progress tracking and question bookmarking.

### 4. Module D — End-to-End Network Simulator & Network Lab
The centerpiece interactive laboratory:
- **Panel 1: Visual Network Topology** (powered by `@xyflow/react`): Realistic hardware nodes, link metrics, and live packet pulse highlights.
- **Panel 2: Synchronized Event Timeline**: Chronological event logs with microsecond timestamps.
- **Panel 3: Technical Packet Inspector**:
  * Decoded 5-layer header structure (Ethernet MAC, IPv4 checksum/TTL/flags, TCP/UDP ports/seq/ack, Application payload).
  * Layer-by-layer Encapsulation & Decapsulation view.
  * Formatted Hexadecimal & ASCII memory dump.
- **"Why Did This Happen?" Explanation Engine**: Protocol-grounded causal explanation for every event.
- **Live Analytics**: Packets sent/received/dropped/retransmitted, Throughput, and interactive Congestion Window (CWND) chart over time.
- **Failure Injection**: Sliders for simulated packet loss rate, bit error rate, and MTU limits.

---

## 💻 Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS v4, `@xyflow/react`, Zustand, Recharts, Lucide Icons |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, NetworkX, Uvicorn, WebSockets |
| **Testing** | Pytest, FastAPI TestClient, TypeScript Strict Verification |
| **Deployment** | Docker, Docker Compose, Nginx |

---

## 🚀 Quickstart Guide

### 1. Clone & Setup Backend
```bash
# Activate virtual environment
python -m venv backend_venv
# On Windows PowerShell:
.\backend_venv\Scripts\Activate.ps1
# On Linux / macOS:
source backend_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn backend.app.main:app --reload --port 8000
```
Backend API will be running at `http://127.0.0.1:8000`.
Interactive Swagger Docs: `http://127.0.0.1:8000/docs`.

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend application will be running at `http://localhost:5173`.

### 3. Run Automated Tests
```bash
# Run backend test suite (20 unit and integration tests)
python -m pytest backend/app/tests/ -v

# Verify frontend build
cd frontend
npm run build
```

### 4. Docker Deployment
```bash
docker-compose up --build
```

---

## 📄 License
MIT License. Built for Computer Science and Engineering students, educators, and software engineers worldwide.

