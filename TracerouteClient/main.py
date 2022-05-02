import argparse
from client import TracerouteClient
from response import TracerouteResponse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', const=1, default='ya.ru', type=str)
    parser.add_argument('-n', nargs='?', const=1, default=3, type=int)
    parser.add_argument('--timeout', nargs='?', const=1, default=1000, type=int)
    parser.add_argument('--maxttl', nargs='?', const=1, default=247, type=int)
    args = parser.parse_args()
    return args.host, args.n, args.timeout, args.maxttl

if __name__ == '__main__':
    host, requests_count, timeout_ms, maxttl = parse_arguments()
    traceroute_client = TracerouteClient(timeout_ms)

    for ttl in range(1, maxttl + 1):
        address = None
        has_success = False

        print(f'{ttl:3}', end = '\t')
        for _ in range(requests_count):
            temp_address, response, rtt_ms = traceroute_client.traceroute(host, ttl=ttl)

            if response in [TracerouteResponse.SUCCESS, TracerouteResponse.EXPIREDTTL]:
                print(f'{str(rtt_ms) + "мс":<6}', end = '\t')
            elif response == TracerouteResponse.TIMEOUT:
                print(f'{"*":<6}', end = '\t')
            else:
                print(f'\nUnexpected error: {response.name}')

            if response == TracerouteResponse.SUCCESS:
                has_success = True

            if temp_address is not None:
                address = temp_address

        if address is not None:
            print(f'{traceroute_client.gethostbyaddr(address)}')
        else:
            print('Превышен интервал ожидания для запроса.')
        
        if has_success:
            break
