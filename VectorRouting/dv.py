class DistanceVector:

    INF = 10 ** 9

    def __init__(self, data: dict[str, int] = None):
        if data is None:
            data = {}
        self.data = data

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return DistanceVector.INF

    def __setitem__(self, key, value):
        if value < DistanceVector.INF:
            self.data[key] = value

    def __str__(self):
        return '{' + ', '.join(
            f"'{key}': {self.data[key]}"
            for key in sorted(self.data.keys())
        ) + '}'

    def update_item(self, key, value) -> bool:
        '''Returns True if there are changes.'''
        if value >= DistanceVector.INF:
            return False
        if key not in self.data or value < self.data[key]:
            self.data[key] = value
            return True
        return False

    def update_dv(self, other_data: dict[str, int]):
        other_data = {
            key: value
            for key, value in other_data.items()
            if value < DistanceVector.INF
        }
        self.data = other_data
