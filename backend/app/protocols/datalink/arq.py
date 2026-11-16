from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ARQEvent(BaseModel):
    step: int
    sender_window: List[int]
    receiver_window: List[int]
    action: str
    frame_sent: Optional[int] = None
    ack_received: Optional[int] = None
    is_dropped: bool = False
    is_corrupted: bool = False
    is_timeout: bool = False
    explanation: str


def simulate_stop_and_wait(total_frames: int = 5, drop_frames: Optional[List[int]] = None) -> Dict[str, Any]:
    """Simulates Stop-and-Wait ARQ with frame/ACK drops."""
    drop_frames = drop_frames or []
    events: List[ARQEvent] = []
    step = 1
    current_frame = 0
    retransmissions = 0

    while current_frame < total_frames and step <= 40:
        # Sender sends frame
        is_dropped = current_frame in drop_frames and step not in [e.step for e in events if e.is_dropped]
        if is_dropped:
            events.append(ARQEvent(
                step=step,
                sender_window=[current_frame],
                receiver_window=[current_frame],
                action=f"Frame {current_frame} sent but LOST in transit",
                frame_sent=current_frame,
                is_dropped=True,
                explanation=f"Frame {current_frame} was lost. In Stop-and-Wait, the sender waits for timer expiry before retransmission."
            ))
            step += 1
            # Timeout triggers retransmit
            events.append(ARQEvent(
                step=step,
                sender_window=[current_frame],
                receiver_window=[current_frame],
                action=f"Timer Expired! Retransmitting Frame {current_frame}",
                frame_sent=current_frame,
                is_timeout=True,
                explanation=f"Timer elapsed without ACK for Frame {current_frame}. Sender retransmits the unacknowledged frame."
            ))
            retransmissions += 1
            step += 1
            # Remove from drop_frames so it succeeds on retransmit
            drop_frames.remove(current_frame)

        # Successful transmission & ACK
        events.append(ARQEvent(
            step=step,
            sender_window=[current_frame],
            receiver_window=[current_frame + 1],
            action=f"Frame {current_frame} delivered -> ACK {current_frame + 1} received",
            frame_sent=current_frame,
            ack_received=current_frame + 1,
            explanation=f"Frame {current_frame} received successfully by receiver. Receiver returns ACK {current_frame + 1} requesting next frame."
        ))
        current_frame += 1
        step += 1

    return {
        "protocol": "Stop-and-Wait ARQ",
        "window_size": 1,
        "total_frames": total_frames,
        "retransmissions": retransmissions,
        "events": [e.model_dump() for e in events]
    }


def simulate_go_back_n(total_frames: int = 8, window_size: int = 4, drop_frame_index: Optional[int] = 2) -> Dict[str, Any]:
    """
    Simulates Go-Back-N ARQ.
    When a frame is dropped, subsequent frames sent in the window are discarded by the receiver,
    and the sender must go back and retransmit all unacknowledged frames from the lost frame onward.
    """
    events: List[ARQEvent] = []
    step = 1
    base = 0
    next_seq = 0
    retransmissions = 0
    dropped = False

    while base < total_frames and step <= 50:
        # Send up to window limit
        if next_seq < base + window_size and next_seq < total_frames:
            # Check if this frame is dropped
            if next_seq == drop_frame_index and not dropped:
                dropped = True
                events.append(ARQEvent(
                    step=step,
                    sender_window=list(range(base, min(base + window_size, total_frames))),
                    receiver_window=[base],
                    action=f"Frame {next_seq} sent but DROPPED by network",
                    frame_sent=next_seq,
                    is_dropped=True,
                    explanation=f"Frame {next_seq} was dropped. Receiver is still expecting frame {base}."
                ))
                next_seq += 1
                step += 1
                continue

            if dropped and next_seq > drop_frame_index and next_seq < base + window_size:
                # Frame arrives out of order -> Receiver discards it
                events.append(ARQEvent(
                    step=step,
                    sender_window=list(range(base, min(base + window_size, total_frames))),
                    receiver_window=[base],
                    action=f"Frame {next_seq} received out-of-order -> DISCARDED by receiver (ACK {base} resent)",
                    frame_sent=next_seq,
                    ack_received=base,
                    explanation=f"Go-Back-N does not buffer out-of-order frames. Since frame {base} is missing, frame {next_seq} is discarded."
                ))
                next_seq += 1
                step += 1
                continue

            events.append(ARQEvent(
                step=step,
                sender_window=list(range(base, min(base + window_size, total_frames))),
                receiver_window=[next_seq + 1],
                action=f"Frame {next_seq} sent and ACK {next_seq + 1} received",
                frame_sent=next_seq,
                ack_received=next_seq + 1,
                explanation=f"Frame {next_seq} received in order. Cumulative ACK {next_seq + 1} advances the sender window."
            ))
            base += 1
            next_seq += 1
            step += 1
        else:
            # Window exhausted or dropped frame causes timeout
            if dropped and base <= drop_frame_index:
                events.append(ARQEvent(
                    step=step,
                    sender_window=list(range(base, min(base + window_size, total_frames))),
                    receiver_window=[base],
                    action=f"Timeout expired for unacknowledged Frame {base}! Going back to {base}",
                    frame_sent=base,
                    is_timeout=True,
                    explanation=f"Sender timer for frame {base} expired. Go-Back-N resets next_seq to {base} and retransmits all frames in the window."
                ))
                retransmissions += (next_seq - base)
                next_seq = base
                drop_frame_index = -1  # Do not drop again
                step += 1
            else:
                base += 1
                step += 1

    return {
        "protocol": "Go-Back-N ARQ",
        "window_size": window_size,
        "total_frames": total_frames,
        "retransmissions": retransmissions,
        "events": [e.model_dump() for e in events]
    }


def simulate_selective_repeat(total_frames: int = 8, window_size: int = 4, drop_frame_index: Optional[int] = 2) -> Dict[str, Any]:
    """
    Simulates Selective Repeat ARQ.
    When a frame is dropped, the receiver buffers subsequent valid frames in its receive window,
    and only the missing frame is retransmitted.
    """
    events: List[ARQEvent] = []
    step = 1
    base = 0
    retransmissions = 0
    buffered_at_receiver: List[int] = []
    dropped_done = False

    # Simulate sending frames 0..window_size-1
    for frame_id in range(min(window_size, total_frames)):
        if frame_id == drop_frame_index and not dropped_done:
            dropped_done = True
            events.append(ARQEvent(
                step=step,
                sender_window=list(range(base, min(base + window_size, total_frames))),
                receiver_window=list(range(base, min(base + window_size, total_frames))),
                action=f"Frame {frame_id} sent but DROPPED",
                frame_sent=frame_id,
                is_dropped=True,
                explanation=f"Frame {frame_id} was lost in transit."
            ))
            step += 1
        else:
            buffered_at_receiver.append(frame_id)
            events.append(ARQEvent(
                step=step,
                sender_window=list(range(base, min(base + window_size, total_frames))),
                receiver_window=list(range(base, min(base + window_size, total_frames))),
                action=f"Frame {frame_id} received & BUFFERED -> Selective ACK {frame_id} returned",
                frame_sent=frame_id,
                ack_received=frame_id,
                explanation=f"Receiver buffers out-of-order frame {frame_id} and sends an individual Selective ACK for {frame_id}."
            ))
            step += 1

    # Retransmit ONLY dropped frame
    if drop_frame_index is not None and drop_frame_index < total_frames:
        retransmissions += 1
        events.append(ARQEvent(
            step=step,
            sender_window=[drop_frame_index],
            receiver_window=list(range(base, min(base + window_size, total_frames))),
            action=f"Timeout for Frame {drop_frame_index}! Sender retransmits ONLY Frame {drop_frame_index}",
            frame_sent=drop_frame_index,
            is_timeout=True,
            explanation=f"Unlike Go-Back-N, Selective Repeat does NOT retransmit frames already buffered by the receiver. Only frame {drop_frame_index} is resent."
        ))
        step += 1
        buffered_at_receiver.append(drop_frame_index)
        buffered_at_receiver.sort()
        base = max(buffered_at_receiver) + 1
        events.append(ARQEvent(
            step=step,
            sender_window=list(range(base, min(base + window_size, total_frames))),
            receiver_window=list(range(base, min(base + window_size, total_frames))),
            action=f"Frame {drop_frame_index} delivered! Receiver releases buffered frames to application, window slides to {base}",
            frame_sent=drop_frame_index,
            ack_received=drop_frame_index,
            explanation=f"The missing piece has arrived. Receiver delivers contiguous frames to application layer and slides its window forward."
        ))
        step += 1

    return {
        "protocol": "Selective Repeat ARQ",
        "window_size": window_size,
        "total_frames": total_frames,
        "retransmissions": retransmissions,
        "events": [e.model_dump() for e in events]
    }

