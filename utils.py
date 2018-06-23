"""
short and useful global functions
"""

import pprint

##constants

#packet type
COMMAND = 1
ACL_DATA = 2
EVENT = 4


##helper function
def info(msg):
    pprint.pprint(msg)
