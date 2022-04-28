from enum import Enum

class PingResponse(Enum):
    SUCCESS = 0
    TIMEOUT = 1
    UNKNOWN_HOST = 2
    UNREACHABLE_HOST = 3
    UNREACHABLE_NETWORK = 4
    UNKNOWN_ERROR = 4

    @staticmethod
    def from_error_code(code: int) -> "PingResponse":
        '''For ICMP with type 3.'''
        if code == 0:
            return PingResponse.UNREACHABLE_NETWORK
        if code == 1:
            return PingResponse.UNREACHABLE_HOST
        return PingResponse.UNKNOWN_ERROR
