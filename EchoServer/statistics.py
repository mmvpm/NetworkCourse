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

    def get_stats(self):
        return (
            self.rtt_min,
            self.rtt_max,
            0 if self.response_count == 0 else self.rtt_sum / self.response_count,
            0 if self.total_count == 0 else self.no_response_count / self.total_count * 100
        )
