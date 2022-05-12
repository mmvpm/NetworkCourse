import json
from router import Router
from network import Network

if __name__ == '__main__':
    schema = json.load(open('network.json'))
    routers = [
        Router(router_name, schema[router_name])
        for router_name in schema
    ]
    network = Network(routers)
    network.sync()
