# NetLab Architecture & Design Specification

## 1. System Overview
**NetLab** is an interactive, multi-layer Computer Networks learning and simulation platform designed to bridge theoretical protocol concepts with real-world system behavior.

Unlike typical educational dashboards with static diagrams, NetLab utilizes an independent event-driven Python simulation engine that processes actual protocol transitions across all five layers:
- **Application Layer**: HTTP/HTTPS, DNS recursive resolution, DHCP DORA allocation, cookies, ETags.
- **Transport Layer**: TCP state machine (3-way handshake, 4-way teardown), Tahoe & Reno congestion control (cwnd, ssthresh, Fast Retransmit, Fast Recovery), flow control (rwnd), UDP datagrams.
- **Network Layer**: IPv4 addressing, subnetting, RFC 791 fragmentation (8-byte block offsets, MF/DF flags), Dijkstra shortest-path routing, Distance Vector (Bellman-Ford) routing, ARP resolution, NAPT/PAT port address translation.
- **Data Link Layer**: Ethernet II framing, IEEE 802.3 CRC-32 checksum generation and verification, Stop-and-Wait, Go-Back-N, and Selective Repeat ARQ flow/error control.
- **Physical Layer**: Latency, bandwidth limits, channel bit error rate corruption, packet loss injection.

---

## 2. Component Synchronization (The Three Panels)
In the Network Lab module, the user experiences three synchronized panels driven by the deterministic event log:
1. **Panel 1: Network Topology Canvas** (powered by `@xyflow/react`): Shows nodes, active connections, and animated packet highlights as frames traverse links.
2. **Panel 2: Synchronized Event Timeline**: Lists every discrete protocol event chronologically with microsecond timestamps and layer tags. Clicking any step steps the entire simulator state back or forward.
3. **Panel 3: Technical Packet Inspector & Explanation Engine**: Displays:
   - Full 5-layer decoded header breakdown.
   - Encapsulation visualizer (Layer 2 frame wrapping Layer 3 datagram wrapping Layer 4 segment wrapping Layer 7 payload).
   - Hex / ASCII memory dump.
   - **Why Did This Happen?** causal reasoning engine grounded in networking RFCs.

