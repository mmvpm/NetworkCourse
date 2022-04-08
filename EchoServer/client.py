import socket
import datetime
from statistics import Statistics

def build_message(index, time):
    return f'Ping {index} {time}'

def parse_time(message):
    message = message.split()
    time_message = f'{message[2]} {message[3]}'
    return datetime.datetime.strptime(time_message, '%Y-%m-%d %H:%M:%S.%f')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.settimeout(1)

stats = Statistics()

for query_index in range(1, 11):
    time_now = datetime.datetime.now()
    message = build_message(query_index, time_now).encode()
    client_socket.sendto(message, ('127.0.0.1', 12321))

    try:
        response, _ = client_socket.recvfrom(1024)
        response = response.decode()
        print(response)

        time_now = datetime.datetime.now()
        time_response = parse_time(response)

        rtt_ms = (time_now - time_response).total_seconds() * 1000
        stats.update_rtt(rtt_ms)
    except:
        print(f'Request timed out\n')
        stats.update_missed()

    rtt_min, rtt_max, rtt_avg, missed = stats.get_stats()
    print(f'''
Статистика Ping для 127.0.0.1:
    Пакетов: отправлено = {stats.total_count}, получено = {stats.response_count}, потеряно = {stats.no_response_count}
    ({int(missed)}% потерь)
Приблизительное время приема-передачи в мс:
    Минимальное = {int(rtt_min)} мсек, Максимальное = {int(rtt_max)} мсек, Среднее = {int(rtt_avg)} мсек
''')
