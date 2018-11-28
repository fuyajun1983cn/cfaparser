from cfaparser.handler import Handler
from cfaparser.utils import info
from cfaparser.sdp import SDPHandler

L2CAP_DEBUG = True

BT_PSM_SDP      =                0x0001
BT_PSM_RFCOMM   =                0x0003
BT_PSM_TCS      =                0x0005
BT_PSM_CTP      =                0x0007
BT_PSM_BNEP     =                0x000F
BT_PSM_HIDC     =                0x0011
BT_PSM_HIDI     =                0x0013
BT_PSM_UPNP     =                0x0015
BT_PSM_AVCTP    =                0x0017
BT_PSM_AVDTP    =                0x0019
BT_PSM_AVCTP_13 =                0x001B
BT_PSM_UDI_CP   =                0x001D
BT_PSM_ATT      =                0x001F

"""
A class holding sdp related variables
"""
class SDPVars:
    sdp_request_received = False
    sdp_scid = 0
    sdp_dcid = 0
    sdp_l2cap_id = 0
    sdp_handler = SDPHandler()

    @classmethod
    def reset(cls):
        """
         reset all class holding variables
        :return:  None
        """
        sdp_request_received = False
        sdp_scid = 0
        sdp_dcid = 0
        sdp_l2cap_id = 0

class L2capHandler(Handler):

    NAME = "L2CAP Handler"



    def process(self, data):
        #Header part
        print_str = ""
        try:
            pdu_len = data[0] | data[1] << 8
            chn_id = data[2] | data[3] << 8

            if chn_id == 0x0001: #Signaling Channel
                code = data[4]
                identifier = data[5]
                length = data[6] | data[7] << 8
                print_str += "Identifier: {}, Command Length: 0x{:04x}, ".format(identifier, length)
                if code == 0x01:
                    print_str += "[Command Reject]"
                elif code == 0x02:
                    psm = data[8] | data[9] << 8
                    scid = data[10] | data[11] << 8
                    print_str += "PSM: 0x{:04x}, Source CID: 0x{:04x}".format(psm, scid)
                    print_str += "[Connection Request]"
                    if psm == BT_PSM_SDP:
                        print_str += "[SDP]"
                        SDPVars.reset()
                        SDPVars.sdp_request_received = True
                        SDPVars.sdp_l2cap_id = identifier
                elif code == 0x03:
                    print_str += "Connection Response"
                    if identifier == SDPVars.sdp_l2cap_id and SDPVars.sdp_request_received == True:
                        SDPVars.sdp_request_received = False
                        SDPVars.sdp_dcid = data[8] | data[9] << 8
                        SDPVars.sdp_scid = data[10] | data[11] << 8
                elif code == 0x04:
                    print_str += "Configure Request"
                elif code == 0x05:
                    print_str += "Configure Response"
                elif code == 0x06:
                    print_str += "Disconnection Request"
                elif code == 0x07:
                    print_str += "Disconnection Response"
                elif code == 0x08:
                    print_str += "Echo Request"
                elif code == 0x09:
                    print_str += "Echo Response"
                elif code == 0x0a:
                    print_str += "Information Request"
                elif code == 0x0b:
                    print_str += "Information Response"
                elif code == 0x0c:
                    print_str += "Create Channel Request"
                elif code == 0x0d:
                    print_str += "Create Channel Response"
                elif code == 0x0e:
                    print_str += "Move Channel Request"
                elif code == 0x0f:
                    print_str += "Move Channel Response"
                elif code == 0x10:
                    print_str += "Move Channel Confirmation"
                elif code == 0x11:
                    print_str += "Move Channel Confirmation Response"
                elif code == 0x12:
                    print_str += "Connection Parameter Update Request"
                elif code == 0x13:
                    print_str += "Connection Parameter Update Response"
                elif code == 0x14:
                    print_str += "LE Credit Based Connection Request"
                elif code == 0x15:
                    print_str += "LE Credit Based Connection Response"
                elif code == 0x16:
                    print_str += "LE Flow Control Credit"
                else:
                    print_str += "Unknown Signaling Packet type"
            elif chn_id == 0x0005:
                print_str += "[LE Signaling]"
            elif chn_id == 0x0004: #ATT
                print_str += "[ATT]: "
            elif chn_id == SDPVars.sdp_scid or chn_id == SDPVars.sdp_dcid: #SDP Request/Response
                SDPVars.sdp_handler.process(data[4:])
            else:
                pass

        except IndexError:
            pass #ignore invalid data packet silently
        else:
            if L2CAP_DEBUG == False:
                info("PDU Length: {}, CID: 0x{:04x}, Details of the PDU: {} ".format(pdu_len, L2capHandler.sdp_scid, print_str))