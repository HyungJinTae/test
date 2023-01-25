BEG_ID_ERROR_CODE_BIT_SHIFT = 26
BEG_ID_DEVICE_NO_BIT_SHIFT = 22
BEG_ID_COMMAND_NO_BIT_SHIFT = 16
BEG_ID_DESTINATION_BIT_SHIFT = 8
BEG_ID_SOURCE_BIT_SHIFT = 0

BEG_ID_ERROR_CODE_NORMAL = 0x00
BEG_ID_ERROR_CODE_COMMAND_INVALID = 0x02
BEG_ID_ERROR_CODE_DATA_INVALID = 0x03
BEG_ID_ERROR_CODE_IN_START_PROCESSING = 0x07
BEG_ID_DEVICE_NO_SINGlE_MODULE = 0x0A   # Protocol between controller and single module
BEG_ID_DEVICE_NO_GROUP_MODULE = 0x0B    # Protocol between controller and module group
BEG_ID_DESTINATION_BROADCAST = 0x3F
BEG_ID_DESTINATION_DEFAULT_ADDRESS = 0x00
BEG_ID_SOURCE_DEFAULT_ADDRESS = 0xF0
BEG_ID_COMMAND_NO_READ = 0x23
BEG_ID_COMMAND_NO_WRITE = 0x24

BEG_COMMAND_SUB_BYTE0_SYSTEM_BASIC_INFO = 0x10        # system basic information
BEG_COMMAND_SUB_BYTE0_SINGLE_PM_BASIC = 0x11          # single PM basic information
BEG_COMMAND_SUB_BYTE0_SINGLE_PM_AC_SIDE = 0x21        # single PM AC side information
BEG_COMMAND_SUB_BYTE0_SINGLE_BIDIR_DC_SIDE = 0x41     # single bidirectional DC/DC PM basic information.

BEG_READ_D1_SYSTEM_DC_SIDE_VOLTAGE = 0x01
BEG_READ_D1_SYSTEM_DC_SIDE_CURRENT = 0x02
BEG_READ_D1_POWER_MODULE_NUMBER = 0x10
BEG_READ_D1_POWER_MODULE_SIDE_VOLTAGE = 0x01
BEG_READ_D1_POWER_MODULE_SIDE_CURRENT = 0x02
BEG_READ_D1_ACAB_LINE_VOLTAGE = 0x03
BEG_READ_D1_ACBC_LINE_VOLTAGE = 0x04
BEG_READ_D1_ACCA_LINE_VOLTAGE = 0x05
BEG_READ_D1_TEMPERATURE = 0x06
BEG_READ_D1_STATUS = 0x10
BEG_READ_D1_INVERTER_STATUS = 0x11
REG_READ_D1_MODULE_GROUP_NUMBER = 0x20
BEG_READ_D1_AC_A_PHASE_VOLTAGE = 0x01
BEG_READ_D1_AC_B_PHASE_VOLTAGE = 0x02
BEG_READ_D1_AC_C_PHASE_VOLTAGE = 0x03
BEG_READ_D1_AC_A_PHASE_CURRENT = 0x04
BEG_READ_D1_AC_B_PHASE_CURRENT = 0x05
BEG_READ_D1_AC_C_PHASE_CURRENT = 0x06
BEG_READ_D1_AC_FREQUENCY = 0x07
BEG_READ_D1_TOTAL_ACTIVE_POWER = 0x08
BEG_READ_D1_AC_A_PHASE_ACTIVE_POWER = 0x09
BEG_READ_D1_AC_B_PHASE_ACTIVE_POWER = 0x0A
BEG_READ_D1_AC_C_PHASE_ACTIVE_POWER = 0x0B
BEG_READ_D1_TOTAL_REACTIVE_POWER = 0x0C
BEG_READ_D1_TOTAL_APPARENT_POWER = 0x10
BEG_READ_D1_FW_VERSION1 = 0x22
BEG_READ_D1_FW_VERSION2 = 0x23

BEG_READ_D1_HIGH_VOLTAGE = 0x01
BEG_READ_D1_HIGH_CURRENT = 0x02

BEG_WRITE_D1_SYSTEM_DC_VOLTAGE = 0x01
BEG_WRITE_D1_SYSTEM_DC_CURRENT = 0x02
BEG_WRITE_D1_POWER_MODULE_SIDE_VOLTAGE = 0x01
BEG_WRITE_D1_POWER_MODULE_SIDE_CURRENT = 0x02
BEG_WRITE_D1_MODULE_ON_OFF = 0x10
BEG_WRITE_D1_GREEN_LED_BLINK = 0x20
BEG_WRITE_D1_SLEEP = 0x21
BEG_WRITE_D1_WALKIN_ENABLE = 0x22
BEG_WRITE_D1_WORKING_MODE = 0x10
BEG_WRITE_D1_ALLOW_WRONG_PHASE = 0x11
BEG_WRITE_D1_L1_OV_PROTECTION_VOLTAGE = 0x20
BEG_WRITE_D1_L1_OV_PROTECTION_TIME = 0x21
BEG_WRITE_D1_L2_OV_PROTECTION_VOLTAGE = 0x22
BEG_WRITE_D1_L2_OV_PROTECTION_TIME = 0x23
BEG_WRITE_D1_L1_LV_PROTECTION_VOLTAGE = 0x24
BEG_WRITE_D1_L1_LV_PROTECTION_TIME = 0x25
BEG_WRITE_D1_L2_LV_PROTECTION_VOLTAGE = 0x26
BEG_WRITE_D1_L2_LV_PROTECTION_TIME = 0x27
BEG_WRITE_D1_RATED_PHASE_VOLTAGE = 0x91
BEG_WRITE_D1_HIGH_VOLTAGE = 0x01
BEG_WRITE_D1_HIGH_CURRENT = 0x02

BEG_DATA_INFO_BYTE0 = 0
BEG_DATA_INFO_BYTE1 = 1
BEG_DATA_INFO_BYTE2 = 2
BEG_DATA_INFO_BYTE3 = 3
BEG_DATA_INFO_BYTE4 = 4
BEG_DATA_INFO_BYTE5 = 5
BEG_DATA_INFO_BYTE6 = 6
BEG_DATA_INFO_BYTE7 = 7

BEG_MAX_CONTROLLER_COUNT = 8
BEG_MAX_GROUP_MODULE_COUNT = 60
BEG_MAX_DATA_LENGTH = 8
BEG_MAX_DC_VOLTAGE_VALUE = 1000.0
BEG_MIN_DC_VOLTAGE_VALUE = 150.0
BEG_MAX_DC_CURRENT_VALUE = 73.0
BEG_MIN_DC_CURRENT_VALUE = 0.0
BEG_INT_TO_BYTE_LENGTH = 4
BEG_SCALE_MILLI_VOLTAGE = 1000.0

BEG_MODULE_ON_VALUE = 0xA0
BEG_MODULE_OFF_VALUE = 0xA1
BEG_MODULE_GREEN_LED_BLINK = 0xA1
BEG_MODULE_GREEN_LED_NORMAL = 0xA0
BEG_MODULE_SLEEP_VALUE = 0xA1
BEG_MODULE_NOT_SLEEP_VALUE = 0xA0
BEG_MODULE_WALKIN_ENABLE = 0xA1
BEG_MODULE_WALKIN_DISABLE = 0xA0
BEG_MODULE_WORKING_MODE_READY = 0
BEG_MODULE_WORKING_MODE_RECTIFICATION = 0xA0
BEG_MODULE_WORKING_MODE_INVERTER = 0xA1
BEG_MODULE_WORKING_MODE_INVERTER_OFF_GRID = 0xA2
BEG_MODULE_ALLOW_WRONG_PHASE_ON = 0xA1
BEG_MODULE_ALLOW_WRONG_PHASE_OFF = 0xA0


class BEG_Alarm_Status:
    mdl_pfc_side_off = False
    input_over_voltage_protection = False
    input_low_voltage_alarm = False
    three_phase_input_unbalance_alarm = False
    three_phase_input_phase_lost_alarm = False
    mdl_load_sharing_alarm = False
    mdl_id_repeat_alarm = False
    mdl_power_limit_status = False
    mdl_communication_interrupt_alarm = False
    mdl_walk_in_enable = False
    output_over_voltage_alarm = False
    over_temperature_alarm = False
    fan_fault_alarm = False
    mdl_protection_alarm = False
    mdl_fault_alarm = False
    mdl_dc_side_off_status = False
    mdl_discharge_abnormal = False
    mdl_sleeping = False
    mdl_output_short_current = False
    inverter_mode = False
    rectifier_mode = False


class BEG_Identifier:
    def __init__(self):
        self.error_code = 0
        self.device_no = 0
        self.command_no = 0
        self.destination_address = 0
        self.source_address = 0

    def set_error_code(self, error_code):
        self.error_code = error_code

    def set_device_no(self, device_no):
        self.device_no = device_no

    def set_command_no(self, command_no):
        self.command_no = command_no

    def set_destination_address(self, destination_address):
        self.destination_address = destination_address

    def set_source_address(self, source_address):
        self.source_address = source_address

    def get_identifier(self):
        identifier = 0
        identifier += (self.error_code & 0x07) << BEG_ID_ERROR_CODE_BIT_SHIFT
        identifier += (self.device_no & 0x0F) << BEG_ID_DEVICE_NO_BIT_SHIFT
        identifier += (self.command_no & 0x3F) << BEG_ID_COMMAND_NO_BIT_SHIFT
        identifier += (self.destination_address & 0xFF) << BEG_ID_DESTINATION_BIT_SHIFT
        identifier += (self.source_address & 0xFF) << BEG_ID_SOURCE_BIT_SHIFT
        return identifier

    def parsing_identifier(self, identifier):
        error_code = (identifier >> BEG_ID_ERROR_CODE_BIT_SHIFT) & 0x07
        device_no = (identifier >> BEG_ID_DEVICE_NO_BIT_SHIFT) & 0x0F
        command_no = (identifier >> BEG_ID_COMMAND_NO_BIT_SHIFT) & 0x3F
        destination_address = (identifier >> BEG_ID_DESTINATION_BIT_SHIFT) & 0xFF
        source_address = (identifier >> BEG_ID_SOURCE_BIT_SHIFT) & 0xFF
        return error_code, device_no, command_no, destination_address, source_address


class BEG_parameters:
    def __init__(self):
        self.module_address = 0
        self.rx_count = 0
        self.read_identifier = 0
        self.alarm = False
        self.alarm_code = 0
        self.alarm_status = BEG_Alarm_Status()

        self.power_module_dc_side_voltage = float(0)
        self.power_module_dc_side_current = float(0)
        self.ac_ab_line_voltage = float(0)
        self.ac_bc_line_voltage = float(0)
        self.ac_ca_line_voltage = float(0)
        self.power_module_temperature = float(0)
        self.power_module_status = [0] * BEG_MAX_DATA_LENGTH
        self.inverter_status = [0] * BEG_MAX_DATA_LENGTH
        self.module_group_number = int(0)
        self.dc_max_output_voltage = float(0)
        self.dc_min_output_voltage = float(0)
        self.dc_max_output_current = float(0)
        self.dc_min_output_current = float(0)
        self.ac_a_phase_voltage = float(0)
        self.ac_b_phase_voltage = float(0)
        self.ac_c_phase_voltage = float(0)
        self.ac_a_phase_current = float(0)
        self.ac_b_phase_current = float(0)
        self.ac_c_phase_current = float(0)
        self.ac_frequency = float(0)
        self.total_active_power = float(0)
        self.ac_a_phase_active_power = float(0)
        self.ac_b_phase_active_power = float(0)
        self.ac_c_phase_active_power = float(0)
        self.total_reactive_power = float(0)
        self.ac_a_phase_reactive_power = float(0)
        self.ac_b_phase_reactive_power = float(0)
        self.ac_c_phase_reactive_power = float(0)
        self.total_apparent_power = float(0)
        self.ac_a_phase_apparent_power = float(0)
        self.ac_b_phase_apparent_power = float(0)
        self.ac_c_phase_apparent_power = float(0)
        self.pm_dc_high_voltage_side_voltage = float(0)
        self.pm_dc_high_voltage_side_current = float(0)
