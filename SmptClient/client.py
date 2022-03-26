import ssl
import base64
import socket
import argparse

from util import *
from logger import Logger

logger = Logger()

class SMPTClient:

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = ssl.wrap_socket(self.socket, ssl_version=ssl.PROTOCOL_SSLv23)
        self.socket.connect((host, port))

    def __del__(self):
        self.socket.close()

    def send_bytes(self, raw_message = None, has_response = True, verbose = True):
        if raw_message is not None:
            if verbose:
                logger.info(f'Request: {raw_message}')
            self.socket.send(raw_message)
        if has_response:
            response = read_from_socket(self.socket)
            if verbose:
                logger.info(f'Response: {response.strip()}')
            return response
        return None

    def send_string(self, message = None, has_response = True, verbose = True):
        if message is not None:
            raw_message = bytes(message, encoding='utf-8')
        else:
            raw_message = None
        self.send_bytes(raw_message, has_response, verbose)

    def first_response(self):
        self.send_string()

    def helo(self, mail_from: str):
        self.send_string(f'HELO {mail_from.split("@")[0]}\r\n')

    def login(self, mail_from, password):
        credentials = ('\x00' + mail_from + '\x00' + password).encode()
        auth_raw_message = 'AUTH PLAIN '.encode() + base64.b64encode(credentials) + '\r\n'.encode()
        self.send_bytes(auth_raw_message)

    def send_headers(self, mail_from, mail_to, subject, content_type, extra_headers = []):
        self.send_string(f'MAIL FROM: {mail_from}\r\n')
        self.send_string(f'RCPT TO: {mail_to}\r\n')
        self.send_string('DATA\r\n')
        self.send_string(
            f'From: {mail_from}\r\n'
            f'To: {mail_to}\r\n'
            f'Subject: {subject}\r\n'
            f'Content-Type: {content_type}\r\n',
            has_response=False
        )
        for header in extra_headers:
            self.send_string(header + '\r\n', has_response=False)

    def send_text_content(self, content):
        self.send_string(f'{content}\r\n', has_response=False)
        self.send_string('.\r\n')

    def send_image_content(self, content):
        self.send_bytes(content + '\r\n'.encode(), has_response=False, verbose=False)
        self.send_string('.\r\n')

    def quit(self):
        self.send_string('QUIT\r\n')

    def run(self, mail_from, mail_from_password, mail_to, subject, content_type, content, extra_headers = []):
        self.first_response()
        self.helo(mail_from)
        self.login(mail_from, mail_from_password)
        self.send_headers(mail_from, mail_to, subject, content_type, extra_headers)
        if len(extra_headers) == 0:
            self.send_text_content(content)
        else:
            self.send_image_content(content)
        self.quit()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', const=1, type=str, default='smtp.mail.ru')
    parser.add_argument('port', nargs='?', const=1, type=int, default=465)
    parser.add_argument('credentials_filename', nargs='?', const=1, type=str, default='auth.txt')
    parser.add_argument('mail_to', nargs='?', const=1, type=str, default='stroganov.n.36@gmail.com')
    parser.add_argument('subject', nargs='?', const=1, type=str, default='Sample subject')
    parser.add_argument('message_filename', nargs='?', const=1, type=str, default='message.html')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    mail_from, mail_from_password = read_from_file(args.credentials_filename).split()[:2]

    extra_headers = []
    content = read_from_file(args.message_filename)

    extension = args.message_filename.split('.')[-1]
    if extension == 'html':
        content_type = 'text/html'
    elif extension == 'txt':
        content_type = 'text/plain'
    else:
        content_type = f'image/{extension}; name={args.message_filename}'
        content = read_from_binary_file(args.message_filename)
        extra_headers = [ 'Content-Transfer-Encoding: base64' ]

    smpt_client = SMPTClient(args.host, args.port)
    smpt_client.run(mail_from, mail_from_password, args.mail_to, args.subject, content_type, content, extra_headers)
