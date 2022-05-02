import os
import socket
from icmp import *
from util import get_current_ms
from response import TracerouteResponse

class TracerouteClient:

    def __init__(self, timeout_ms: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.socket.settimeout(timeout_ms / 1000)

    def __del__(self):
        self.socket.close()
    
    def gethostbyaddr(self, host):
        try:
            host = socket.gethostbyaddr(host)
            return f'{host[0]} {host[2]}'
        except:
            return host

    def traceroute(self, host: str, port = 1, ttl: int = 1):
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            return None, TracerouteResponse.UNKNOWN_HOST, 0

        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        packet_id = os.getpid() & 0xFFFF

        start_time_ms = get_current_ms()
        echo_packet = ICMP.construct_echo_request(packet_id, ttl, start_time_ms)
        echo_packet_bytes = echo_packet.to_bytes()
        self.socket.sendto(echo_packet_bytes, (host, port))
        address, response_code = self.receive_traceroute_reply(packet_id, ttl)
        end_time_ms = get_current_ms()

        return address, response_code, end_time_ms - start_time_ms

    def receive_traceroute_reply(self, expected_id: int, expected_seq: int):
        address = None
        try:
            while True:
                ip_packet, address = self.socket.recvfrom(1024)
                address = address[0]
                icmp_reply = ICMP.parse_packet(ip_packet)

                if isinstance(icmp_reply.data, EchoData):
                    echo_reply: EchoData = icmp_reply.data
                    if echo_reply.id == expected_id and echo_reply.seq == expected_seq:
                        return address, TracerouteResponse.SUCCESS

                if isinstance(icmp_reply.data, ErrorData):
                    error_reply: ErrorData = icmp_reply.data
                    nested_echo: EchoData = error_reply.icmp.data
                    if nested_echo.id == expected_id and nested_echo.seq == expected_seq:
                        return address, TracerouteResponse.from_error_code(icmp_reply.code)

                if isinstance(icmp_reply.data, ExpiredTTLData):
                    expired_tll_reply: ExpiredTTLData = icmp_reply.data
                    nested_echo: ExpiredTTLData = expired_tll_reply.icmp.data
                    if nested_echo.id == expected_id and nested_echo.seq == expected_seq:
                        return address, TracerouteResponse.EXPIREDTTL

        except socket.timeout:
            return address, TracerouteResponse.TIMEOUT
