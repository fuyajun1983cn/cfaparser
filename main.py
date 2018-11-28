""""
    A  cfa file parser for self use.

    reference file: vendor/qcom/opensource/bluetooth/bt_logger/src/btsnoop_dump.c


    24 Bytes snoop Header
    Initial 4 bytes have the length of the HCI packet
    Read 8 bytes which have orignal length and included length
279*/
"""

import pprint
import base64
from cfaparser import utils
from cfaparser import hciframe
from cfaparser.l2cap import L2capHandler


## Snoop file header magic
SNOOP_FILE_MAGIC = b'btsnoop\x00\x00\x00\x00\x01\x00\x00\x03\xea'
SNOOP_FILE_MAGIC_LEN = 16

SNOOP_HEADER_LEN = 24

file_size = 0
#hold all hci packets
hci_frames = []
command_frames = []
event_frames = []
data_frames = []


def process_frame(frame_no, frame_content, frame_len):
    frame = hciframe.HciFrame(frame_no, frame_len)
    frame.load_content(frame_content)
    hci_frames.append(frame)


def main():
    global file_size
    frame_no = 0
    with open("files/test1.cfa", mode='rb') as f:
        pos = f.seek(0)
        if f.read(SNOOP_FILE_MAGIC_LEN) == SNOOP_FILE_MAGIC:
            utils.info("It's a BT snoop file")
        else:
            utils.info("It's an invalid BT snoop file.")
            return

        while True:
            bytes = f.read(SNOOP_HEADER_LEN)
            if len(bytes) != SNOOP_HEADER_LEN:
                break;
            #hci_len = bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3]
            frame_len = int.from_bytes(bytes[0:4], byteorder='big', signed=False)
          #  pprint.pprint("Frame Size: {}".format(frame_len))
            frame_content = f.read(frame_len)
            frame_no += 1
          #  pprint.pprint("Frame Content: {}".format(frame_content))
            process_frame(frame_no, frame_content, frame_len)
            file_size += SNOOP_HEADER_LEN + frame_len

    #put frames into the seprate list as per type
    for frame in hci_frames:
        if frame.type == 1:
            command = hciframe.CommandPacket(frame)
            command_frames.append(command)
        elif frame.type == 2:
            data = hciframe.ACLDataPacket(frame)
            data_frames.append(data)
        elif frame.type == 4:
            event = hciframe.EventPacket(frame)
            event_frames.append(event)
        else:
            utils.info("Unknown frame, drop it.")

    #process frames
    hander = L2capHandler()
    for frame in data_frames:
        if int.from_bytes(frame.header[:2], byteorder="little", signed=False) == 0x2edc:
            pass #ignore QCA Debug Data
        else:
            #utils.info("======Frame NO: {}===========".format(frame.frame_no))
            if frame.frame_no in [247, 251, 253, 260, 262, 263, 339]:
                hander.process(frame.payload)
            #utils.info("======   End      ===========")


if __name__ == "__main__":

    main()