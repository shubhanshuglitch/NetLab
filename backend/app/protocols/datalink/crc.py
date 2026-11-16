from typing import Dict, Any, List, Tuple
import binascii


def compute_crc32(data: bytes) -> str:
    """Computes standard IEEE 802.3 CRC-32 checksum as hex string."""
    crc = binascii.crc32(data) & 0xffffffff
    return f"0x{crc:08X}"


def verify_crc32(data: bytes, expected_crc_hex: str) -> bool:
    """Verifies data integrity against expected CRC-32."""
    actual_crc = compute_crc32(data)
    return actual_crc.lower() == expected_crc_hex.lower()


def crc_bitwise_division(data_bits: str, generator_bits: str) -> Dict[str, Any]:
    """
    Simulates step-by-step bitwise modulo-2 division for educational visualization.
    data_bits: string of '1's and '0's (e.g. '1101011011')
    generator_bits: string of '1's and '0's (e.g. '10011' for CRC-4)
    """
    g_len = len(generator_bits)
    appended_data = data_bits + "0" * (g_len - 1)
    current_bits = list(appended_data)
    
    steps: List[Dict[str, Any]] = []
    
    for i in range(len(data_bits)):
        if current_bits[i] == '1':
            step_desc = f"Bit {i} is '1': XOR current window with generator {generator_bits}"
            window_before = "".join(current_bits[i:i+g_len])
            for j in range(g_len):
                bit1 = int(current_bits[i + j])
                bit2 = int(generator_bits[j])
                current_bits[i + j] = str(bit1 ^ bit2)
            window_after = "".join(current_bits[i:i+g_len])
            steps.append({
                "step_index": len(steps) + 1,
                "bit_position": i,
                "action": "XOR",
                "window_before": window_before,
                "divisor": generator_bits,
                "window_after": window_after,
                "current_remainder": "".join(current_bits[-(g_len - 1):])
            })
        else:
            steps.append({
                "step_index": len(steps) + 1,
                "bit_position": i,
                "action": "SHIFT",
                "window_before": "".join(current_bits[i:i+g_len]),
                "divisor": "0" * g_len,
                "window_after": "".join(current_bits[i:i+g_len]),
                "current_remainder": "".join(current_bits[-(g_len - 1):])
            })

    remainder = "".join(current_bits[-(g_len - 1):])
    transmitted_codeword = data_bits + remainder

    return {
        "original_data_bits": data_bits,
        "generator_bits": generator_bits,
        "appended_data_bits": appended_data,
        "remainder_crc_bits": remainder,
        "transmitted_codeword": transmitted_codeword,
        "steps": steps[:20]  # cap steps for UI readability
    }


def inject_bit_error(data: bytes, bit_position: int = 0) -> bytes:
    """Flips a single bit in the bytearray to simulate physical medium corruption."""
    byte_array = bytearray(data)
    if not byte_array:
        return data
    byte_idx = (bit_position // 8) % len(byte_array)
    bit_offset = bit_position % 8
    byte_array[byte_idx] ^= (1 << bit_offset)
    return bytes(byte_array)

