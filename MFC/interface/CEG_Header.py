# INFY DC-DC Converter Communication Interface Header

from common.App_Header import *

INFY_ID_ERROR_CODE_BIT_SHIFT = 26
INFY_ID_DEVICE_NO_BIT_SHIFT = 22
INFY_ID_COMMAND_NO_BIT_SHIFT = 16
INFY_ID_DESTINATION_BIT_SHIFT = 8
INFY_ID_SOURCE_BIT_SHIFT = 0

INFY_ID_ERROR_CODE_NORMAL = 0x00
INFY_ID_ERROR_CODE_COMMAND_INVALID = 0x02
INFY_ID_ERROR_CODE_DATA_INVALID = 0x03
INFY_ID_ERROR_CODE_IN_START_PROCESSING = 0x07
INFY_ID_DEVICE_NO_SINGlE_MODULE = 0x0A   # Protocol between controller and single module
INFY_ID_DEVICE_NO_GROUP_MODULE = 0x0B    # Protocol between controller and module group
INFY_ID_DESTINATION_BROADCAST = 0x3F
INFY_ID_DESTINATION_DEFAULT_ADDRESS = 0x00
INFY_ID_SOURCE_DEFAULT_ADDRESS = 0xF0

CEG_MAX_OUTPUT_VOLTAGE = 1000.0
CEG_MIN_OUTPUT_VOLTAGE = 150.0
CEG_MAX_OUTPUT_TOTAL_CURRENT = (100 * APP_CEG_MODULE_COUNT)

CEG_ID_CMD_NO_SYSTEM_OUTPUT_GET = 0x01
CEG_ID_CMD_NO_SYSTEM_MODULE_NUMBER_GET = 0x02
CEG_ID_CMD_NO_MODULE_OUTPUT_GET = 0x03
CEG_ID_CMD_NO_ALARM_STATE_TEMP_GET = 0x04
CEG_ID_CMD_NO_MODULE_INPUT_GET = 0x06
CEG_ID_CMD_NO_MODULE_OUTPUT_MAX_GET = 0x0A
CEG_ID_CMD_NO_MODULE_DIODE_OUTPUT_GET = 0x0C

CEG_ID_CMD_NO_MODULE_WALK_IN_SET = 0x13
CEG_ID_CMD_NO_MODULE_BLINK_SET = 0x14
CEG_ID_CMD_NO_CONTROL_ON_OFF_SET = 0x1A
CEG_ID_CMD_NO_SYSTEM_OUTPUT_SET = 0x1B
CEG_ID_CMD_NO_EACH_MODULE_OUTPUT_SET = 0x1C

CEG_APP_GROUP_NO = APP_CEG_GROUP_NO
CEG_APP_GROUP_MODULE_COUNT = APP_CEG_MODULE_COUNT
CEG_APP_MODULE_ID_1 = APP_CEG_MODULE0_ID
CEG_APP_MODULE_ID_2 = APP_CEG_MODULE1_ID

CEG_GROUP_MODULE_COUNT_MAX = 10
CEG_WRITE_DATA_LENGTH = 4
CEG_MAX_DATA_LENGTH = 8
CEG_SCALE_MILLI_VOLTAGE = 1000.0

CEG_MAX_DC_INPUT_VOLTAGE = 825.0
CEG_MIN_DC_INPUT_VOLTAGE = 650.0
CEG_MAX_DC_OUTPUT_VOLTAGE = 1000.0
CEG_MIN_DC_OUTPUT_VOLTAGE = 0.0
CEG_MAX_DC_INPUT_CURRENT = 50.0
CEG_MAX_DC_OUTPUT_CURRENT = 100.0
CEG_MAX_DC_OUTPUT_POWER_WATT = 30000.0
CEG_MIN_DC_OUTPUT_POWER_WATT = 14000.0

CEG_TEMPERATURE_MAX_POWER_SECTION1 = 45.0
CEG_TEMPERATURE_MAX_POWER_SECTION2 = 55.0
CEG_TEMPERATURE_MAX_POWER_SECTION3 = 65.0
CEG_TEMPERATURE_MAX_POWER_SECTION4 = 75.0
CEG_TEMPERATURE_MAX_POWER_SECTION5 = 78.0


CEG_MIN_DC_INPUT_VOLTAGE_SLOPE = 300.0
CEG_MIN_DC_INPUT_VOLTAGE_X = 45
CEG_MIN_DC_INPUT_VOLTAGE_ALPHA = 285

CEG_TRUE = APP_TRUE
CEG_FALSE = APP_FALSE

CEG_DEF_CONTROL_OFF = 1
CEG_DEF_CONTROL_ON = 0
CEG_DEF_DC_SIDE_OFF_ON = 1
CEG_DEF_DC_SIDE_OFF_OFF = 0
CEG_DEF_GREEN_LED_BLINK = 1
CEG_DEF_GREEN_LED_NORMAL = 0
CEG_DEF_WALK_IN_ENABLE = 1
CEG_DEF_WALK_IN_DISABLE = 0


def CEG_DataToBit(data, bit):
    return (data >> bit) & 0x01


def CEG_FloatFromByteArray(byte_array, multiple=0.1, byteorder='big', signed=True):
    i_res = int.from_bytes(byte_array, byteorder=byteorder, signed=signed)
    return float(i_res) * multiple


def CEG_FloatToDataArray(fData, multiple=1000, byte_length=4, byteorder='big', signed=False):
    iData = int(fData * multiple)
    data_array = list(iData.to_bytes(byte_length, byteorder=byteorder, signed=signed))
    return data_array


def INFY_ParsingIdentifier(identifier):
    error_code = (identifier >> INFY_ID_ERROR_CODE_BIT_SHIFT) & 0x07
    device_no = (identifier >> INFY_ID_DEVICE_NO_BIT_SHIFT) & 0x0F
    command_no = (identifier >> INFY_ID_COMMAND_NO_BIT_SHIFT) & 0x3F
    destination_address = (identifier >> INFY_ID_DESTINATION_BIT_SHIFT) & 0xFF
    source_address = (identifier >> INFY_ID_SOURCE_BIT_SHIFT) & 0xFF
    return error_code, device_no, command_no, destination_address, source_address


class INFY_Identifier:
    def __init__(self):
        self.error_code = 0
        self.device_no = 0
        self.command_no = 0
        self.destination_address = 0
        self.source_address = 0

    def SetErrorCode(self, error_code):
        self.error_code = error_code

    def SetDeviceNo(self, device_no):
        self.device_no = device_no

    def SetCommandNo(self, command_no):
        self.command_no = command_no

    def SetDestinationAddress(self, destination_address):
        self.destination_address = destination_address

    def SetSourceAddress(self, source_address):
        self.source_address = source_address

    def GetIdentifier(self):
        identifier = 0
        identifier += (self.error_code & 0x07) << INFY_ID_ERROR_CODE_BIT_SHIFT
        identifier += (self.device_no & 0x0F) << INFY_ID_DEVICE_NO_BIT_SHIFT
        identifier += (self.command_no & 0x3F) << INFY_ID_COMMAND_NO_BIT_SHIFT
        identifier += (self.destination_address & 0xFF) << INFY_ID_DESTINATION_BIT_SHIFT
        identifier += (self.source_address & 0xFF) << INFY_ID_SOURCE_BIT_SHIFT
        return identifier


class CEG_Alarm_State:
    def __init__(self):
        self.pfc_side_is_off = 1
        self.input_over_voltage = 0
        self.input_under_voltage = 0
        self.input_unbalance = 0
        self.input_phase_lost = 0
        self.load_unsharing = 0
        self.mdl_ID_repetition = 0
        self.power_limit = 0
        self.can_comm_interrupt = 0
        self.walk_in_enable = 0
        self.output_over_voltage = 0
        self.over_temperature = 0
        self.fan_fault = 0
        self.mdl_protect = 0
        self.mdl_fault = 0
        self.dc_side_is_off = 1
        self.discharge_abnormal = 0
        self.pfc_side_abnormal = 0
        self.inner_comm_interrupt = 0
        self.output_short = 0


class CEG_Module_Demand_Parameters:
    def __init__(self, module_ID):
        self.module_ID = module_ID
        self.alarm_code = 0
        self.alarm_state = CEG_Alarm_State()
        self.output_voltage = float(0)
        self.output_current = float(0)
        self.group_no = 0
        self.temperature = 0
        self.state0 = 0
        self.state1 = 0
        self.state2 = 0
        self.input_voltage = float(0)
        self.max_output_voltage = float(0)
        self.min_output_voltage = float(0)
        self.max_output_current = float(0)
        self.rated_output_power = float(0)
        self.diode_output_voltage = float(0)
        self.available_output_current = float(0)

    def SetModuleID(self, module_ID):
        self.module_ID = module_ID
