from enum import Enum

class TracerouteResponse(Enum):
    SUCCESS = 0
    TIMEOUT = 1
    UNKNOWN_HOST = 2
    UNREACHABLE_HOST = 3
    UNREACHABLE_NETWORK = 4
    EXPIREDTTL = 5
    UNKNOWN_ERROR = 6

    @staticmethod
    def from_error_code(code: int) -> "TracerouteResponse":
        '''For ICMP with type 3.'''
        if code == 0:
            return TracerouteResponse.UNREACHABLE_NETWORK
        if code == 1:
            return TracerouteResponse.UNREACHABLE_HOST
        return TracerouteResponse.UNKNOWN_ERROR
