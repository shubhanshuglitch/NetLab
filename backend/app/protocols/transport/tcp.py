from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from pydantic import BaseModel
from backend.app.schemas.packets import TransportHeader, TCPFlags


class TCPState(str, Enum):
    CLOSED = "CLOSED"
    LISTEN = "LISTEN"
    SYN_SENT = "SYN_SENT"
    SYN_RECEIVED = "SYN_RECEIVED"
    ESTABLISHED = "ESTABLISHED"
    FIN_WAIT_1 = "FIN_WAIT_1"
    FIN_WAIT_2 = "FIN_WAIT_2"
    CLOSE_WAIT = "CLOSE_WAIT"
    LAST_ACK = "LAST_ACK"
    TIME_WAIT = "TIME_WAIT"


class CongestionState(str, Enum):
    SLOW_START = "SLOW_START"
    CONGESTION_AVOIDANCE = "CONGESTION_AVOIDANCE"
    FAST_RECOVERY = "FAST_RECOVERY"


class TCPConnection:
    """
    Simulates a full RFC 793 / RFC 5681 TCP Connection State Machine with
    Congestion Control (Tahoe / Reno).
    """
    def __init__(
        self,
        src_ip: str,
        src_port: int,
        dst_ip: str,
        dst_port: int,
        initial_seq: int = 1000,
        algorithm: str = "Reno"
    ):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.algorithm = algorithm  # "Tahoe" or "Reno"
        
        # State
        self.state = TCPState.CLOSED
        self.seq_num = initial_seq
        self.ack_num = 0
        self.peer_seq_num = 0
        
        # Flow Control
        self.rwnd = 65535  # Receiver advertised window
        self.send_window = 65535
        
        # Congestion Control (units in MSS: 1 MSS = 1 packet)
        self.cwnd = 1.0  # Initial Congestion Window
        self.ssthresh = 16.0  # Slow Start Threshold
        self.cong_state = CongestionState.SLOW_START
        self.duplicate_acks = 0
        self.rtt_history: List[float] = []
        self.cwnd_history: List[Dict[str, Any]] = [{"step": 0, "cwnd": 1.0, "ssthresh": 16.0, "state": self.cong_state}]

    def create_syn_packet(self) -> TransportHeader:
        self.state = TCPState.SYN_SENT
        header = TransportHeader(
            protocol="TCP",
            src_port=self.src_port,
            dst_port=self.dst_port,
            seq_num=self.seq_num,
            ack_num=0,
            flags=TCPFlags(syn=True),
            window_size=self.rwnd
        )
        self.seq_num += 1  # SYN consumes 1 sequence number
        return header

    def receive_syn_ack(self, peer_seq: int, ack_num: int) -> TransportHeader:
        self.peer_seq_num = peer_seq
        self.ack_num = peer_seq + 1  # ACK next byte
        self.state = TCPState.ESTABLISHED
        header = TransportHeader(
            protocol="TCP",
            src_port=self.src_port,
            dst_port=self.dst_port,
            seq_num=self.seq_num,
            ack_num=self.ack_num,
            flags=TCPFlags(ack=True),
            window_size=self.rwnd
        )
        return header

    def on_ack_received(self, ack_num: int, is_duplicate: bool = False):
        """Updates Congestion Window according to Tahoe / Reno rules."""
        if not is_duplicate:
            self.duplicate_acks = 0
            if self.cwnd < self.ssthresh:
                # Slow Start: cwnd grows exponentially (1 MSS per ACK)
                self.cong_state = CongestionState.SLOW_START
                self.cwnd += 1.0
            else:
                # Congestion Avoidance: cwnd grows linearly (~1 MSS per RTT)
                self.cong_state = CongestionState.CONGESTION_AVOIDANCE
                self.cwnd += (1.0 / int(self.cwnd))

            if self.cong_state == CongestionState.FAST_RECOVERY:
                self.cong_state = CongestionState.CONGESTION_AVOIDANCE
                self.cwnd = self.ssthresh
        else:
            self.duplicate_acks += 1
            if self.duplicate_acks == 3:
                # 3 Duplicate ACKs -> Fast Retransmit
                self.ssthresh = max(self.cwnd / 2.0, 2.0)
                if self.algorithm == "Tahoe":
                    self.cwnd = 1.0
                    self.cong_state = CongestionState.SLOW_START
                else:  # Reno
                    self.cwnd = self.ssthresh + 3.0
                    self.cong_state = CongestionState.FAST_RECOVERY
            elif self.duplicate_acks > 3 and self.cong_state == CongestionState.FAST_RECOVERY:
                # Fast Recovery window inflation
                self.cwnd += 1.0

        self.cwnd_history.append({
            "step": len(self.cwnd_history),
            "cwnd": round(self.cwnd, 2),
            "ssthresh": round(self.ssthresh, 2),
            "state": self.cong_state,
            "duplicate_acks": self.duplicate_acks
        })

    def on_timeout(self):
        """Handles Retransmission Timeout (RTO) in Tahoe & Reno."""
        self.ssthresh = max(self.cwnd / 2.0, 2.0)
        self.cwnd = 1.0
        self.cong_state = CongestionState.SLOW_START
        self.duplicate_acks = 0
        self.cwnd_history.append({
            "step": len(self.cwnd_history),
            "cwnd": 1.0,
            "ssthresh": round(self.ssthresh, 2),
            "state": "TIMEOUT",
            "duplicate_acks": 0
        })

    def create_data_packet(self, payload_len: int) -> TransportHeader:
        header = TransportHeader(
            protocol="TCP",
            src_port=self.src_port,
            dst_port=self.dst_port,
            seq_num=self.seq_num,
            ack_num=self.ack_num,
            flags=TCPFlags(ack=True, psh=True),
            window_size=self.rwnd
        )
        self.seq_num += payload_len
        return header

    def create_fin_packet(self) -> TransportHeader:
        self.state = TCPState.FIN_WAIT_1
        header = TransportHeader(
            protocol="TCP",
            src_port=self.src_port,
            dst_port=self.dst_port,
            seq_num=self.seq_num,
            ack_num=self.ack_num,
            flags=TCPFlags(fin=True, ack=True),
            window_size=self.rwnd
        )
        self.seq_num += 1
        return header

