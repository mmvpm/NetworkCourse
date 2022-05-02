import argparse
from time import sleep
from client import PingClient
from statistics import Statistics
from ping_response import PingResponse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', const=1, default='ya.ru', type=str)
    parser.add_argument('-n', nargs='?', const=1, default=10, type=int)
    parser.add_argument('--timeout', nargs='?', const=1, default=1000, type=int)
    parser.add_argument('--ttl', nargs='?', const=1, default=247, type=int)
    args = parser.parse_args()
    return args.host, args.n, args.timeout, args.ttl

if __name__ == '__main__':
    stats = Statistics()
    host, request_count, timeout_ms, ttl = parse_arguments()
    ping_client = PingClient(timeout_ms, ttl)

    for request_index in range(1, request_count + 1):
        address, packet_len, ping_response, rtt_ms = ping_client.ping(host, seq=request_index)

        if ping_response == PingResponse.SUCCESS:
            print(f'Ответ от {address}: число байт={packet_len} время={rtt_ms}мс TTL={ttl}')
            stats.update_rtt(rtt_ms)
        else:
            print(f'Unexpected error: {ping_response.name}')
            stats.update_missed()

        if rtt_ms < 1000:
            sleep((1000 - rtt_ms) / 1000)

    stats.print_stats(address)
