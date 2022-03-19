import datetime

class Logger:

    def __init__(self, print_to_console = True):
        self.print_to_console = print_to_console
        self.log_file = open('proxy-server.log', 'wt')

    def __del__(self):
        self.log_file.close()

    def info(self, message):
        now = datetime.datetime.now()
        log_message = f'[{now}] {message}\n'
        if self.print_to_console:
            print(log_message, end = '')
        self.log_file.write(log_message)
        self.log_file.flush()
