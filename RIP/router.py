class Router:

    INF = 10 ** 9

    def __init__(self, name: str, neighbors: list[str]):
        self.name = name
        self.neighbors = set(neighbors)
        self.dv = {
            neighbor: 1
            for neighbor in self.neighbors
        }
        self.next_hop = {
            neighbor: neighbor
            for neighbor in self.neighbors
        }

    def update_dv_with(self, key: str, new_value: int, next_hop: str):
        if new_value < Router.INF and (key not in self.dv or new_value < self.dv[key]):
            self.dv[key] = new_value
            self.next_hop[key] = next_hop
            return True
        return False

    def dv_or_inf(self, key):
        if key in self.dv:
            return self.dv[key]
        return Router.INF

    def print_results(self):
        print(f'{"[Source IP]":20} {"[Destination IP]":20} {"[Next Hop]":20} {"Metric":20}')
        for to_router_name in self.dv:
            distance = self.dv[to_router_name] if to_router_name in self.dv else 'inf'
            print(f'{self.name:20} {to_router_name:20} {self.next_hop[to_router_name]:20} {str(distance):20}')
