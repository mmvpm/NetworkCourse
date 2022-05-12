from router import Router

class Network:

    def __init__(self, routers: list[Router]):
        self.routers = routers

    def sync(self, verbose = True):
        step = 0
        has_changes = True
        while has_changes:
            step += 1
            has_changes = False
            for from_router in self.routers:
                for to_router in self.routers:
                    if from_router.name == to_router.name:
                        continue
                    for next_hop_router_name in from_router.neighbors:
                        has_changes |= from_router.update_dv_with(
                            to_router.name,
                            1 + to_router.dv_or_inf(next_hop_router_name),
                            next_hop_router_name
                        )
                if verbose:
                    print(f'Simulation step {step} of router {from_router.name}:')
                    from_router.print_results()
                    print()
        if verbose:
            for router in self.routers:
                print(f'Final state of router {router.name}:')
                router.print_results()
                print()
