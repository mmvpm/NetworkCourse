import socket
import PySimpleGUI as sg
import scapy.all as scapy

HOME_IP = '192.168.1.86'
NETWORK_IP = '192.168.1.0'
HOME_MAC = '64-5D-86-86-5B-64'
HOME_HOST_NAME = socket.gethostbyaddr(HOME_IP)[0]
MASK = [255, 255, 255, 0]

def scan_network(ip):
    return [
        {
            'ip': i[1].psrc,
            'mac': i[1].hwsrc
        }
        for i in scapy.srp(
            scapy.Ether(dst='ff:ff:ff:ff:ff:ff') / scapy.ARP(pdst=ip),
            timeout = 1,
            verbose = False)[0]    
    ]

has_hello_input = False
clients = scan_network(f'{NETWORK_IP}/24')

layout = [
    [sg.ProgressBar(len(clients), orientation='h', size=(54, 20), key='progress_bar')],
    [sg.Output(size=(100, 20), font=('Consolas', 10))],
    [sg.Submit('Начать')]
]
window = sg.Window('LocalNetScanner', layout)

while True:
    event, values = window.read(timeout=100)

    if event in (None, 'Exit'):
        break

    if event == 'Начать':
        if not has_hello_input:
            print(f'{"IP адрес":30}{"MAC адрес":30}{"Имя хоста":30}')
            print('Этот компьютер:')
            print(f'{HOME_IP:30}{HOME_MAC:30}{HOME_HOST_NAME:30}')
            print('Локальная сеть:')
            has_hello_input = True

        progress_bar = window['progress_bar']
        for i, host in enumerate(clients):
            ip, mac_address = host['ip'], host['mac']
            if ip == HOME_IP:
                continue
            try:
                host_name = socket.gethostbyaddr(ip)[0]
            except Exception:
                host_name = 'Имя не найдено'
            print(f'{str(ip):30}{str(mac_address):30}{str(host_name):30}')
            progress_bar.UpdateBar(i + 1)

window.close()
