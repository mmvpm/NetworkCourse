from dv import DistanceVector

class NodeInfo:

    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        dv: dict[str, int] = None,
        which_neighbor: dict[str, str]  = None
    ):
        self.name = name
        self.host = host
        self.port = port

        if dv is None:
            dv = {}
        if which_neighbor is None:
            which_neighbor = {}

        self.dv = DistanceVector(dv)
        self.which_neighbor = which_neighbor
