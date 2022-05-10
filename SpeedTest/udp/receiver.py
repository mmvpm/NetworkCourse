import socket
import datetime
import PySimpleGUI as sg

PACKET_SIZE = 1024

def create_udp_socket(host, port):
    receiver_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_udp_socket.settimeout(0.1)
    receiver_udp_socket.bind((host, port))
    return receiver_udp_socket

def create_tcp_socket(host, port):
    receiver_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_tcp_socket.bind((host, port))
    receiver_tcp_socket.listen(1)
    return receiver_tcp_socket

host, port = '127.0.0.1', 12321
receiver_udp_socket = create_udp_socket(host, port)
receiver_tcp_socket = create_tcp_socket(host, port)

layout = [
    [sg.Text('Введите IP', size=(30, 1)), sg.InputText(host)],
    [sg.Text('Введите порт', size=(30, 1)), sg.InputText(str(port))],
    [sg.Text('Пакетов получено:', size=(30, 1)), sg.Text(key='messages')],
    [sg.Text('Скорость передачи:', size=(30, 1)), sg.Text(key='speed')],
    [sg.Button('Начать получение данных')],
]

window = sg.Window('UDP Receiver', layout)

total_messages = 0
messages_counter = 0
first_message_ms = 0
last_recevied_ms = 1

while True:
    event, values = window.read(100)

    if event in (None, 'Exit'):
        break

    if event == 'Начать получение данных':
        messages_counter = 0
        first_message_ms = 0

        try:
            recv_tcp_socket, _ = receiver_tcp_socket.accept()
            total_messages = int(recv_tcp_socket.recv(PACKET_SIZE).decode())
        except Exception as e:
            print(f'Receiving the number of messages failed: {e}')
        finally:
            recv_tcp_socket.close()

        for i in range(total_messages):
            try:
                message, _ = receiver_udp_socket.recvfrom(PACKET_SIZE)
                message_time_ms, _ = message.decode().split()
                messages_counter += 1
                if first_message_ms == 0:
                    first_message_ms = int(message_time_ms)
            except socket.timeout:
                pass
        last_recevied_ms = round(datetime.datetime.now().timestamp() * 1000)

    try:
        new_host, new_port = values[0], int(values[1])
        if new_host != host or new_port != port:
            host, port = new_host, new_port
            receiver_udp_socket.close()
            receiver_tcp_socket.close()
            receiver_udp_socket = create_udp_socket(host, port)
            receiver_tcp_socket = create_tcp_socket(host, port)
    except:
        pass

    total_time_ms = last_recevied_ms - first_message_ms
    if total_time_ms > 0:
        speed = round(PACKET_SIZE * messages_counter / total_time_ms)
    window['speed'].Update(f'{speed} KB/s')
    window['messages'].Update(f'{messages_counter}/{total_messages}')

receiver_udp_socket.close()
receiver_tcp_socket.close()
