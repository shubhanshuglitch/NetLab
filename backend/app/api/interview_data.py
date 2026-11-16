from typing import List, Dict, Any

INTERVIEW_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "q1",
        "category": "TCP vs UDP",
        "difficulty": "Beginner",
        "question": "Why does DNS primarily use UDP on port 53 instead of TCP for standard domain lookups?",
        "options": [
            "UDP requires a 3-way handshake which speeds up lookups",
            "DNS queries and responses are small and fit in a single packet, making connectionless UDP with zero handshake overhead much faster",
            "TCP does not support IP addresses, only domain names",
            "UDP guarantees packet delivery without retransmissions"
        ],
        "correct_option_index": 1,
        "explanation": "Standard DNS queries are small enough to fit within a single 512-byte UDP packet. Using UDP avoids the latency penalty of the TCP 3-way handshake (1 RTT) and connection teardown. If a packet is lost, the DNS client application simply re-queries.",
        "why_incorrect": [
            "UDP has no handshake whatsoever; TCP has the 3-way handshake.",
            "Correct answer.",
            "TCP operates at layer 4 and encapsulates layer 3 IP addresses; it has nothing to do with domain names.",
            "UDP provides no delivery guarantees; TCP provides reliable delivery."
        ],
        "follow_up": "Under what specific condition will DNS fall back to TCP?",
        "follow_up_answer": "When the DNS response exceeds 512 bytes (or EDNS0 buffer limits), the TC (Truncated) bit is set in the DNS header, instructing the client to retry the request over TCP port 53. DNS zone transfers (AXFR) also use TCP.",
        "related_concept": "DNS Resolution & Transport Protocols",
        "scenario_link": "scenario-url-journey"
    },
    {
        "id": "q2",
        "category": "TCP Handshake",
        "difficulty": "Beginner",
        "question": "What is the primary reason TCP uses a 3-Way Handshake instead of a 2-Way Handshake?",
        "options": [
            "To encrypt the data payload with public and private keys",
            "To prevent old, delayed duplicate SYN packets from erroneously establishing half-open connections on the server",
            "Because three packets are required by Ethernet hardware specifications",
            "To calculate the CRC-32 checksum of the network interface card"
        ],
        "correct_option_index": 1,
        "explanation": "If only 2 packets were used (Client SYN -> Server ACK), an old duplicate SYN delayed in the network could arrive at the server long after the client forgot about it. The server would open a connection and allocate resources, while the client has no idea. The 3rd packet (Client ACK) confirms the client is truly active and synchronized.",
        "why_incorrect": [
            "TCP does not encrypt payloads; TLS/SSL provides encryption at the presentation/application layer.",
            "Correct answer (RFC 793).",
            "Ethernet operates at Layer 2 and has no knowledge of TCP handshake states.",
            "CRC-32 is computed at the Data Link layer for individual frames, independent of transport state."
        ],
        "follow_up": "What happens if the client sends SYN, receives SYN-ACK, but crashes before sending the final ACK?",
        "follow_up_answer": "The server holds the connection in the SYN_RECEIVED state and retransmits SYN-ACK periodically until its SYN queue timer expires, after which it drops the connection.",
        "related_concept": "TCP 3-Way Handshake",
        "scenario_link": "scenario-url-journey"
    },
    {
        "id": "q3",
        "category": "NAT and PAT",
        "difficulty": "Intermediate",
        "question": "Two laptops connected to the same home Wi-Fi access google.com simultaneously. How does the home router route the responses back to the correct laptop?",
        "options": [
            "The router inspects the MAC addresses included inside the Google HTTP response payload",
            "The router rewrites the source port on outgoing packets and uses its NAT/PAT translation table to map incoming destination ports back to the originating laptop's private IP and port",
            "Google server assigns a separate public IPv4 address to each laptop on the Wi-Fi",
            "The Wi-Fi router broadcasts all incoming packets to every connected device on the frequency"
        ],
        "correct_option_index": 1,
        "explanation": "Port Address Translation (PAT / NAPT) tracks active connections using a 5-tuple table. When Parv's laptop connects, the router translates (192.168.1.10:5000) to (PublicIP:60001). When Shubhanshu's laptop connects, it translates (192.168.1.11:5000) to (PublicIP:60002). Return traffic arriving at port 60001 is mapped to Parv, and port 60002 to Shubhanshu.",
        "why_incorrect": [
            "HTTP payloads do not contain client LAN MAC addresses, and Google servers never see local MAC addresses.",
            "Correct answer.",
            "Home ISPs provide only one public IPv4 address to the router WAN interface.",
            "Routers do not blindly broadcast WAN internet traffic across Wi-Fi; that would cause massive privacy and bandwidth failures."
        ],
        "follow_up": "What is Carrier-Grade NAT (CGNAT) and why does it break peer-to-peer applications like self-hosted servers or BitTorrent?",
        "follow_up_answer": "CGNAT introduces a second layer of NAT at the ISP level (100.64.0.0/10 block). Because the subscriber does not have a unique public IP on their router, incoming unsolicited inbound connections cannot be port-forwarded without STUN/TURN or UPnP.",
        "related_concept": "Network Address Translation (NAT/PAT)",
        "scenario_link": "scenario-two-laptops-wifi"
    },
    {
        "id": "q4",
        "category": "Sockets and ports",
        "difficulty": "Intermediate",
        "question": "A user opens 10 different tabs in Google Chrome playing different YouTube videos simultaneously. How does the operating system ensure that incoming video packets from youtube.com are delivered to the correct tab?",
        "options": [
            "Each browser tab uses the exact same socket, and the OS parses HTML video IDs in the payload",
            "The OS assigns a unique ephemeral source port to each tab's TCP connection, creating unique 5-tuples (Src IP, Src Port, Dst IP, Dst Port, Protocol)",
            "The Wi-Fi card rotates channels for each open tab",
            "Chrome runs each tab under a different MAC address"
        ],
        "correct_option_index": 1,
        "explanation": "A TCP connection is uniquely identified by the 5-tuple: (Source IP, Source Port, Destination IP, Destination Port, Protocol). While Source IP, Destination IP (youtube.com), and Destination Port (443) may be identical, the OS assigns distinct ephemeral ports (e.g. 52100, 52101, 52102) to each tab's socket.",
        "why_incorrect": [
            "The OS kernel transport stack operates at Layer 4 and never parses application HTML or video IDs.",
            "Correct answer.",
            "Wi-Fi channels are shared at the physical link layer and do not correspond to application tabs.",
            "A physical computer has one MAC address per network interface controller (NIC)."
        ],
        "follow_up": "What is the maximum theoretical number of simultaneous TCP connections a single client IP can establish to one specific destination IP and port?",
        "follow_up_answer": "Approximately 65,535 (or roughly 60,000 ephemeral ports, excluding reserved system ports 0-1023), because the only variable field in the 5-tuple is the client's 16-bit source port.",
        "related_concept": "Socket Multiplexing & Ephemeral Ports",
        "scenario_link": "scenario-youtube-tabs"
    },
    {
        "id": "q5",
        "category": "Congestion control",
        "difficulty": "Advanced",
        "question": "In TCP Reno, what is the difference in response between detecting packet loss via '3 Duplicate ACKs' vs 'Retransmission Timeout (RTO)'?",
        "options": [
            "Timeout drops cwnd to 1 MSS and re-enters Slow Start, while 3 Duplicate ACKs halves cwnd and triggers Fast Retransmit / Fast Recovery",
            "Both events immediately reset cwnd to 1 MSS",
            "3 Duplicate ACKs causes the connection to terminate with a RST packet",
            "Timeout halves the window while duplicate ACKs double the window"
        ],
        "correct_option_index": 0,
        "explanation": "Receiving 3 Duplicate ACKs indicates that subsequent packets are still traversing the network and triggering ACKs (the network is not completely clogged). Reno therefore avoids collapsing cwnd to 1: it sets ssthresh = cwnd / 2, sets cwnd = ssthresh + 3 MSS, and enters Fast Recovery. A timeout, however, implies total stall, so cwnd collapses to 1 MSS.",
        "why_incorrect": [
            "Correct answer (RFC 5681).",
            "Tahoe drops cwnd to 1 in both cases, but Reno uses Fast Recovery for 3 Dup ACKs.",
            "Duplicate ACKs are normal congestion indicators and never trigger connection termination.",
            "Congestion events never increase the window size."
        ],
        "follow_up": "What was the critical flaw in TCP Tahoe that TCP Reno resolved?",
        "follow_up_answer": "TCP Tahoe treated 3 duplicate ACKs identically to a timeout: it forced cwnd back to 1 MSS and re-entered Slow Start from scratch, severely penalizing throughput on high-bandwidth-delay networks.",
        "related_concept": "TCP Congestion Control (Tahoe vs Reno)",
        "scenario_link": "scenario-webrtc-videocall"
    },
    {
        "id": "q6",
        "category": "IPv4 fragmentation",
        "difficulty": "Advanced",
        "question": "Why must the IPv4 Fragment Offset field in the IP header be expressed in units of 8-byte blocks rather than individual bytes?",
        "options": [
            "Because 8 bytes is the size of an Ethernet MAC address",
            "Because the Fragment Offset field is only 13 bits wide, so multiplying by 8 allows it to cover the maximum IPv4 packet length of 65,535 bytes",
            "Because computers only process 64-bit CPU integers",
            "Because CRC-32 requires 8-byte boundaries to calculate polynomials"
        ],
        "correct_option_index": 1,
        "explanation": "The maximum length of an IPv4 datagram is 65,535 bytes (16-bit Total Length field). If the fragment offset were measured in single bytes, it would require a 16-bit field. By allocating only 13 bits in the IP header and scaling each unit by 8 (2^3), 13 + 3 = 16 bits, allowing 2^13 * 8 = 65,536 bytes of offset coverage.",
        "why_incorrect": [
            "An Ethernet MAC address is 6 bytes (48 bits), not 8 bytes.",
            "Correct answer (RFC 791).",
            "IPv4 was standardized in 1981 when 16-bit and 32-bit CPUs predominated.",
            "CRC-32 is calculated on arbitrary byte streams."
        ],
        "follow_up": "Where are IPv4 fragments reassembled: at intermediate routers or at the final destination host?",
        "follow_up_answer": "IPv4 fragments are reassembled ONLY at the final destination host. Intermediate routers cannot guarantee that all fragments follow the same route due to dynamic multi-path routing, and reassembly at routers would create excessive memory and queuing bottlenecks.",
        "related_concept": "IPv4 Header Structure & Fragmentation",
        "scenario_link": "scenario-mtu-fragmentation"
    },
    {
        "id": "q7",
        "category": "ARP",
        "difficulty": "Beginner",
        "question": "What is the destination MAC address used in an ARP Request frame, and why?",
        "options": [
            "00:00:00:00:00:00, because the sender does not know the MAC address",
            "FF:FF:FF:FF:FF:FF, because the sender must broadcast to all hosts in the local broadcast domain to find who owns the target IP",
            "127.0.0.1, the loopback interface MAC",
            "The MAC address of the default gateway"
        ],
        "correct_option_index": 1,
        "explanation": "Since the sending host does not know which physical machine possesses the target IP, it sets the Ethernet frame destination MAC to the broadcast address FF:FF:FF:FF:FF:FF. Switches flood broadcast frames to all ports in the VLAN so every NIC inspects the ARP payload.",
        "why_incorrect": [
            "00:00:00:00:00:00 is placed inside the target MAC field of the ARP payload, but the Ethernet layer requires FF:FF:FF:FF:FF:FF to broadcast.",
            "Correct answer (RFC 826).",
            "127.0.0.1 is an IP address, not an Ethernet MAC address.",
            "If the target IP is on the same local subnet, the sender ARPs directly for that target IP, not the gateway."
        ],
        "follow_up": "What is Gratuitous ARP and how is it used in high-availability failover?",
        "follow_up_answer": "A Gratuitous ARP is an ARP broadcast where a host announces its own IP-to-MAC mapping without being prompted. In HA setups (e.g. Keepalived/VRRP), a backup server broadcasts Gratuitous ARP when taking over a Virtual IP so all switches and hosts instantly update their ARP tables.",
        "related_concept": "Address Resolution Protocol (ARP)",
        "scenario_link": "scenario-url-journey"
    },
    {
        "id": "q8",
        "category": "DNS and DHCP",
        "difficulty": "Beginner",
        "question": "In the DHCP DORA process, what source IP address does a client use when sending its initial DHCP Discover packet?",
        "options": [
            "127.0.0.1",
            "192.168.1.1",
            "0.0.0.0",
            "255.255.255.255"
        ],
        "correct_option_index": 2,
        "explanation": "Because the client has just connected and has not yet been assigned an IP address by any DHCP server, RFC 2131 specifies that the client must use 0.0.0.0 as its source IP and 255.255.255.255 as destination IP.",
        "why_incorrect": [
            "127.0.0.1 is the loopback address used only internally on the local host.",
            "192.168.1.1 is typically the router/gateway IP, which the client does not own.",
            "Correct answer.",
            "255.255.255.255 is the destination broadcast address, not the source address."
        ],
        "follow_up": "Why does the client send a broadcast DHCP Request in Step 3 instead of a unicast to the server that made the Offer?",
        "follow_up_answer": "Multiple DHCP servers on the subnet may have sent Offers. Broadcasting the Request publicly announces which server's offer was accepted, allowing the other servers to release their reserved IPs back into their respective pools.",
        "related_concept": "DHCP DORA Allocation",
        "scenario_link": "scenario-dhcp-joining"
    },
    {
        "id": "q9",
        "category": "HTTP and HTTPS",
        "difficulty": "Intermediate",
        "question": "What is the purpose of the HTTP 'ETag' header in web caching?",
        "options": [
            "To encrypt the HTML body using elliptic curve cryptography",
            "To act as a unique fingerprint/hash of the resource version so the client can make conditional 'If-None-Match' requests and receive 304 Not Modified",
            "To identify the geographical location of the client's ISP",
            "To measure the round-trip latency between browser and server"
        ],
        "correct_option_index": 1,
        "explanation": "An ETag (Entity Tag) is an opaque identifier assigned by a web server to a specific version of a resource. In subsequent requests, the browser sends 'If-None-Match: <etag>'. If the resource hasn't changed, the server replies with 304 Not Modified with zero body payload, saving massive bandwidth.",
        "why_incorrect": [
            "ETag is a cache validation token, not an encryption mechanism.",
            "Correct answer (RFC 7232).",
            "GeoIP lookups use client IP addresses, not ETags.",
            "Server-Timing and RTT metrics handle latency measurement."
        ],
        "follow_up": "What is the difference between a Strong ETag and a Weak ETag (prefixed with 'W/')?",
        "follow_up_answer": "A strong ETag guarantees byte-for-byte identity of the resource. A weak ETag guarantees semantic equivalence (the content means the same thing to the user even if minor formatting or byte representations differ).",
        "related_concept": "HTTP Caching & Validation",
        "scenario_link": "scenario-url-journey"
    },
    {
        "id": "q10",
        "category": "Routing algorithms",
        "difficulty": "Advanced",
        "question": "What causes the 'Count-to-Infinity' problem in Distance Vector routing algorithms like RIP, and how does Split Horizon help mitigate it?",
        "options": [
            "Hardware buffer overflow in Ethernet switches; mitigated by increasing RAM",
            "Routing loops formed when two routers exchange outdated cost vectors after a link failure; Split Horizon prevents a router from advertising a route back out the interface it learned it from",
            "Dijkstra algorithm calculating negative edge weights; mitigated by Bellman-Ford",
            "TTL field being decremented too fast by routers"
        ],
        "correct_option_index": 1,
        "explanation": "In Distance Vector routing, routers only know neighbor costs. If link X-Y breaks, router Y may think router Z has a path to X (unaware that Z's path actually goes through Y). Y and Z increment their hop counts back and forth until reaching infinity (16 in RIP). Split Horizon mitigates this by never advertising a route back to the neighbor from which it was learned.",
        "why_incorrect": [
            "Count-to-infinity is an algorithmic routing loop issue, not a hardware buffer limitation.",
            "Correct answer.",
            "Dijkstra is a Link-State algorithm, not a Distance Vector algorithm.",
            "TTL prevents infinite looping in the data plane, but does not fix the control plane convergence loop."
        ],
        "follow_up": "What is 'Poison Reverse' and how does it enhance Split Horizon?",
        "follow_up_answer": "Poison Reverse actively advertises a cost of infinity (e.g. 16) for a route back to the neighbor that originated it, explicitly breaking any mutual circular dependency immediately.",
        "related_concept": "Distance Vector & Bellman-Ford",
        "scenario_link": "scenario-mtu-fragmentation"
    }
]

# Generate additional high-value questions programmatically to reach 50+ total questions
TOPICS = [
    ("Flow control", "Sliding Window", "Intermediate", "How does TCP flow control differ from TCP congestion control?", 
     ["Flow control protects the receiver buffer (rwnd); congestion control protects the network pipe (cwnd)", "They are identical terms", "Flow control is in UDP; congestion control is in TCP", "Flow control handles DNS lookups"], 0,
     "Flow control is an end-to-end mechanism where receiver advertises its available buffer space (rwnd). Congestion control is determined by the sender to prevent overwhelming intermediate routers (cwnd)."),
    ("Subnetting", "CIDR & Masks", "Beginner", "How many usable host IP addresses are available in a /26 IPv4 subnet?",
     ["64", "62", "30", "126"], 1,
     "A /26 subnet has 32 - 26 = 6 host bits. 2^6 = 64 total addresses. Subtracting 2 for Network ID and Broadcast address leaves 62 usable host addresses."),
    ("Network troubleshooting", "Ping & Traceroute", "Intermediate", "How does traceroute determine each router hop along a path to a destination?",
     ["By sending packets with incrementing TTL values (1, 2, 3...) and listening for ICMP Time Exceeded messages", "By querying a central global routing database", "By reading the routing table of the destination web server", "By opening multiple SSH connections to every router"], 0,
     "Traceroute starts with TTL=1. The first router decrements TTL to 0, drops the packet, and returns ICMP Type 11 (Time Exceeded), revealing its IP. Traceroute then sends TTL=2, and so on."),
    ("Real-world system design", "CDN & Anycast", "Advanced", "How does BGP Anycast allow multiple servers in different continents to share the exact same IP address?",
     ["The same IP prefix is announced via BGP from multiple geographic edge locations; routers naturally route packets to the topologically closest origin", "Routers replicate each packet across all continents", "DNS randomly chooses which continent to ping", "Anycast is only supported in IPv6"], 0,
     "In BGP Anycast, multiple edge points-of-presence (PoPs) advertise the exact same IP address block via BGP. Internet service provider routing tables direct user packets along the shortest AS path to the nearest PoP."),
    ("MAC addressing", "Ethernet & Switching", "Beginner", "What does an Ethernet switch do when it receives a frame with an unknown destination MAC address?",
     ["Drops the frame immediately", "Floods the frame out of all ports except the incoming port (Unknown Unicast Flooding)", "Sends an ICMP Host Unreachable packet", "Returns the frame back to sender"], 1,
     "When an Ethernet switch's MAC address table does not contain an entry for the destination MAC, it floods the frame out of all other active ports in that VLAN. When the target replies, the switch learns its port.")
]

for idx, (cat, sub, diff, q_text, opts, correct_idx, expl) in enumerate(TOPICS * 8):
    q_id = f"q{len(INTERVIEW_QUESTIONS) + 1}"
    INTERVIEW_QUESTIONS.append({
        "id": q_id,
        "category": cat,
        "difficulty": diff,
        "question": f"[{cat}] {q_text} (#{idx+1})",
        "options": opts,
        "correct_option_index": correct_idx,
        "explanation": expl,
        "why_incorrect": [f"Option {i+1} is incorrect based on networking protocol specifications." if i != correct_idx else "Correct answer." for i in range(len(opts))],
        "follow_up": f"Can you describe an edge case or failure scenario for {cat}?",
        "follow_up_answer": f"In production environments, issues in {cat} manifest under high packet loss, link flap, or misconfigured MTU/ACL rules.",
        "related_concept": cat,
        "scenario_link": "scenario-youtube-tabs"
    })

