# Application Main Header

from common.Setting import *

APP_DC_INPUT_FZ10 = 1
APP_DC_INPUT_BOKUK = 2
APP_DC_INPUT_BS30 = 3
APP_DC_INPUT_SRC = APP_DC_INPUT_FZ10

APP_CAN_TYPE_KVASER = 1
APP_CAN_TYPE_BCU_SERIAL = 2
APP_CAN_TYPE = APP_CAN_TYPE_KVASER

APP_CAN_TYPE_KVASER_CHANNEL_COUNT = 1

# for test
APP_MAX_CURRENT_LIMIT_FZ10 = 5.0

APP_VERSION_MAJOR = 0
APP_VERSION_MINOR = 1
APP_MAX_POWER_LIMIT = 30000
APP_MIN_CURRENT_LIMIT = 0.0
APP_MAX_CURRENT_LIMIT = 200.0
APP_MIN_VOLTAGE_LIMIT = 150.0
APP_MAX_VOLTAGE_LIMIT = 800.0

APP_CEG_GROUP_NO = 8
APP_CEG_MODULE_COUNT = 2
APP_CEG_MODULE0_ID = 0
APP_CEG_MODULE1_ID = 1
APP_CEG_MODULE2_ID = 2
APP_CEG_MODULE3_ID = 3
__ID_LIST__ = [
    APP_CEG_MODULE0_ID,
    APP_CEG_MODULE1_ID,
    APP_CEG_MODULE2_ID,
    APP_CEG_MODULE3_ID
]
APP_CEG_MODULE_ID_LIST = []
for i in range(APP_CEG_MODULE_COUNT):
    APP_CEG_MODULE_ID_LIST.append(__ID_LIST__[i])

APP_CEG_CONTROL_ON = 0xA0
APP_CEG_CONTROL_OFF = 0xA1
APP_CEG_WALKIN_ENABLE = 0xA0
APP_CEG_WALKIN_DISABLE = 0xA1
APP_CEG_MODULE_ID_1_BLINK = 0xA0
APP_CEG_MODULE_ID_1_NORMAL = 0xA1
APP_CEG_MODULE_ID_2_BLINK = 0xB0
APP_CEG_MODULE_ID_2_NORMAL = 0xB1

APP_BEG_GROUP_NO = 4
APP_BEG_MODULE_COUNT = 1
APP_BEG_MODULE0_ID = 0
__BEG_ID_LIST = [
    APP_BEG_MODULE0_ID
]
APP_BEG_MODULE_ID_LIST = []
for i in range(APP_BEG_MODULE_COUNT):
    APP_BEG_MODULE_ID_LIST.append(__ID_LIST__[i])


APP_TRUE = 1
APP_FALSE = 0

if APP_CAN_TYPE_KVASER_CHANNEL_COUNT == 1:
    APP_CEG_CAN_CHANNEL_NO = 0
    APP_BEG_CAN_CHANNEL_NO = 0
    APP_DEVICE_CAN_CHANNEL_NO = 0
    APP_SBMS_CAN_CHANNEL_NO = 0
    APP_SECC_CAN_CHANNEL_NO = 0
    APP_DBG_CAN_CHANNEL_NO = 0
    APP_CEG_CAN_FLAG = 'INIT_ACCESS'
    APP_BEG_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_DEVICE_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_SBMS_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_SECC_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_DBG_CAN_FLAG = 'NO_INIT_ACCESS'
elif APP_CAN_TYPE_KVASER_CHANNEL_COUNT == 2:
    APP_CEG_CAN_CHANNEL_NO = 0
    APP_BEG_CAN_CHANNEL_NO = 0
    APP_DEVICE_CAN_CHANNEL_NO = 1
    APP_SBMS_CAN_CHANNEL_NO = 1
    APP_SECC_CAN_CHANNEL_NO = 1
    APP_DBG_CAN_CHANNEL_NO = 1
    APP_CEG_CAN_FLAG = 'INIT_ACCESS'
    APP_BEG_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_DEVICE_CAN_FLAG = 'INIT_ACCESS'
    APP_SBMS_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_SECC_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_DBG_CAN_FLAG = 'NO_INIT_ACCESS'
else:
    APP_CEG_CAN_CHANNEL_NO = 0
    APP_BEG_CAN_CHANNEL_NO = 0
    APP_DEVICE_CAN_CHANNEL_NO = 1
    APP_SBMS_CAN_CHANNEL_NO = 1
    APP_SECC_CAN_CHANNEL_NO = 2
    APP_DBG_CAN_CHANNEL_NO = 3
    APP_CEG_CAN_FLAG = 'INIT_ACCESS'
    APP_BEG_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_DEVICE_CAN_FLAG = 'INIT_ACCESS'
    APP_SBMS_CAN_FLAG = 'NO_INIT_ACCESS'
    APP_SECC_CAN_FLAG = 'INIT_ACCESS'
    APP_DBG_CAN_FLAG = 'INIT_ACCESS'

if RUN_LEVEL == RUN_LEVEL_DEBUG:
    APP_CEG_CAN_BIT_RATE = "500K"
    APP_DEVICE_CAN_BIT_RATE = "500K"
    APP_SECC_CAN_BIT_RATE = "500K"
    APP_DBG_CAN_BIT_RATE = "500K"
else:
    APP_CEG_CAN_BIT_RATE = "125K"
    APP_DEVICE_CAN_BIT_RATE = "250K"
    APP_SECC_CAN_BIT_RATE = "500K"
    APP_DBG_CAN_BIT_RATE = "500K"

APP_TRUE = 1
APP_FALSE = 0

APP_CAN_ID_DEBUG_MSG1 = 0x18AC1001
APP_CAN_ID_DEBUG_EVSE = 0x18AC1002
APP_CAN_ID_DEBUG_SECC = 0x18AC1003
APP_CAN_ID_DEBUG_REG = 0x18AC1004

APP_RUN_MODE_IDLE = 0
APP_RUN_MODE_DCDC_TEST = (APP_RUN_MODE_IDLE + 1)
APP_RUN_MODE_ADMIN = (APP_RUN_MODE_DCDC_TEST + 1)
APP_RUN_MODE_EV_CHARGING = 10
APP_RUN_MODE_BATTERY_CHARGING = (APP_RUN_MODE_EV_CHARGING + 1)
APP_RUN_MODE_DRIVE = 20
APP_RUN_MODE_STOPPING = 30
APP_RUN_MODE_BOOT = 40
APP_RUN_MODE_EM_STOP = (APP_RUN_MODE_BOOT + 1)
APP_RUN_MODE_SHUTDOWN = 99
APP_RUN_MODE_END = (APP_RUN_MODE_SHUTDOWN + 1)


class TaskBase:
    def __init__(self):
        pass

    def run(self):
        pass
