import os
import socket
from util import get_current_ms
from ping_response import PingResponse
from icmp import ICMP, EchoData, ErrorData

class PingClient:

    def __init__(self, timeout_ms: int, ttl: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        self.socket.settimeout(timeout_ms / 1000)

    def __del__(self):
        self.socket.close()

    def ping(self, host: str, port = 1, seq: int = 0):
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            return host, PingResponse.UNKNOWN_HOST, 0

        packet_id = os.getpid() & 0xFFFF

        start_time_ms = get_current_ms()
        echo_packet = ICMP.construct_echo_request(packet_id, seq, start_time_ms)
        echo_packet_bytes = echo_packet.to_bytes()
        self.socket.sendto(echo_packet_bytes, (host, port))
        response_code = self.receive_ping_reply(packet_id, seq)
        end_time_ms = get_current_ms()

        return host, len(echo_packet_bytes), response_code, end_time_ms - start_time_ms

    def receive_ping_reply(self, expected_id: int, expected_seq: int) -> PingResponse:
        try:
            while True:
                ip_packet, _ = self.socket.recvfrom(1024)
                icmp_reply = ICMP.parse_packet(ip_packet)

                if isinstance(icmp_reply.data, EchoData):
                    echo_reply: EchoData = icmp_reply.data
                    if echo_reply.id == expected_id and echo_reply.seq == expected_seq:
                        return PingResponse.SUCCESS

                if isinstance(icmp_reply.data, ErrorData):
                    error_reply: ErrorData = icmp_reply.data
                    nested_echo: EchoData = error_reply.icmp.data
                    if nested_echo.id == expected_id and nested_echo.seq == expected_seq:
                        return PingResponse.from_error_code(icmp_reply.code)

        except socket.timeout:
            return PingResponse.TIMEOUT
