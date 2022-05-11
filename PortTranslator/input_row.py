class InputRow:

    def __init__(
        self,
        name: str = None,
        internal_host: str = '127.0.0.1',
        internal_port: int = 10000,
        external_host: str = '',
        external_port: int = 80,
        rule_index: int = 0,
    ):
        self.name = name if name is not None else f'Правило #{rule_index + 1}'
        self.internal_host = internal_host
        self.internal_port = internal_port + rule_index
        self.external_host = external_host
        self.external_port = external_port
        self.rule_index = rule_index
        self.is_applied = False
