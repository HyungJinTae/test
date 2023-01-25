from common.Setting import logger
from interface.BEG_Header import *


class BEG_Group_Interface:
    def __init__(self, can_obj, grp_no):
        self.can_obj = can_obj

        self.is_activated = False

        self.group_address = grp_no
        self.group_dc_side_voltage = float(0)
        self.group_dc_side_total_current = float(0)
        self.group_power_module_numbers_of_group = 0
        self.dict_param = {0: BEG_parameters()}
        self.identifier = BEG_Identifier()

    def add_module(self, module_no):
        if module_no == 0:
            return
        self.dict_param[module_no] = BEG_parameters()

    def add_module_list(self, module_list):
        self.dict_param = {}
        for mdl_no in module_list:
            self.dict_param[mdl_no] = BEG_parameters()

    def initialize(self):
        if self.can_obj.is_opened:
            self.is_activated = True
        log_msg = "[BEG]"
        log_msg += f"Group No -> {self.group_address} |"
        log_msg += f"Module ID -> {self.dict_param.keys()} |"
        log_msg += f"Activated -> {self.is_activated} |"
        logger.info(log_msg)

    def finalize(self):
        if not self.is_activated:
            return
        self.is_activated = False

    # ###### query ###########

    def _query_read_group(self, byte0, byte1):
        data = bytearray([byte0, byte1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.identifier.set_error_code(BEG_ID_ERROR_CODE_NORMAL)
        self.identifier.set_device_no(BEG_ID_DEVICE_NO_GROUP_MODULE)
        self.identifier.set_command_no(BEG_ID_COMMAND_NO_READ)
        self.identifier.set_destination_address(self.group_address)
        self.identifier.set_source_address(BEG_ID_SOURCE_DEFAULT_ADDRESS)
        self.can_obj.write_wait(id_=self.identifier.get_identifier(), data=data)

    def _query_write_group(self, byte0, byte1, byte4567):
        data = bytearray([byte0, byte1, 0x00, 0x00, byte4567[0], byte4567[1], byte4567[2], byte4567[3]])
        self.identifier.set_error_code(BEG_ID_ERROR_CODE_NORMAL)
        self.identifier.set_device_no(BEG_ID_DEVICE_NO_GROUP_MODULE)
        self.identifier.set_command_no(BEG_ID_COMMAND_NO_WRITE)
        self.identifier.set_destination_address(self.group_address)
        self.identifier.set_source_address(BEG_ID_SOURCE_DEFAULT_ADDRESS)
        self.can_obj.write_wait(id_=self.identifier.get_identifier(), data=data)

    def _query_write_single(self, module_no, byte0, byte1, byte4567):
        data = bytearray([byte0, byte1, 0x00, 0x00, byte4567[0], byte4567[1], byte4567[2], byte4567[3]])
        self.identifier.set_error_code(BEG_ID_ERROR_CODE_NORMAL)
        self.identifier.set_device_no(BEG_ID_DEVICE_NO_SINGlE_MODULE)
        self.identifier.set_command_no(BEG_ID_COMMAND_NO_WRITE)
        self.identifier.set_destination_address(module_no)
        self.identifier.set_source_address(BEG_ID_SOURCE_DEFAULT_ADDRESS)
        self.can_obj.write_wait(id_=self.identifier.get_identifier(), data=data)

    # ###### query command functions ###########

    def _read_group_system_info(self, byte1):
        byte0 = BEG_COMMAND_SUB_BYTE0_SYSTEM_BASIC_INFO
        return self._query_read_group(byte0, byte1)

    def _read_group_module_info(self, byte1):
        byte0 = BEG_COMMAND_SUB_BYTE0_SINGLE_PM_BASIC
        return self._query_read_group(byte0, byte1)

    def _read_group_module_ac_info(self, byte1):
        byte0 = BEG_COMMAND_SUB_BYTE0_SINGLE_PM_AC_SIDE
        return self._query_read_group(byte0, byte1)

    def _write_group_system_info(self, byte1, byte4567):
        byte0 = BEG_COMMAND_SUB_BYTE0_SYSTEM_BASIC_INFO
        return self._query_write_group(byte0, byte1, byte4567)

    def _write_group_module_info(self, byte1, byte4567):
        byte0 = BEG_COMMAND_SUB_BYTE0_SINGLE_PM_BASIC
        return self._query_write_group(byte0, byte1, byte4567)

    def _write_group_module_ac_info(self, byte1, byte4567):
        byte0 = BEG_COMMAND_SUB_BYTE0_SINGLE_PM_AC_SIDE
        return self._query_write_group(byte0, byte1, byte4567)

    def _write_single_module_info(self, module_no, byte1, byte4567):
        byte0 = BEG_COMMAND_SUB_BYTE0_SINGLE_PM_BASIC
        return self._query_write_single(module_no, byte0, byte1, byte4567)

    def _write_single_module_ac_info(self, module_no, byte1, byte4567):
        byte0 = BEG_COMMAND_SUB_BYTE0_SINGLE_PM_AC_SIDE
        return self._query_write_single(module_no, byte0, byte1, byte4567)

    # ###### read command functions ###########

    # -- system info
    def read_system_info_dc_voltage(self):
        if not self.is_activated:
            return
        self._read_group_system_info(BEG_READ_D1_SYSTEM_DC_SIDE_VOLTAGE)

    def read_system_info_dc_total_current(self):
        if not self.is_activated:
            return
        self._read_group_system_info(BEG_READ_D1_SYSTEM_DC_SIDE_CURRENT)

    def read_system_info_power_module_numbers(self):
        if not self.is_activated:
            return
        self._read_group_system_info(BEG_READ_D1_POWER_MODULE_NUMBER)

    # -- module info
    def read_module_info_dc_voltage(self):
        if not self.is_activated:
            return
        self._read_group_module_info(BEG_READ_D1_POWER_MODULE_SIDE_VOLTAGE)

    def read_module_info_dc_current(self):
        if not self.is_activated:
            return
        self._read_group_module_info(BEG_READ_D1_POWER_MODULE_SIDE_CURRENT)

    def read_module_info_temperature(self):
        if not self.is_activated:
            return
        self._read_group_module_info(BEG_READ_D1_TEMPERATURE)

    def read_module_info_power_module_status(self):
        """ query unconditional """
        # if not self.is_activated:
        #    return
        self._read_group_module_info(BEG_READ_D1_STATUS)

    def read_module_info_inverter_status(self):
        """ query unconditional """
        # if not self.is_activated:
        #    return
        self._read_group_module_info(BEG_READ_D1_INVERTER_STATUS)

    def read_module_info_module_group_number(self):
        if not self.is_activated:
            return
        self._read_group_module_info(REG_READ_D1_MODULE_GROUP_NUMBER)

    def read_module_info_fw_version1(self):
        if not self.is_activated:
            return
        self._read_group_module_info(BEG_READ_D1_FW_VERSION1)

    def read_module_info_fw_version2(self):
        if not self.is_activated:
            return
        self._read_group_module_info(BEG_READ_D1_FW_VERSION2)

    # -- module ac info
    def read_module_ac_a_phase_voltage(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_A_PHASE_VOLTAGE)

    def read_module_ac_b_phase_voltage(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_B_PHASE_VOLTAGE)

    def read_module_ac_c_phase_voltage(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_C_PHASE_VOLTAGE)

    def read_module_ac_a_phase_current(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_A_PHASE_CURRENT)

    def read_module_ac_b_phase_current(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_B_PHASE_CURRENT)

    def read_module_ac_c_phase_current(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_C_PHASE_CURRENT)

    def read_module_ac_frequency(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_FREQUENCY)

    def read_module_ac_a_phase_active_power(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_A_PHASE_ACTIVE_POWER)

    def read_module_ac_b_phase_active_power(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_B_PHASE_ACTIVE_POWER)

    def read_module_ac_c_phase_active_power(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_AC_C_PHASE_ACTIVE_POWER)

    def read_module_ac_total_active_power(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_TOTAL_ACTIVE_POWER)

    def read_module_ac_total_reactive_power(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_TOTAL_REACTIVE_POWER)

    def read_module_ac_total_apparent_power(self):
        if not self.is_activated:
            return
        self._read_group_module_ac_info(BEG_READ_D1_TOTAL_APPARENT_POWER)

    # ###### write command functions ###########

    # -- system info
    def write_system_info_dc_voltage(self, f_dc_voltage):
        if not self.is_activated:
            return
        dc_voltage = f_dc_voltage
        dc_voltage = min(dc_voltage, BEG_MAX_DC_VOLTAGE_VALUE)
        dc_voltage = max(dc_voltage, BEG_MIN_DC_VOLTAGE_VALUE)
        dc_milli_voltage = int(dc_voltage * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(dc_milli_voltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_system_info(BEG_WRITE_D1_SYSTEM_DC_VOLTAGE, byte4567)

    def write_system_info_dc_total_current(self, f_dc_current):
        if not self.is_activated:
            return
        dc_current = f_dc_current
        # dc_current = min(dc_current, BEG_MAX_DC_CURRENT_VALUE)
        dc_current = max(dc_current, BEG_MIN_DC_CURRENT_VALUE)
        dc_milli_current = int(dc_current * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(dc_milli_current.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_system_info(BEG_WRITE_D1_SYSTEM_DC_CURRENT, byte4567)

    # -- module info
    def write_module_info_dc_voltage(self, f_dc_voltage):
        if not self.is_activated:
            return
        dc_voltage = f_dc_voltage
        dc_voltage = min(dc_voltage, BEG_MAX_DC_VOLTAGE_VALUE)
        dc_voltage = max(dc_voltage, BEG_MIN_DC_VOLTAGE_VALUE)
        dc_milli_voltage = int(dc_voltage * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(dc_milli_voltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_info(BEG_WRITE_D1_POWER_MODULE_SIDE_VOLTAGE, byte4567)

    def write_module_info_dc_current(self, f_dc_current):
        if not self.is_activated:
            return
        dc_current = f_dc_current
        dc_current = min(dc_current, BEG_MAX_DC_CURRENT_VALUE)
        dc_current = max(dc_current, BEG_MIN_DC_CURRENT_VALUE)
        dc_milli_current = int(dc_current * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(dc_milli_current.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_info(BEG_WRITE_D1_POWER_MODULE_SIDE_CURRENT, byte4567)

    def write_module_info_control_on(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_ON_VALUE]
        self._write_group_module_info(BEG_WRITE_D1_MODULE_ON_OFF, byte4567)

    def write_module_info_control_off(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_OFF_VALUE]
        self._write_group_module_info(BEG_WRITE_D1_MODULE_ON_OFF, byte4567)

    def write_module_info_walk_in_enable(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_WALKIN_ENABLE]
        self._write_group_module_info(BEG_WRITE_D1_WALKIN_ENABLE, byte4567)

    def write_module_info_walk_in_disable(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_WALKIN_DISABLE]
        self._write_group_module_info(BEG_WRITE_D1_WALKIN_ENABLE, byte4567)

    def write_module_info_sleep_on(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_SLEEP_VALUE]
        self._write_group_module_info(BEG_WRITE_D1_SLEEP, byte4567)

    def write_module_info_sleep_off(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_NOT_SLEEP_VALUE]
        self._write_group_module_info(BEG_WRITE_D1_SLEEP, byte4567)

    def write_module_info_green_led_blink(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_GREEN_LED_BLINK]
        self._write_group_module_info(BEG_WRITE_D1_GREEN_LED_BLINK, byte4567)

    def write_module_info_green_led_normal(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_GREEN_LED_NORMAL]
        self._write_group_module_info(BEG_WRITE_D1_GREEN_LED_BLINK, byte4567)

    # -- module ac info
    def write_module_ac_info_working_mode_rectification(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_WORKING_MODE_RECTIFICATION]
        self._write_group_module_ac_info(BEG_WRITE_D1_WORKING_MODE, byte4567)

    def write_module_ac_info_working_mode_inverter(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_WORKING_MODE_INVERTER]
        self._write_group_module_ac_info(BEG_WRITE_D1_WORKING_MODE, byte4567)

    def write_module_ac_info_working_mode_inverter_off_grid(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_WORKING_MODE_INVERTER_OFF_GRID]
        self._write_group_module_ac_info(BEG_WRITE_D1_WORKING_MODE, byte4567)

    def write_module_ac_info_level1_ov_protection_time(self, sec):
        if not self.is_activated:
            return
        msec_ = int(sec * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(msec_.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L1_OV_PROTECTION_TIME, byte4567)

    def write_module_ac_info_level2_ov_protection_time(self, sec):
        if not self.is_activated:
            return
        msec_ = int(sec * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(msec_.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L2_OV_PROTECTION_TIME, byte4567)

    def write_module_ac_info_level1_lv_protection_time(self, sec):
        if not self.is_activated:
            return
        msec_ = int(sec * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(msec_.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L1_LV_PROTECTION_TIME, byte4567)

    def write_module_ac_info_level2_lv_protection_time(self, sec):
        if not self.is_activated:
            return
        msec_ = int(sec * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(msec_.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L2_LV_PROTECTION_TIME, byte4567)

    def write_module_ac_info_level1_lv_protection_voltage(self, voltage):
        if not self.is_activated:
            return
        mvoltage = int(voltage * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(mvoltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L1_LV_PROTECTION_VOLTAGE, byte4567)

    def write_module_ac_info_level2_lv_protection_voltage(self, voltage):
        if not self.is_activated:
            return
        mvoltage = int(voltage * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(mvoltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L2_LV_PROTECTION_VOLTAGE, byte4567)

    def write_module_ac_info_level1_ov_protection_voltage(self, voltage):
        if not self.is_activated:
            return
        mvoltage = int(voltage * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(mvoltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L1_OV_PROTECTION_VOLTAGE, byte4567)

    def write_module_ac_info_level2_ov_protection_voltage(self, voltage):
        if not self.is_activated:
            return
        mvoltage = int(voltage * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(mvoltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_L2_OV_PROTECTION_VOLTAGE, byte4567)

    def write_module_ac_info_allow_wrong_phase_on(self):
        if not self.is_activated:
            return
        byte4567 = [0, 0, 0, BEG_MODULE_ALLOW_WRONG_PHASE_ON]
        self._write_group_module_ac_info(BEG_WRITE_D1_ALLOW_WRONG_PHASE, byte4567)

    def write_module_ac_info_rated_phase_voltage(self, phase_vo):
        if not self.is_activated:
            return
        phase_vo_milli = int(phase_vo * BEG_SCALE_MILLI_VOLTAGE)
        byte4567 = list(phase_vo_milli.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
        self._write_group_module_ac_info(BEG_WRITE_D1_RATED_PHASE_VOLTAGE, byte4567)

    # ###### write single command functions ###########

    # -- module info
    def write_single_module_info_dc_voltage(self, module_no, f_dc_voltage):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            dc_voltage = f_dc_voltage
            dc_voltage = min(dc_voltage, BEG_MAX_DC_VOLTAGE_VALUE)
            dc_voltage = max(dc_voltage, BEG_MIN_DC_VOLTAGE_VALUE)
            dc_milli_voltage = int(dc_voltage * BEG_SCALE_MILLI_VOLTAGE)
            byte4567 = list(dc_milli_voltage.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
            self._write_single_module_info(module_no, BEG_WRITE_D1_POWER_MODULE_SIDE_VOLTAGE, byte4567)

    def write_single_module_info_dc_current(self, module_no, f_dc_current):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            dc_current = f_dc_current
            dc_current = min(dc_current, BEG_MAX_DC_CURRENT_VALUE)
            dc_current = max(dc_current, BEG_MIN_DC_CURRENT_VALUE)
            dc_milli_current = int(dc_current * BEG_SCALE_MILLI_VOLTAGE)
            byte4567 = list(dc_milli_current.to_bytes(BEG_INT_TO_BYTE_LENGTH, byteorder="big"))
            self._write_single_module_info(module_no, BEG_WRITE_D1_POWER_MODULE_SIDE_CURRENT, byte4567)

    def write_single_module_info_control_on(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_ON_VALUE]
            self._write_single_module_info(module_no, BEG_WRITE_D1_MODULE_ON_OFF, byte4567)

    def write_single_module_info_control_off(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_OFF_VALUE]
            self._write_single_module_info(module_no, BEG_WRITE_D1_MODULE_ON_OFF, byte4567)

    def write_single_module_info_work_in_enable(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_WALKIN_ENABLE]
            self._write_single_module_info(module_no, BEG_WRITE_D1_WALKIN_ENABLE, byte4567)

    def write_single_module_info_work_in_disable(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_WALKIN_DISABLE]
            self._write_single_module_info(module_no, BEG_WRITE_D1_WALKIN_ENABLE, byte4567)

    def write_single_module_info_sleep_on(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_SLEEP_VALUE]
            self._write_single_module_info(module_no, BEG_WRITE_D1_SLEEP, byte4567)

    def write_single_module_info_sleep_off(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_NOT_SLEEP_VALUE]
            self._write_single_module_info(module_no, BEG_WRITE_D1_SLEEP, byte4567)

    def write_single_module_info_green_led_blink(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_GREEN_LED_BLINK]
            self._write_single_module_info(module_no, BEG_WRITE_D1_GREEN_LED_BLINK, byte4567)

    def write_single_module_info_green_led_normal(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_GREEN_LED_NORMAL]
            self._write_single_module_info(module_no, BEG_WRITE_D1_GREEN_LED_BLINK, byte4567)

    # -- module ac info
    def write_single_module_ac_info_working_mode_rectification(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_WORKING_MODE_RECTIFICATION]
            self._write_single_module_ac_info(module_no, BEG_WRITE_D1_WORKING_MODE, byte4567)

    def write_single_module_ac_info_working_mode_inverter(self, module_no):
        if not self.is_activated:
            return
        if module_no in self.dict_param.keys():
            byte4567 = [0, 0, 0, BEG_MODULE_WORKING_MODE_INVERTER]
            self._write_single_module_ac_info(module_no, BEG_WRITE_D1_WORKING_MODE, byte4567)

    # ###### process functions ###########

    def _data_array_to_float(self, data_array):
        mvol = int.from_bytes(data_array[4:], byteorder='big', signed=True)
        return float(mvol) / 1000.0

    def process(self, frame):
        if (not self.is_activated) or (frame is None):
            return
        self._read_process_for_module(frame)
        self._read_process_for_group(frame)

    def init_status_alarm(self, module_no):
        self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE7] = 0
        self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE6] = 0
        self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE5] = 0

    def init_status_param(self, module_no):
        self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE7] = 0
        self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE6] = 0
        self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE5] = 0
        self.dict_param[module_no].inverter_status[BEG_DATA_INFO_BYTE7] = 0
        self.process_for_status(module_no)
        self.dict_param[module_no].ac_frequency = 0.0
        self.dict_param[module_no].ac_a_phase_voltage = 0.0
        self.dict_param[module_no].ac_b_phase_voltage = 0.0
        self.dict_param[module_no].ac_c_phase_voltage = 0.0
        self.dict_param[module_no].ac_a_phase_current = 0.0
        self.dict_param[module_no].ac_b_phase_current = 0.0
        self.dict_param[module_no].ac_c_phase_current = 0.0

    def process_for_status(self, module_no):
        if not (module_no in self.dict_param.keys()):
            print("There is no module with no:{}".format(module_no))
            return
        status0 = self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE7]
        status1 = self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE6]
        status2 = self.dict_param[module_no].power_module_status[BEG_DATA_INFO_BYTE5]
        status3 = self.dict_param[module_no].inverter_status[BEG_DATA_INFO_BYTE7]
        alarm_status = self.dict_param[module_no].alarm_status

        self.dict_param[module_no].alarm_code = status0 & 0x31
        self.dict_param[module_no].alarm_code += ((status1 & 0xBE) << 8)
        self.dict_param[module_no].alarm_code += ((status2 & 0x7F) << 8)

        if self.dict_param[module_no].alarm_code > 0:
            self.dict_param[module_no].alarm = True
        else:
            self.dict_param[module_no].alarm = False

        # inverter status 0
        alarm_status.inverter_mode = (status3 >> 0) & 0x01  # inverter mode
        alarm_status.rectifier_mode = not self.dict_param[module_no].alarm_status.inverter_mode  # rectification mode
        # module status 2
        alarm_status.mdl_pfc_side_off = (status2 >> 7) & 0x01  # Mdl PFC side off
        alarm_status.input_over_voltage_protection = (status2 >> 6) & 0x01  # input over voltage protection
        alarm_status.input_low_voltage_alarm = (status2 >> 5) & 0x01  # input low voltage alarm
        alarm_status.three_phase_input_unbalance_alarm = (status2 >> 4) & 0x01  # 3 phase input unbalance alarm
        alarm_status.three_phase_input_phase_lost_alarm = (status2 >> 3) & 0x01  # 3 phase input phase lost alarm
        alarm_status.mdl_load_sharing_alarm = (status2 >> 2) & 0x01  # Mdl load sharing alarm
        alarm_status.mdl_id_repeat_alarm = (status2 >> 1) & 0x01  # Mdl ID repeat alarm
        alarm_status.mdl_power_limit_status = (status2 >> 0) & 0x01  # Mdl power limit status
        # module status 1
        alarm_status.mdl_communication_interrupt_alarm = (status1 >> 7) & 0x01  # Mdl communication interrupt alarm
        alarm_status.mdl_walk_in_enable = (status1 >> 6) & 0x01  # WALK-IN enable
        alarm_status.output_over_voltage_alarm = (status1 >> 5) & 0x01  # output over voltage alarm
        alarm_status.over_temperature_alarm = (status1 >> 4) & 0x01  # over temperature alarm
        alarm_status.fan_fault_alarm = (status1 >> 3) & 0x01  # Mdl fan alarm
        alarm_status.mdl_protection_alarm = (status1 >> 2) & 0x01  # Mdl protection alarm
        alarm_status.mdl_fault_alarm = (status1 >> 1) & 0x01  # Mdl fault alarm
        alarm_status.mdl_dc_side_off_status = (status1 >> 0) & 0x01  # Mdl DC side off status
        # module status 0
        alarm_status.mdl_discharge_abnormal = (status0 >> 5) & 0x01  # Mdl discharge abnormal
        alarm_status.mdl_sleeping = (status0 >> 4) & 0x01  # Mdl sleeping
        alarm_status.mdl_output_short_current = (status0 >> 0) & 0x01  # output short current

    def _read_process_for_group(self, frame):
        errcode, dev_no, cmd_no, destaddr, srcaddr = self.identifier.parsing_identifier(frame.id)
        if errcode == BEG_ID_ERROR_CODE_NORMAL:
            if dev_no == BEG_ID_DEVICE_NO_GROUP_MODULE:
                if cmd_no == BEG_ID_COMMAND_NO_READ:
                    if destaddr == BEG_ID_SOURCE_DEFAULT_ADDRESS:
                        if srcaddr == self.group_address:
                            self._read_process_details_for_group(frame)

    def _read_process_details_for_group(self, frame):
        data_list = self.can_obj.data_list(frame)
        if not len(data_list):
            return
        if data_list[BEG_DATA_INFO_BYTE0] == BEG_COMMAND_SUB_BYTE0_SYSTEM_BASIC_INFO:
            if data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_POWER_MODULE_NUMBER:
                self.group_power_module_numbers_of_group = data_list[BEG_DATA_INFO_BYTE7]
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_SYSTEM_DC_SIDE_VOLTAGE:
                self.group_dc_side_voltage = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_SYSTEM_DC_SIDE_CURRENT:
                self.group_dc_side_total_current = self._data_array_to_float(frame.data)

    def _read_process_for_module(self, frame):
        errcode, dev_no, cmd_no, destaddr, srcaddr = self.identifier.parsing_identifier(frame.id)
        if errcode == BEG_ID_ERROR_CODE_NORMAL:
            if dev_no == BEG_ID_DEVICE_NO_GROUP_MODULE:
                if cmd_no == BEG_ID_COMMAND_NO_READ:
                    if destaddr == BEG_ID_SOURCE_DEFAULT_ADDRESS:
                        if srcaddr in self.dict_param.keys():
                            self.dict_param[srcaddr].read_identifier = frame.id
                            self.dict_param[srcaddr].rx_count += 1
                            self._read_process_details_for_module(srcaddr, frame)

    def _read_process_details_for_module(self, module_no, frame):
        data_list = self.can_obj.data_list(frame)
        if not len(data_list):
            return
        if data_list[BEG_DATA_INFO_BYTE0] == BEG_COMMAND_SUB_BYTE0_SINGLE_PM_BASIC:
            if data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_POWER_MODULE_SIDE_VOLTAGE:
                self.dict_param[module_no].power_module_dc_side_voltage = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_POWER_MODULE_SIDE_CURRENT:
                self.dict_param[module_no].power_module_dc_side_current = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_TEMPERATURE:
                self.dict_param[module_no].power_module_temperature = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_STATUS:
                self.dict_param[module_no].power_module_status = self.can_obj.data_list(frame)
                self.process_for_status(module_no)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_INVERTER_STATUS:
                self.dict_param[module_no].inverter_status = self.can_obj.data_list(frame)
                self.process_for_status(module_no)
            elif data_list[BEG_DATA_INFO_BYTE1] == REG_READ_D1_MODULE_GROUP_NUMBER:
                data = self.can_obj.data_list(frame)
                self.dict_param[module_no].module_group_number = data[BEG_DATA_INFO_BYTE7]
        elif data_list[BEG_DATA_INFO_BYTE0] == BEG_COMMAND_SUB_BYTE0_SINGLE_PM_AC_SIDE:
            if data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_A_PHASE_VOLTAGE:
                self.dict_param[module_no].ac_a_phase_voltage = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_B_PHASE_VOLTAGE:
                self.dict_param[module_no].ac_b_phase_voltage = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_C_PHASE_VOLTAGE:
                self.dict_param[module_no].ac_c_phase_voltage = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_A_PHASE_CURRENT:
                self.dict_param[module_no].ac_a_phase_current = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_B_PHASE_CURRENT:
                self.dict_param[module_no].ac_b_phase_current = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_C_PHASE_CURRENT:
                self.dict_param[module_no].ac_c_phase_current = self._data_array_to_float(frame.data)
            elif data_list[BEG_DATA_INFO_BYTE1] == BEG_READ_D1_AC_FREQUENCY:
                self.dict_param[module_no].ac_frequency = self._data_array_to_float(frame.data)
