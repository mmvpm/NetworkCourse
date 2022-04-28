import struct
from util import *
from checksum import *

class ICMP:

    ECHO_REQUEST_TYPE = 8
    ECHO_REQUEST_CODE = 0

    ECHO_REPLY_TYPE = 0
    ECHO_REPLY_CODE = 0

    HEADER_SIZE = 4
    STRUCT_FORMAT = 'BBH' # [uint8, uint8, uint16]
    IP_HEADER_SIZE = 20

    def __init__(self, type: int, code: int, checksum: int, data: "ICMPData"):
        self.type = type
        self.code = code
        self.checksum = checksum
        self.data = data

    @staticmethod
    def build_header(type: int, code: int, checksum: int) -> bytes:
        return struct.pack(ICMP.STRUCT_FORMAT, type, code, checksum)

    @staticmethod
    def construct(type: int, code: int, data: "ICMPData") -> "ICMP":
        header_without_checksum = ICMP.build_header(type, code, 0)
        checksum = checksum_compute(header_without_checksum + data.to_bytes())
        return ICMP(type, code, checksum, data)

    @staticmethod
    def construct_echo_request(id: int, seq: int, time_ms: int) -> "ICMP":
        echo_data = EchoData.construct(id, seq, time_ms)
        return ICMP.construct(ICMP.ECHO_REQUEST_TYPE, ICMP.ECHO_REQUEST_CODE, echo_data)

    @staticmethod
    def parse_header(header: bytes) -> tuple:
        return struct.unpack(ICMP.STRUCT_FORMAT, header)
    
    @staticmethod
    def parse_data(type: int, data: bytes) -> "ICMPData":
        if type == 0 or type == 8:
            return EchoData.from_bytes(data)
        if type == 3:
            return ErrorData.from_bytes(data)
        return None

    @staticmethod
    def parse_packet(ip_packet: bytes) -> "ICMP":
        _, icmp_part = split_bytes(ip_packet, ICMP.IP_HEADER_SIZE)
        if not checksum_verify(icmp_part):
            print('Checksum verification failed')
            return None
        header_bytes, data_bytes = split_bytes(icmp_part, ICMP.HEADER_SIZE)
        type, code, checksum = ICMP.parse_header(header_bytes)
        data = ICMP.parse_data(type, data_bytes)
        return ICMP(type, code, checksum, data)

    def to_bytes(self) -> bytes:
        header = self.build_header(self.type, self.code, self.checksum)
        return header + self.data.to_bytes()


class ICMPData:

    @staticmethod
    def from_bytes(raw_data: bytes) -> "ICMPData":
        pass

    def to_bytes(self) -> bytes:
        pass


class EchoData(ICMPData):
    '''ICMPData with type 0 or 8: Echo request or reply.'''

    HEADER_SIZE = 4
    STRUCT_FORMAT = 'HH' # [uint16, uint16]

    def __init__(self, id: int, seq: int, data: bytes):
        self.id = id
        self.seq = seq
        self.data = data

    @staticmethod
    def construct(id: int, seq: int, time_ms: int) -> "EchoData":
        data = time_ms.to_bytes(8, byteorder = 'big')
        return EchoData(id, seq, data)

    @staticmethod
    def from_bytes(raw_data: bytes) -> "EchoData":
        header, data = split_bytes(raw_data, EchoData.HEADER_SIZE)
        id, seq = struct.unpack(EchoData.STRUCT_FORMAT, header)
        return EchoData(id, seq, data)

    def to_bytes(self) -> bytes:
        header = struct.pack(EchoData.STRUCT_FORMAT, self.id, self.seq)
        return header + self.data


class ErrorData(ICMPData):
    '''ICMPData with type 3: The addressee is unavailable.'''

    HEADER_SIZE = 4
    STRUCT_FORMAT = 'HH' # unused

    def __init__(self, icmp: ICMP, unused: bytes = None):
        self.icmp = icmp
        if unused is None:
            unused = struct.pack(ErrorData.STRUCT_FORMAT, 0, 0)
        self.unused = unused

    @staticmethod
    def from_bytes(raw_data: bytes) -> "ErrorData":
        unused, nested_ip_packet = split_bytes(raw_data, ErrorData.HEADER_SIZE)
        nested_icmp = ICMP.parse_packet(nested_ip_packet)
        return ErrorData(nested_icmp, unused)

    def to_bytes(self) -> bytes:
        return self.unused + self.icmp.to_bytes()
