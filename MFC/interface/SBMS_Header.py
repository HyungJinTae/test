
from common.App_Header import *

SBMS_RELAY_CLOSED = 1
SBMS_RELAY_OPENED = 2

SBMS_IMD_OK = 1
SBMS_IMD_NOK = 0

SBMS_ACTIVATED = 1
SBMS_DEACTIVATED = 0

SBMS_ST_IDLE = 0
SBMS_ST_END = (SBMS_ST_IDLE + 1)


class SBMS_Param:
    def __init__(self):
        self.state = 0
        self.is_activated = 0
        self.hv_relay = 0
        self.hv_relay_status = 0
        self.imd_status = 0

