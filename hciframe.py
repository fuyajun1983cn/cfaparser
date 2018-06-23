
##Debug Switch
_COMMAND_DEBUG = False
_EVENT_DEBUG = False
_ACL_DEBUG = True


# private method
def type_str(type):
    if type == 0x01:
        return "HCI Command Packet"
    elif type == 0x02:
        return "HCI ACL Data Packet"
    elif type == 0x03:
        return "HCI Synchronous Data Packet"
    elif type == 4:
        return "HCI Event Packet"
    else:
        return "Invalid HCI Packet"


"""
A class for HCI Frame
"""
class HciFrame:

    __frame_count = 0

    def __init__(self, frame_no, size):
        self.frame_no = frame_no
        self.size = size
        type(self).__frame_count += 1

    def load_content(self, content):
        self.type = content[0]
        self.payload = content[1:]

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload

    def __repr__(self):
        return '([{0}]{1}, {2})'.format(self.frame_no, type_str(self.type), self.size)

    @classmethod
    def frame_count(cls):
        return cls.__frame_count



"""
A class for command packet

The HCI Command
Packet header is the first 3 octets of the packet.

2bytes 
OpCode(OpCode Command Field + OpCode Group Field) Parameter Total Length  

Parameter...


"""
class CommandPacket(HciFrame):

    def __init__(self, frame_no, content, size):
        super().__init__(frame_no, size)
        self.header = content[:3]
        self.payload = content[3:]

    def __init__(self, hci_frame):
        super().__init__(hci_frame.frame_no, hci_frame.size)
        self.header = hci_frame.payload[:3]
        self.payload = hci_frame.payload[3:]

    def getOpCode(self):
        return int.from_bytes(self.header[0:2], byteorder='little', signed=False)

    def getOGF(self):
        return self.header[1] >> 2

    #get parameter total length
    def get_payload_length(self):
        return self.header[2]

    def __repr__(self):
        if _COMMAND_DEBUG:
            return "Command Packet {}: OpCode: 0x{:04x}, OGF: 0x{:02x}, payload length: {}".format(
                self.frame_no, self.getOpCode(), self.getOGF(), self.get_payload_length())
        else:
            return ""


"""
A class for HCI event packets

Event Code(1 byte) + Parameter Total Length(1 byte)

"""
class EventPacket(HciFrame):

    def __init__(self, frame_no, content, size):
        super().__init__(frame_no, size)
        self.header = content[:2]
        self.payload = content[2:]

    def __init__(self, hci_frame):
        super().__init__(hci_frame.frame_no, hci_frame.size)
        self.header = hci_frame.payload[:2]
        self.payload = hci_frame.payload[2:]

    def get_event_code(self):
        return self.header[0]

    def get_payload_length(self):
        return self.header[1]

    def __repr__(self):
        if _EVENT_DEBUG:
            return "Event Packet {}: Event Type 0x{:02x}, Payload length: {}".format(
                self.frame_no, self.get_event_code(), self.get_payload_length())
        else:
            return ""


"""
A class for HCI ACL data packets


Handle(2 Bytes) + Data Total Length(2 Bytes)

"""
class ACLDataPacket(HciFrame):

    def __init__(self, frame_no, content, size):
        super().__init__(frame_no, size)
        self.header = content[:4]
        self.payload = content[4:]

    def __init__(self, hci_frame):
        super().__init__(hci_frame.frame_no, hci_frame.size)
        self.header = hci_frame.payload[:4]
        self.payload = hci_frame.payload[4:]

    def get_handle(self):
        return self.header[0] | (0 << 8)

    def get_payload_length(self):
        return self.header[2] | (self.header[3] << 8)

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header

    def __repr__(self):
        if _ACL_DEBUG:
            return "ACL data packets {}: handle 0x{:04x}, Total length: {}".format(
                self.frame_no, self.get_handle(), self.get_payload_length()
            )
        else:
            return ""