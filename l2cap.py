from cfaparser.handler import Handler
from cfaparser.utils import info


class L2capHandler(Handler):

    NAME = "L2CAP Handler"

    def process(self, data):
        #Header part
        print_str = ""
        try:
            pdu_len = data[0] | data[1] << 8
            chn_id = data[2] | data[3] << 8

            if chn_id == 0x0001:
                print_str += "[Signaling]: "
                code = data[4]
                if code == 0x0a:
                    print_str += "Information Request"
                elif code == 0x0b:
                    print_str += "Information Response"
                elif code == 0x02:
                    print_str += "Connection Request"
                elif code == 0x03:
                    print_str += "Connection Response"
                elif code == 0x04:
                    print_str += "Configure Request"
                elif code == 0x05:
                    print_str += "Configure Response"
                elif code == 0x06:
                    print_str += "Disconnection Request"
                elif code == 0x07:
                    print_str += "Disconnection Response"
                else:
                    print_str += "Unknown Signaling Packet type"
            elif chn_id == 0x0004: #ATT
                print_str += "[ATT]: "
            else:
                pass
        except IndexError:
            pass #ignore invalid data packet silently
        else:
            info("PDU Length: {}, Details of the PDU: {} ".format(pdu_len, print_str))