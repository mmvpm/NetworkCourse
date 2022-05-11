import PySimpleGUI as sg
from threading import Thread
from proxy import ProxySocket
from input_row import InputRow

class Window:

    BUTTON_ADD = 'Добавить правило'
    BUTTON_RUN = 'Запустить транслятор'

    def __init__(self):
        self.threads = []
        self.input_rows = [InputRow()]
        self.layout = self.make_layout()
        self.window = sg.Window('Port translator', self.layout)
        self.handlers = [
            getattr(Window, method_name)
            for method_name in dir(Window)
            if 'handler' in method_name
        ]

    @staticmethod
    def make_text(text: str, size = (19, 1)):
        return sg.Text(text, size, justification='center')

    @staticmethod
    def make_input(default_text, key = None, size = (22, 1)):
        return sg.InputText(default_text, size, key=key)

    @staticmethod
    def make_names_row():
        return [
            Window.make_text('Название'),
            Window.make_text('Внутренний IP'),
            Window.make_text('Внутренний порт'),
            Window.make_text('Внешний IP'),
            Window.make_text('Внешний порт')
        ]

    @staticmethod
    def make_input_row(input_row: InputRow):
        return [
            Window.make_input(input_row.name, f'name {input_row.rule_index}'),
            Window.make_input(input_row.internal_host, f'internal_host {input_row.rule_index}'),
            Window.make_input(input_row.internal_port, f'internal_port {input_row.rule_index}'),
            Window.make_input(input_row.external_host, f'external_host {input_row.rule_index}'),
            Window.make_input(input_row.external_port, f'external_port {input_row.rule_index}'),
        ]

    @staticmethod
    def make_buttons_row():
        return [
            sg.Button(Window.BUTTON_ADD),
            sg.Button(Window.BUTTON_RUN)
        ]
    
    def make_layout(self):
        return [
            Window.make_names_row(),
            *[Window.make_input_row(input_row)
             for input_row in self.input_rows
            ],
            Window.make_buttons_row()
        ]

    def update_input_rows(self, values):
        if values is None:
            return
        for key, value in values.items():
            if type(key) != str or ' ' not in key:
                continue
            value_name, index = key.split()
            index = int(index)
            is_changed = False
            if value_name == 'name':
                self.input_rows[index].name = value
            if value_name == 'internal_host':
                is_changed |= self.input_rows[index].internal_host != value
                self.input_rows[index].internal_host = value
            if value_name == 'internal_port':
                is_changed |= self.input_rows[index].internal_port != int(value)
                self.input_rows[index].internal_port = int(value)
            if value_name == 'external_host':
                is_changed |= self.input_rows[index].external_host != value
                self.input_rows[index].external_host = value
            if value_name == 'external_port':
                is_changed |= self.input_rows[index].external_port != int(value)
                self.input_rows[index].external_port = int(value)
            self.input_rows[index].is_applied &= not is_changed

    def exit_handler(self, event, _):
        if event in (None, 'Exit'):
            self.is_running = False

    def button_add_handler(self, event, _):
        if event == Window.BUTTON_ADD:
            self.input_rows.append(
                InputRow(rule_index=len(self.input_rows))
            )
            self.layout = self.make_layout()
            self.window.close()
            self.window = sg.Window('Port translator', self.layout)

    def button_run_handler(self, event, _):
        if event == Window.BUTTON_RUN:
            for input_row in self.input_rows:
                if not input_row.is_applied:
                    target = lambda: \
                        ProxySocket(
                            input_row.internal_host,
                            input_row.internal_port,
                            input_row.external_host,
                            input_row.external_port
                        )
                    self.threads.append(Thread(target=target))
                    self.threads[-1].start()
                    input_row.is_applied = True

    def run(self):
        self.is_running = True
        while self.is_running:
            event, values = self.window.read(100)
            self.update_input_rows(values)
            for handler in self.handlers:
                handler(self, event, values)
        for thread in self.threads:
            thread.join()
