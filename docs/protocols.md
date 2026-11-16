# NetLab Protocol Implementations & Standards Compliance

All protocols modeled in NetLab are implemented using authentic networking RFC standards:

### 1. Data Link Layer
- **Ethernet II Framing**: Standard 14-byte MAC header (6-byte Dst, 6-byte Src, 2-byte EtherType) + 4-byte FCS CRC.
- **CRC-32 (IEEE 802.3)**: Standard polynomial `0xEDB88320` and interactive GF(2) bitwise division remainder generation.
- **Stop-and-Wait ARQ**: Alternating bit protocol with timer expiration and single frame retransmission.
- **Go-Back-N ARQ**: Cumulative ACKs, sender window $N$, receiver window 1. Packet drop causes subsequent frames to be discarded and triggers full window retransmission on timeout.
- **Selective Repeat ARQ**: Individual selective ACKs, receiver out-of-order buffering, and retransmission of exclusively missing frames.

### 2. Network Layer
- **IPv4 Headers (RFC 791)**: 20-byte base header with calculated 16-bit one's complement checksum, TTL decrement, Identification matching, and Total Length tracking.
- **IPv4 Fragmentation**: Enforces 8-byte block slice alignment `((MTU - 20) // 8) * 8`, More Fragments (MF) flag setting, Fragment Offset units calculation, and end-to-end destination reassembly.
- **Routing Algorithms**:
  - **Dijkstra Link-State**: Greedy minimum-distance relaxation yielding tentative distance tables and shortest-path forwarding trees.
  - **Distance Vector (Bellman-Ford)**: Periodic neighbor exchange matrix, count-to-infinity detection, and split horizon logic.
- **NAPT / PAT (RFC 3022)**: Dynamic translation table mapping private LAN `(IP, Port)` pairs onto public WAN gateway `(IP, Ephemeral Port)`.
- **ARP (RFC 826)**: Broadcast request (`FF:FF:FF:FF:FF:FF`) and unicast reply for IP-to-MAC resolution.

### 3. Transport Layer
- **TCP Connection State Machine (RFC 793)**: Full state transitions (`CLOSED` -> `SYN_SENT` -> `ESTABLISHED` -> `FIN_WAIT` -> `TIME_WAIT`).
- **TCP Congestion Control (RFC 5681)**:
  - Slow Start: exponential growth ($cwnd \mathrel{+}= 1$ per ACK).
  - Congestion Avoidance: linear growth ($cwnd \mathrel{+}= 1 / cwnd$ per ACK).
  - 3 Duplicate ACKs: Fast Retransmit ($ssthresh = cwnd / 2$; Reno enters Fast Recovery with window inflation; Tahoe drops to 1 MSS).
  - Timeout: $cwnd = 1$ MSS, re-enters Slow Start.
- **UDP (RFC 768)**: 8-byte header, connectionless datagram delivery, stateless multiplexing.

### 4. Application Layer
- **DNS (RFC 1035)**: Recursive resolution sequence: Cache -> Root Server (`.`) -> TLD (`.com`) -> Authoritative Nameserver.
- **DHCP (RFC 2131)**: DORA 4-way exchange (Discover, Offer, Request, ACK) with broadcast addressing.
- **HTTP/1.1 (RFC 7230)**: Request methods, response status codes, header parsing, cookies, ETags, and 304 Not Modified cache validation.

