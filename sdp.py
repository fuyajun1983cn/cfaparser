from cfaparser.handler import Handler
from cfaparser.utils import info

SDP_DEBUG = True

class SDPHandler(Handler):

    NAME = "SDP Handler"

    def _PID2STR(self, PDU_ID):
        strs = (
            "Reserved for future use",
            "SDP_ErrorResponse",
            "SDP_ServiceSearchRequest",
            "SDP_ServiceSearchResponse",
            "SDP_ServiceAttributeRequest",
            "SDP_ServiceAttributeResponse",
            "SDP_ServiceSearchAttributeRequest",
            "SDP_ServiceSearchAttributeResponse"
        )

        if PDU_ID > 0x08:
            return strs[0]

        return strs[PDU_ID]

    def _parse_dataelement(self, data):
        type_desc = data >> 3
        size_index = data & 0x07

        valids = {
            0:[0,],
            1: [0, 1, 2, 3, 4],
            2: [0, 1, 2, 3, 4],
            3: [1, 2, 4],
            4: [5, 6, 7],
            5: [0,],
            6: [5, 6, 7],
            7: [5, 6, 7],
            8: [5, 6, 7]
        }

        if not size_index in valids[type_desc]:
            return -1,-1

        return type_desc, size_index

    def process(self, data):
        PDU_ID = data[0]
        TID = data[1] | data[2] << 8
        PLEN = data[4] | data[3] << 8

        print_str = " "

        if PDU_ID == 0x01: #SDP_ErrorResponse
            pass
        elif PDU_ID == 0x02: #SDP_ServiceSearchRequest
            pass
        elif PDU_ID == 0x03: #SDP_ServiceSearchResponse
            pass
        elif PDU_ID == 0x04: #SDP_ServiceAttributeRequest
            pass
        elif PDU_ID == 0x05: #SDP_ServiceAttributeResponse
            pass
        elif PDU_ID == 0x06: #SDP_ServiceSearchAttributeRequest
            #Parameters
            #ServiceSearchPattern
            type_desc, size_index = self._parse_dataelement(data[5])
            size = 0
            uuid = 0
            MaximumAttributeByteCount = 0
            AttributeIDList = []
            if size_index == 5:
                size = data[6]
                uuid = int.from_bytes(data[7:7+size], byteorder='big', signed=False) & 0x00FFFF
                if uuid == 0x111e:
                    print_str += "[HandFree]"
                MaximumAttributeByteCount = int.from_bytes(data[7+size:9+size], byteorder='big', signed=False)
            elif size_index == 6:
                size = int.from_bytes(data[6:8], byteorder='little', signed=False)
                uuid = int.from_bytes(data[8:8+size], byteorder='big', signed=False)  & 0x00FFFF
            elif size_index == 7:
                size = int.from_bytes(bytes[6:10], byteorder='little', signed=False)
                uuid = int.from_bytes(data[10:10+size], byteorder='big', signed=False) & 0x00FFFF

            info("Type: {}, Size_Index: {}, size: {} UUID: 0x{:04x}".format(type_desc, size_index, size, uuid)) #0x111b
            #MaximumAttributeByteCount,
            info("MaximumAttributeByteCount: {}".format(MaximumAttributeByteCount))
            #AttributeIDList,

            #ContinuationState

        elif PDU_ID == 0x07: #SDP_ServiceSearchAttributeResponse
            pass
        elif 0x08 <= PDU_ID <= 0xFF or PDU_ID == 0x00: #Reserved for future use
            pass
        else:
            pass



        if SDP_DEBUG == True:
            info("PDU ID: {}, Transaction ID: 0x{:04x}, Parameter Length: {}".format(self._PID2STR(PDU_ID), TID, PLEN))
