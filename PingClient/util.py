from time import time

def split_bytes(raw_bytes: bytes, split_index: int) -> tuple[bytes, bytes]:
    return raw_bytes[:split_index], raw_bytes[split_index:]

def get_current_ms() -> int:
    return int(time() * 1000)