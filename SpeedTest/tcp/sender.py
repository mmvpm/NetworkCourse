import random
import socket
import datetime
import PySimpleGUI as sg

PACKET_SIZE = 1024

def build_random_message(length):
    return ''.join(
        chr(random.randint(33, 126))
        for _ in range(length)
    )

layout = [
    [sg.Text('Введите IP', size=(30, 1)), sg.InputText('127.0.0.1', key='host')],
    [sg.Text('Введите порт', size=(30, 1)), sg.InputText('12321', key='port')],
    [sg.Text('Введите число пакетов для отправки', size=(30, 1)), sg.InputText('5', key='messages')],
    [sg.Button('Отправить данные')],
]

window = sg.Window('TCP Sender', layout)

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    if event == 'Отправить данные':
        try:
            host, port = values['host'], int(values['port'])
            number_of_messages = int(values['messages'])
        except Exception as e:
            print(f'Parsing arguments failed: {e}')

        try:
            sender_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_tcp_socket.connect((host, port))
            sender_tcp_socket.sendall(bytes(str(number_of_messages), encoding='utf-8'))
            for i in range(number_of_messages):
                now = datetime.datetime.now()
                message = f'{int(now.timestamp() * 1000)} '
                message += build_random_message(PACKET_SIZE - len(message))
                sender_tcp_socket.sendall(message.encode())
        except Exception as e:
            print(f'Sending messages failed: {e}')
        finally:
            sender_tcp_socket.close()
