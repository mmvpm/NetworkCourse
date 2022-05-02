class Statistics:

    def __init__(self):
        self.rtt_min = +10 ** 9
        self.rtt_max = -10 ** 9
        self.rtt_sum = 0
        self.total_count = 0
        self.response_count = 0
        self.no_response_count = 0

    def update_rtt(self, new_rtt):
        self.total_count += 1
        self.response_count += 1
        self.rtt_sum += new_rtt
        self.rtt_min = min(self.rtt_min, new_rtt)
        self.rtt_max = max(self.rtt_max, new_rtt)

    def update_missed(self):
        self.total_count += 1
        self.no_response_count += 1

    def print_stats(self, address):
        rtt_avg, missed = 0, 0
        if self.response_count > 0:
            rtt_avg = self.rtt_sum / self.response_count
        if self.total_count > 0:
            missed = self.no_response_count / self.total_count * 100
        print(f'''
Статистика Ping для {address}:
    Пакетов: отправлено = {self.total_count}, получено = {self.response_count}, потеряно = {self.no_response_count}
    ({int(missed)}% потерь)
Приблизительное время приема-передачи в мс:
    Минимальное = {int(self.rtt_min)} мсек, Максимальное = {int(self.rtt_max)} мсек, Среднее = {int(rtt_avg)} мсек
''')
