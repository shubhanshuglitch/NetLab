from typing import List, Dict, Any
from backend.app.schemas.topology import TopologyConfig, DeviceConfig, LinkConfig, InterfaceConfig, RoutingEntry
from backend.app.schemas.packets import DeviceType, LinkMedium


def get_default_scenarios() -> List[Dict[str, Any]]:
    return [
        # SCENARIO 1: Two YouTube Tabs on One Laptop
        {
            "id": "scenario-youtube-tabs",
            "category": "Browser & Web",
            "title": "Two YouTube Tabs Playing Different Videos on One Laptop",
            "difficulty": "Beginner",
            "summary": "How your operating system and web browser differentiate two video streams playing simultaneously without cross-talk.",
            "core_concept": "Socket Multiplexing & 5-Tuple (Src IP, Src Port, Dst IP, Dst Port, Protocol)",
            "key_question": "Both tabs are connected to youtube.com:443 from the same laptop IP. Why doesn't Video B's audio play in Tab A?",
            "topology": TopologyConfig(
                id="topo-youtube-tabs",
                name="Single Host - Two Ephemeral Sockets",
                devices=[
                    DeviceConfig(
                        id="laptop",
                        label="Parv's Laptop (Chrome)",
                        type=DeviceType.LAPTOP,
                        position={"x": 100, "y": 200},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="192.168.1.50", mac_address="00:1A:2B:3C:4D:50")],
                        default_gateway="192.168.1.1",
                        open_ports=[52100, 52101]
                    ),
                    DeviceConfig(
                        id="router",
                        label="Home Wi-Fi Router",
                        type=DeviceType.ROUTER,
                        position={"x": 380, "y": 200},
                        interfaces=[
                            InterfaceConfig(name="lan0", ip_address="192.168.1.1", mac_address="00:1A:2B:3C:4D:01"),
                            InterfaceConfig(name="wan0", ip_address="203.0.113.15", mac_address="00:1A:2B:3C:4D:02")
                        ],
                        nat_enabled=True
                    ),
                    DeviceConfig(
                        id="youtube_server",
                        label="YouTube Video CDN Server",
                        type=DeviceType.CDN_SERVER,
                        position={"x": 680, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="142.250.190.78", mac_address="00:99:88:77:66:55")],
                        open_ports=[443]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="laptop", target_id="router", medium=LinkMedium.WIFI, bandwidth_mbps=150.0, latency_ms=5.0),
                    LinkConfig(id="l2", source_id="router", target_id="youtube_server", medium=LinkMedium.WAN, bandwidth_mbps=1000.0, latency_ms=25.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "laptop", "action": "Tab 1 opens https://youtube.com/watch?v=A. OS allocates ephemeral port 52100."},
                {"step": 2, "actor": "laptop", "action": "Tab 2 opens https://youtube.com/watch?v=B. OS allocates ephemeral port 52101."},
                {"step": 3, "actor": "router", "action": "NAT translates both sockets onto WAN IP 203.0.113.15 with external ports 60100 and 60101."},
                {"step": 4, "actor": "youtube_server", "action": "Server sends video chunks. Tab 1 arrives at 60100 -> NAT demuxes to 52100. Tab 2 arrives at 60101 -> NAT demuxes to 52101."}
            ],
            "explanation": "Transport layer multiplexing allows millions of simultaneous TCP connections. Sockets are uniquely indexed by the 5-tuple: (Source IP, Source Port, Dest IP, Dest Port, Protocol). Even though Source IP, Dest IP, and Dest Port are identical for both tabs, their distinct Source Ports (52100 vs 52101) guarantee complete isolation."
        },

        # SCENARIO 2: Two Laptops on Same Wi-Fi
        {
            "id": "scenario-two-laptops-wifi",
            "category": "Browser & Web",
            "title": "Two Laptops Accessing YouTube Through the Same Wi-Fi",
            "difficulty": "Intermediate",
            "summary": "How Network Address Translation and Port Translation (NAPT/PAT) enables an entire home or campus to share a single public IP.",
            "core_concept": "NAT / NAPT / PAT & Port Rewriting",
            "key_question": "If both laptops have private IPs (192.168.1.10 and 192.168.1.11), how does YouTube's response reach the exact laptop that asked for it?",
            "topology": TopologyConfig(
                id="topo-two-laptops",
                name="Two Laptops Sharing Wi-Fi NAT",
                devices=[
                    DeviceConfig(
                        id="laptop1",
                        label="Laptop Parv",
                        type=DeviceType.LAPTOP,
                        position={"x": 80, "y": 120},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="192.168.1.10", mac_address="00:11:22:33:44:01")],
                        default_gateway="192.168.1.1"
                    ),
                    DeviceConfig(
                        id="laptop2",
                        label="Laptop Shubhanshu",
                        type=DeviceType.LAPTOP,
                        position={"x": 80, "y": 280},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="192.168.1.11", mac_address="00:11:22:33:44:02")],
                        default_gateway="192.168.1.1"
                    ),
                    DeviceConfig(
                        id="router",
                        label="Wi-Fi Router (NAT Gateway)",
                        type=DeviceType.ROUTER,
                        position={"x": 380, "y": 200},
                        interfaces=[
                            InterfaceConfig(name="lan0", ip_address="192.168.1.1", mac_address="00:11:22:33:44:00"),
                            InterfaceConfig(name="wan0", ip_address="203.0.113.88", mac_address="00:11:22:33:44:99")
                        ],
                        nat_enabled=True
                    ),
                    DeviceConfig(
                        id="youtube",
                        label="YouTube Web Server",
                        type=DeviceType.SERVER,
                        position={"x": 680, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="142.250.190.78", mac_address="00:77:88:99:AA:BB")],
                        open_ports=[443]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="laptop1", target_id="router", medium=LinkMedium.WIFI, bandwidth_mbps=100.0, latency_ms=4.0),
                    LinkConfig(id="l2", source_id="laptop2", target_id="router", medium=LinkMedium.WIFI, bandwidth_mbps=100.0, latency_ms=4.0),
                    LinkConfig(id="l3", source_id="router", target_id="youtube", medium=LinkMedium.WAN, bandwidth_mbps=500.0, latency_ms=20.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "laptop1", "action": "Parv sends packet from 192.168.1.10:49152 to 142.250.190.78:443."},
                {"step": 2, "actor": "laptop2", "action": "Shubhanshu sends packet from 192.168.1.11:49152 to 142.250.190.78:443."},
                {"step": 3, "actor": "router", "action": "Router rewrites Parv to 203.0.113.88:61001 and Shubhanshu to 203.0.113.88:61002 in its NAT table."},
                {"step": 4, "actor": "youtube", "action": "YouTube sees both requests coming from 203.0.113.88, but on ports 61001 and 61002."},
                {"step": 5, "actor": "router", "action": "On inbound return, router translates 61001 back to Parv (192.168.1.10) and 61002 back to Shubhanshu (192.168.1.11)."}
            ],
            "explanation": "NAPT (Network Address Port Translation) creates a dynamic translation entry in the router's memory. When return traffic comes from the server destined to the router's public IP on port 61001, the router consults its table, replaces the destination with 192.168.1.10:49152, and forwards it to Parv."
        },

        # SCENARIO 3: What happens when you enter google.com
        {
            "id": "scenario-url-journey",
            "category": "Browser & Web",
            "title": "What Happens When You Type google.com into Your Browser?",
            "difficulty": "Intermediate",
            "summary": "The quintessential networking interview question: from keyboard press to rendered web page.",
            "core_concept": "Full 5-Layer Stack Protocol Orchestration",
            "key_question": "What is the exact chronological sequence of protocol interactions between entering a URL and seeing the page?",
            "topology": TopologyConfig(
                id="topo-url-journey",
                name="Complete Web Request Journey",
                devices=[
                    DeviceConfig(
                        id="client",
                        label="Client PC",
                        type=DeviceType.DESKTOP,
                        position={"x": 80, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="192.168.1.25", mac_address="00:AA:11:22:33:44")],
                        default_gateway="192.168.1.1",
                        dns_server="8.8.8.8"
                    ),
                    DeviceConfig(
                        id="gateway",
                        label="Default Gateway",
                        type=DeviceType.ROUTER,
                        position={"x": 280, "y": 200},
                        interfaces=[
                            InterfaceConfig(name="eth0", ip_address="192.168.1.1", mac_address="00:AA:11:22:33:01"),
                            InterfaceConfig(name="eth1", ip_address="198.51.100.1", mac_address="00:AA:11:22:33:02")
                        ],
                        nat_enabled=True
                    ),
                    DeviceConfig(
                        id="dns_server",
                        label="Public DNS (8.8.8.8)",
                        type=DeviceType.DNS_SERVER,
                        position={"x": 480, "y": 80},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="8.8.8.8", mac_address="00:AA:11:22:33:88")],
                        open_ports=[53]
                    ),
                    DeviceConfig(
                        id="web_server",
                        label="Google Web Server",
                        type=DeviceType.SERVER,
                        position={"x": 680, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="142.250.190.46", mac_address="00:AA:11:22:33:EE")],
                        open_ports=[80, 443]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="client", target_id="gateway", medium=LinkMedium.ETHERNET, latency_ms=1.0),
                    LinkConfig(id="l2", source_id="gateway", target_id="dns_server", medium=LinkMedium.WAN, latency_ms=12.0),
                    LinkConfig(id="l3", source_id="gateway", target_id="web_server", medium=LinkMedium.WAN, latency_ms=15.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "client", "action": "Browser checks HSTS, internal DNS cache, and OS hosts file."},
                {"step": 2, "actor": "client", "action": "ARP query sent to find Default Gateway's MAC address (00:AA:11:22:33:01)."},
                {"step": 3, "actor": "client", "action": "DNS query sent to 8.8.8.8 requesting A record for google.com."},
                {"step": 4, "actor": "dns_server", "action": "DNS returns IP 142.250.190.46."},
                {"step": 5, "actor": "client", "action": "TCP 3-Way Handshake initiated (SYN -> SYN-ACK -> ACK) with 142.250.190.46:443."},
                {"step": 6, "actor": "client", "action": "TLS 1.3 cryptographic handshake negotiates session keys."},
                {"step": 7, "actor": "client", "action": "HTTP GET / sent; server returns 200 OK with HTML document."}
            ],
            "explanation": "Loading a website requires tight collaboration across all 5 layers: Application (DNS, HTTP/TLS), Transport (UDP for DNS, TCP for HTTP), Network (IPv4 addressing & routing), Data Link (Ethernet framing & ARP), and Physical (fiber/copper transmission)."
        },

        # SCENARIO 4: Device Joining Wi-Fi (DHCP DORA)
        {
            "id": "scenario-dhcp-joining",
            "category": "Network Infrastructure",
            "title": "A New Device Joining a Wi-Fi Network (DHCP DORA)",
            "difficulty": "Beginner",
            "summary": "Step-by-step automatic IP, Subnet Mask, Gateway, and DNS allocation via DHCP Discover, Offer, Request, and ACK.",
            "core_concept": "DHCP DORA Sequence & Broadcast Messaging",
            "key_question": "When Snigdha's phone connects to Wi-Fi with no IP address, how can it communicate over IP before it has an IP?",
            "topology": TopologyConfig(
                id="topo-dhcp",
                name="DHCP DORA Network",
                devices=[
                    DeviceConfig(
                        id="phone",
                        label="Snigdha's Smartphone",
                        type=DeviceType.MOBILE,
                        position={"x": 100, "y": 200},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="0.0.0.0", mac_address="F0:D5:BF:11:22:33")]
                    ),
                    DeviceConfig(
                        id="ap_router",
                        label="Wi-Fi Router & DHCP Server",
                        type=DeviceType.ROUTER,
                        position={"x": 500, "y": 200},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="192.168.1.1", mac_address="00:14:D1:AA:BB:CC")],
                        services=["DHCP"]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="phone", target_id="ap_router", medium=LinkMedium.WIFI, latency_ms=3.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "phone", "action": "DHCP DISCOVER broadcast from 0.0.0.0 to 255.255.255.255 (UDP port 67)."},
                {"step": 2, "actor": "ap_router", "action": "DHCP OFFER: Router reserves 192.168.1.105 and offers gateway 192.168.1.1, DNS 8.8.8.8."},
                {"step": 3, "actor": "phone", "action": "DHCP REQUEST: Phone formally broadcasts acceptance of 192.168.1.105."},
                {"step": 4, "actor": "ap_router", "action": "DHCP ACK: Router commits lease and confirms configuration. Phone configures interface."}
            ],
            "explanation": "A device without an IP uses 0.0.0.0 as source and 255.255.255.255 (limited broadcast) as destination at the IP layer, and FF:FF:FF:FF:FF:FF at the Ethernet layer. Once the DHCP ACK arrives, the host applies the IP address, subnet mask, default gateway, and DNS servers to its network adapter."
        },

        # SCENARIO 5: WhatsApp Message Delivery & Offline Queueing
        {
            "id": "scenario-whatsapp-delivery",
            "category": "Real Applications",
            "title": "WhatsApp Message Delivery & Offline Store-and-Forward",
            "difficulty": "Intermediate",
            "summary": "How messaging platforms achieve end-to-end delivery: single tick (sent to server), double tick (delivered to phone), and offline store-and-forward queueing.",
            "core_concept": "Store-and-Forward Messaging & Long-Lived WebSocket/TCP Connections",
            "key_question": "Where does Snigdha's message live when Shubhanshu's phone is switched off or in airplane mode?",
            "topology": TopologyConfig(
                id="topo-whatsapp",
                name="WhatsApp Architecture",
                devices=[
                    DeviceConfig(
                        id="snigdha_phone",
                        label="Snigdha's Phone (Sender)",
                        type=DeviceType.MOBILE,
                        position={"x": 80, "y": 200},
                        interfaces=[InterfaceConfig(name="cell0", ip_address="10.42.1.8", mac_address="AA:BB:CC:11:22:33")]
                    ),
                    DeviceConfig(
                        id="wa_server",
                        label="WhatsApp Edge & Queue Server",
                        type=DeviceType.SERVER,
                        position={"x": 380, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="157.240.22.53", mac_address="00:1C:73:AA:BB:CC")],
                        open_ports=[443, 5222]
                    ),
                    DeviceConfig(
                        id="shubhanshu_phone",
                        label="Shubhanshu's Phone (Receiver)",
                        type=DeviceType.MOBILE,
                        position={"x": 680, "y": 200},
                        interfaces=[InterfaceConfig(name="cell0", ip_address="10.88.4.19", mac_address="DD:EE:FF:44:55:66")]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="snigdha_phone", target_id="wa_server", medium=LinkMedium.WAN, latency_ms=30.0),
                    LinkConfig(id="l2", source_id="wa_server", target_id="shubhanshu_phone", medium=LinkMedium.WAN, latency_ms=35.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "snigdha_phone", "action": "Snigdha sends E2E encrypted message to WhatsApp server over persistent TLS connection."},
                {"step": 2, "actor": "wa_server", "action": "Server stores message in transient database and sends 'Single Tick' receipt back to Snigdha."},
                {"step": 3, "actor": "wa_server", "action": "Shubhanshu is currently offline (no active socket). Message remains safely persisted in server queue."},
                {"step": 4, "actor": "shubhanshu_phone", "action": "Shubhanshu connects to cellular network; APNs/FCM push wakes Shubhanshu's phone; Shubhanshu establishes TLS connection."},
                {"step": 5, "actor": "wa_server", "action": "Server flushes queued messages to Shubhanshu's phone and receives delivery ACK."},
                {"step": 6, "actor": "wa_server", "action": "Server sends 'Double Tick' delivery receipt to Snigdha's active session."}
            ],
            "explanation": "Real-time chat platforms do not send peer-to-peer packets directly between phones. All traffic transits message broker servers (e.g. Erlang/XMPP/MQTT clusters) using store-and-forward semantics. Messages are persisted until the recipient's phone establishes an active TCP connection and acknowledges receipt."
        },

        # SCENARIO 6: Video Calling (WebRTC vs File Download)
        {
            "id": "scenario-webrtc-videocall",
            "category": "Real Applications",
            "title": "Video Calling (WebRTC / UDP) vs File Download (TCP)",
            "difficulty": "Intermediate",
            "summary": "Why video calls prioritize real-time low latency over 100% packet reliability, while file downloads require byte-perfect TCP retransmission.",
            "core_concept": "UDP vs TCP Trade-Offs: Latency vs Reliability",
            "key_question": "Why does a 1% packet loss cause a slight video glitch in Parv and Snigdha's call, but in a file download causes the transfer speed to plummet?",
            "topology": TopologyConfig(
                id="topo-webrtc",
                name="WebRTC Media Flow",
                devices=[
                    DeviceConfig(
                        id="user1",
                        label="Parv's Laptop (Caller)",
                        type=DeviceType.LAPTOP,
                        position={"x": 100, "y": 200},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="192.168.1.30", mac_address="00:11:22:33:44:55")]
                    ),
                    DeviceConfig(
                        id="stun_turn",
                        label="STUN/TURN Relay Server",
                        type=DeviceType.SERVER,
                        position={"x": 400, "y": 100},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="34.102.136.180", mac_address="00:22:33:44:55:66")],
                        open_ports=[3478]
                    ),
                    DeviceConfig(
                        id="user2",
                        label="Snigdha's Phone (Callee)",
                        type=DeviceType.MOBILE,
                        position={"x": 700, "y": 200},
                        interfaces=[InterfaceConfig(name="wlan0", ip_address="192.168.0.45", mac_address="00:33:44:55:66:77")]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="user1", target_id="user2", medium=LinkMedium.WAN, latency_ms=45.0, loss_rate=0.03),
                    LinkConfig(id="l2", source_id="user1", target_id="stun_turn", medium=LinkMedium.WAN, latency_ms=25.0),
                    LinkConfig(id="l3", source_id="user2", target_id="stun_turn", medium=LinkMedium.WAN, latency_ms=25.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "user1", "action": "Signaling server exchanges SDP (Session Description Protocol) offer/answer between Parv and Snigdha over TCP."},
                {"step": 2, "actor": "user1", "action": "STUN server resolves public Reflexive IP/port for NAT hole punching."},
                {"step": 3, "actor": "user1", "action": "Direct P2P UDP media stream (RTP/SRTP) begins between Parv and Snigdha."},
                {"step": 4, "actor": "user1", "action": "Packet 42 is dropped due to 3% link jitter. Snigdha's video decoder interpolates missing macroblock and continues without freezing."},
                {"step": 5, "actor": "user1", "action": "If TCP were used, the entire video stream would pause waiting for Packet 42 retransmission (Head-of-Line Blocking)."}
            ],
            "explanation": "Human conversation cannot tolerate latency over 200ms. In video calling, an old packet that arrives 300ms late is useless. WebRTC therefore utilizes UDP (via RTP/SRTP) to deliver media frames immediately, accepting slight packet loss rather than stalling for retransmissions."
        },

        # SCENARIO 7: IPv4 MTU Mismatch & Fragmentation
        {
            "id": "scenario-mtu-fragmentation",
            "category": "Advanced Networking",
            "title": "IPv4 MTU Mismatch & Packet Fragmentation",
            "difficulty": "Advanced",
            "summary": "Observe how routers divide a large 2500-byte packet across a constrained 1000-byte WAN link and reassemble it at the destination.",
            "core_concept": "IPv4 Fragmentation, 8-Byte Block Alignment, and MF/DF Flags",
            "key_question": "Why must IPv4 fragment offsets always be multiples of 8 bytes?",
            "topology": TopologyConfig(
                id="topo-fragmentation",
                name="MTU Bottleneck Topology",
                devices=[
                    DeviceConfig(
                        id="src_host",
                        label="Source Workstation (MTU 1500)",
                        type=DeviceType.DESKTOP,
                        position={"x": 100, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="10.0.1.10", mac_address="00:01:02:03:04:05")]
                    ),
                    DeviceConfig(
                        id="router1",
                        label="Gateway Router R1",
                        type=DeviceType.ROUTER,
                        position={"x": 380, "y": 200},
                        interfaces=[
                            InterfaceConfig(name="eth0", ip_address="10.0.1.1", mac_address="00:01:02:03:04:01"),
                            InterfaceConfig(name="wan0", ip_address="172.16.0.1", mac_address="00:01:02:03:04:02")
                        ]
                    ),
                    DeviceConfig(
                        id="dst_server",
                        label="Destination Database Server",
                        type=DeviceType.SERVER,
                        position={"x": 680, "y": 200},
                        interfaces=[InterfaceConfig(name="eth0", ip_address="172.16.0.2", mac_address="00:01:02:03:04:99")]
                    )
                ],
                links=[
                    LinkConfig(id="l1", source_id="src_host", target_id="router1", medium=LinkMedium.ETHERNET, mtu_bytes=1500, latency_ms=2.0),
                    LinkConfig(id="l2", source_id="router1", target_id="dst_server", medium=LinkMedium.WAN, mtu_bytes=800, latency_ms=20.0)
                ]
            ),
            "walkthrough": [
                {"step": 1, "actor": "src_host", "action": "Sends a 2000-byte packet. Link 1 has MTU 1500, so packet arrives at Router R1 intact."},
                {"step": 2, "actor": "router1", "action": "Next link has MTU 800 bytes. Available payload = 800 - 20 (IP Header) = 780 bytes."},
                {"step": 3, "actor": "router1", "action": "780 is rounded down to nearest multiple of 8: (780 // 8) * 8 = 776 bytes."},
                {"step": 4, "actor": "router1", "action": "Fragment 1: 776 bytes payload, Offset = 0, MF = 1."},
                {"step": 5, "actor": "router1", "action": "Fragment 2: 776 bytes payload, Offset = 97 (776 / 8), MF = 1."},
                {"step": 6, "actor": "router1", "action": "Fragment 3: 428 bytes payload, Offset = 194 (1552 / 8), MF = 0 (last fragment)."},
                {"step": 7, "actor": "dst_server", "action": "Destination receives all 3 fragments matching Identification, reassembles payload, and delivers to app."}
            ],
            "explanation": "Because the IPv4 Fragment Offset field is only 13 bits long but must reference byte positions up to 65,535, it measures offsets in units of 8-byte blocks (2^3 = 8). Intermediate routers slice fragments, but reassembly happens ONLY at the final destination host."
        }
    ]
