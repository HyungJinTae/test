# INFY DC-DC Converter Communication Interface
# written based on REG_IF C Code

import struct
from interface.KVASER_Interface import KVASER_Interface
from interface.CEG_Header import *


class CEG_Group_Interface:
    def __init__(self, can_obj: KVASER_Interface, module_ID_list: [], group_no: int = APP_CEG_GROUP_NO):
        self.is_activated = False
        self.is_demand_activated = False
        self.can_obj = can_obj
        self.group_address = group_no
        self.module_numbers_in_group = 0
        self.group_dc_side_voltage = float(0)
        self.group_dc_side_total_current = float(0)
        self.dict_param = {0: CEG_Module_Demand_Parameters(0)}
        self.SetModuleParameter_Dict(module_ID_list)
        self.identifier = INFY_Identifier()
        self.dummy_data = [0] * 8
        self.demand_response_count = 0
        if self.can_obj.is_connected and self.can_obj.is_opened:
            self.is_activated = True
        log_msg = "[CEG]"
        log_msg += f"Group No -> {self.group_address} |"
        log_msg += f"Module ID -> {self.dict_param.keys()} |"
        log_msg += f"Activated -> {self.is_activated} |"
        logger.info(log_msg)

    def response_parsing_group(self, cmd_no, can_byte_array, can_data_array):
        if cmd_no == CEG_ID_CMD_NO_SYSTEM_OUTPUT_GET:
            [v, c] = struct.unpack('!ff', can_byte_array)
            self.group_dc_side_voltage = v
            self.group_dc_side_total_current = c
        elif cmd_no == CEG_ID_CMD_NO_SYSTEM_MODULE_NUMBER_GET:
            self.module_numbers_in_group = can_data_array[2]

    def response_parsing_module(self, cmd_no, module_ID, can_byte_array, can_data_array):
        module = self.dict_param[module_ID]
        if cmd_no == CEG_ID_CMD_NO_MODULE_OUTPUT_GET:
            [v, c] = struct.unpack('!ff', can_byte_array)
            module.output_voltage = v
            module.output_current = c
        elif cmd_no == CEG_ID_CMD_NO_ALARM_STATE_TEMP_GET:
            module.group_no = can_data_array[2]
            module.temperature = int.from_bytes(can_byte_array[4:5], byteorder='big', signed=True)
            module.state2 = can_data_array[5]
            module.state1 = can_data_array[6]
            module.state0 = can_data_array[7]
            self.alarm_state_parsing(module_ID)
        elif cmd_no == CEG_ID_CMD_NO_MODULE_INPUT_GET:
            module.input_voltage = CEG_FloatFromByteArray(can_byte_array[0:2])
        elif cmd_no == CEG_ID_CMD_NO_MODULE_OUTPUT_MAX_GET:
            module.max_output_voltage = CEG_FloatFromByteArray(can_byte_array[0:2], multiple=1)
            module.min_output_voltage = CEG_FloatFromByteArray(can_byte_array[2:4], multiple=1)
            module.max_output_current = CEG_FloatFromByteArray(can_byte_array[4:6], multiple=0.1)
            module.rated_output_power = CEG_FloatFromByteArray(can_byte_array[6:8], multiple=10)
        elif cmd_no == CEG_ID_CMD_NO_MODULE_DIODE_OUTPUT_GET:
            module.diode_output_voltage = CEG_FloatFromByteArray(can_byte_array[0:2], multiple=0.1)
            module.available_output_current = CEG_FloatFromByteArray(can_byte_array[2:4], multiple=0.1)

    def alarm_state_parsing(self, module_ID):
        module = self.dict_param[module_ID]
        state0 = module.state0
        state1 = module.state1
        state2 = module.state2
        module.alarm_code = state0 & 0x2D
        module.alarm_code += ((state1 & 0xBE) << 8)
        module.alarm_code += ((state2 & 0x7F) << 16)
        module.alarm_state.output_short = CEG_DataToBit(state0, 0)
        module.alarm_state.inner_comm_interrupt = CEG_DataToBit(state0, 2)
        module.alarm_state.pfc_side_abnormal = CEG_DataToBit(state0, 3)
        module.alarm_state.discharge_abnormal = CEG_DataToBit(state0, 4)
        module.alarm_state.dc_side_is_off = CEG_DataToBit(state1, 0)
        module.alarm_state.mdl_fault = CEG_DataToBit(state1, 1)
        module.alarm_state.mdl_protect = CEG_DataToBit(state1, 2)
        module.alarm_state.fan_fault = CEG_DataToBit(state1, 3)
        module.alarm_state.over_temperature = CEG_DataToBit(state1, 4)
        module.alarm_state.output_over_voltage = CEG_DataToBit(state1, 5)
        module.alarm_state.walk_in_enable = CEG_DataToBit(state1, 6)
        module.alarm_state.can_comm_interrupt = CEG_DataToBit(state1, 7)
        module.alarm_state.power_limit = CEG_DataToBit(state2, 0)
        module.alarm_state.mdl_ID_repetition = CEG_DataToBit(state2, 1)
        module.alarm_state.load_unsharing = CEG_DataToBit(state2, 2)
        module.alarm_state.input_phase_lost = CEG_DataToBit(state2, 3)
        module.alarm_state.input_unbalance = CEG_DataToBit(state2, 4)
        module.alarm_state.input_under_voltage = CEG_DataToBit(state2, 5)
        module.alarm_state.input_over_voltage = CEG_DataToBit(state2, 6)
        module.alarm_state.pfc_side_is_off = CEG_DataToBit(state2, 7)

    def SetModuleParameter_Dict(self, module_ID_list: []):
        self.dict_param.clear()
        for module_ID in module_ID_list:
            module_parameter = CEG_Module_Demand_Parameters(module_ID)
            self.dict_param[module_ID] = module_parameter

    def SetDemandEnable(self, enable=True):
        self.is_demand_activated = enable

    def ResponseParsing(self, frame):
        """ can.read """
        if (frame is None) or (not self.is_activated):
            return
        errcode, dev_no, cmd_no, dstaddr, srcaddr = INFY_ParsingIdentifier(frame.id)
        if not (dstaddr == INFY_ID_SOURCE_DEFAULT_ADDRESS):
            return
        if (dev_no == INFY_ID_DEVICE_NO_GROUP_MODULE) and (srcaddr == self.group_address):
            data_array = self.can_obj.data_list(frame)
            self.response_parsing_group(cmd_no, frame.data, data_array)
            self.demand_response_count += 1
        elif (dev_no == INFY_ID_DEVICE_NO_SINGlE_MODULE) and (srcaddr in self.dict_param.keys()):
            data_array = self.can_obj.data_list(frame)
            self.response_parsing_module(cmd_no, srcaddr, frame.data, data_array)
            self.demand_response_count += 1

    def make_identifier(self, command_no,
                        device_no=INFY_ID_DEVICE_NO_GROUP_MODULE,
                        dstaddr=INFY_ID_DESTINATION_DEFAULT_ADDRESS):
        self.identifier.SetErrorCode(INFY_ID_ERROR_CODE_NORMAL)
        self.identifier.SetDeviceNo(device_no)
        self.identifier.SetCommandNo(command_no)
        self.identifier.SetDestinationAddress(dstaddr)
        self.identifier.SetSourceAddress(INFY_ID_SOURCE_DEFAULT_ADDRESS)

    def send_single_set_data(self, module_ID, command_no, data_array):
        self.make_identifier(command_no,
                             dstaddr=module_ID, device_no=INFY_ID_DEVICE_NO_SINGlE_MODULE)
        byte_array = bytearray(data_array)
        # logger.debug("{0:08x}, {1}".format(self.identifier.GetIdentifier(), byte_array))
        self.can_obj.write_wait(id_=self.identifier.GetIdentifier(), data=byte_array)

    def send_group_set_data(self, command_no, data_array):
        self.make_identifier(command_no,
                             dstaddr=self.group_address, device_no=INFY_ID_DEVICE_NO_GROUP_MODULE)
        byte_array = bytearray(data_array)
        self.can_obj.write_wait(id_=self.identifier.GetIdentifier(), data=byte_array)

    def DemandGroup_SystemOutput(self):
        """ Demand System Output Voltage and Current using Group Protocol """
        if not self.is_demand_activated:
            return
        self.send_group_set_data(CEG_ID_CMD_NO_SYSTEM_OUTPUT_GET, self.dummy_data)

    def DemandGroup_ModuleNumber(self):
        """ Demand Module Number using Group Protocol """
        if not self.is_demand_activated:
            return
        self.send_group_set_data(CEG_ID_CMD_NO_SYSTEM_MODULE_NUMBER_GET, self.dummy_data)

    def DemandSingle_Output(self, module_ID):
        if not self.is_demand_activated:
            return
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_OUTPUT_GET, self.dummy_data)

    def DemandSingle_Input(self, module_ID):
        if not self.is_demand_activated:
            return
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_INPUT_GET, self.dummy_data)

    def DemandSingle_MaxOutput(self, module_ID):
        if not self.is_demand_activated:
            return
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_OUTPUT_MAX_GET, self.dummy_data)

    def DemandSingle_DiodeOutput(self, module_ID):
        if not self.is_demand_activated:
            return
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_DIODE_OUTPUT_GET, self.dummy_data)

    def DemandSingle_AlarmStateTemp_Unconditional(self, module_ID):
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_ALARM_STATE_TEMP_GET, self.dummy_data)

    def SetGroup_SystemOutput(self, voltage, total_current):
        if (voltage > CEG_MAX_OUTPUT_VOLTAGE) or (voltage < CEG_MIN_OUTPUT_VOLTAGE):
            logger.warning(f"wrong parameter: voltage({voltage})")
            return
        if (total_current > CEG_MAX_OUTPUT_TOTAL_CURRENT) or (total_current < 0):
            logger.warning(f"wrong parameter: total_current({total_current})")
            return
        # voltage and total current convert to mV, mA data array
        data0123 = CEG_FloatToDataArray(fData=voltage, multiple=1000)
        data4567 = CEG_FloatToDataArray(fData=total_current, multiple=1000)
        data = data0123 + data4567
        self.send_group_set_data(CEG_ID_CMD_NO_SYSTEM_OUTPUT_SET, data)

    def SetGroup_ControlON(self):
        data = [CEG_DEF_CONTROL_ON, 0, 0, 0, 0, 0, 0, 0]
        self.send_group_set_data(CEG_ID_CMD_NO_CONTROL_ON_OFF_SET, data)

    def SetGroup_ControlOFF(self):
        data = [CEG_DEF_CONTROL_OFF, 0, 0, 0, 0, 0, 0, 0]
        self.send_group_set_data(CEG_ID_CMD_NO_CONTROL_ON_OFF_SET, data)

    def SetGroup_WalkInEnable(self):
        data = [CEG_DEF_WALK_IN_ENABLE, 0, 0, 0, 0, 0, 0, 0]
        self.send_group_set_data(CEG_ID_CMD_NO_MODULE_WALK_IN_SET, data)

    def SetGroup_WalkInDisable(self):
        data = [CEG_DEF_WALK_IN_DISABLE, 0, 0, 0, 0, 0, 0, 0]
        self.send_group_set_data(CEG_ID_CMD_NO_MODULE_WALK_IN_SET, data)

    def SetSingle_ControlON(self, module_ID):
        if not (module_ID in self.dict_param.keys()):
            return
        data = [CEG_DEF_CONTROL_ON, 0, 0, 0, 0, 0, 0, 0]
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_CONTROL_ON_OFF_SET, data)

    def SetSingle_ControlOFF(self, module_ID):
        if not (module_ID in self.dict_param.keys()):
            return
        data = [CEG_DEF_CONTROL_OFF, 0, 0, 0, 0, 0, 0, 0]
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_CONTROL_ON_OFF_SET, data)

    def SetSingle_WalkInEnable(self, module_ID):
        if not (module_ID in self.dict_param.keys()):
            return
        data = [CEG_DEF_WALK_IN_ENABLE, 0, 0, 0, 0, 0, 0, 0]
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_WALK_IN_SET, data)

    def SetSingle_WalkInDisable(self, module_ID):
        if not (module_ID in self.dict_param.keys()):
            return
        data = [CEG_DEF_WALK_IN_DISABLE, 0, 0, 0, 0, 0, 0, 0]
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_WALK_IN_SET, data)

    def SetSingle_GreenLedBlink(self, module_ID):
        if not (module_ID in self.dict_param.keys()):
            return
        data = [CEG_DEF_GREEN_LED_BLINK, 0, 0, 0, 0, 0, 0, 0]
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_BLINK_SET, data)

    def SetSingle_GreenLedNormal(self, module_ID):
        if not (module_ID in self.dict_param.keys()):
            return
        data = [CEG_DEF_GREEN_LED_NORMAL, 0, 0, 0, 0, 0, 0, 0]
        self.send_single_set_data(module_ID, CEG_ID_CMD_NO_MODULE_BLINK_SET, data)

    #######################
    # porting c code functions
    #######################
    def Init(self, group_no, module_numbers):
        self.group_address = group_no
        self.SetModuleParameter_Dict(APP_CEG_MODULE_ID_LIST[:module_numbers])
        self.group_dc_side_voltage = 0.0
        self.group_dc_side_total_current = 0.0
        self.module_numbers_in_group = module_numbers
        log_msg = "[CEG_Init]"
        log_msg += f"Group No -> {self.group_address} |"
        log_msg += f"Module ID -> {self.dict_param.keys()} |"
        log_msg += f"Activated -> {self.is_activated} |"
        logger.info(log_msg)

    def PrepareReqGroupModuleNo(self):
        if self.module_numbers_in_group == 0:
            self.module_numbers_in_group = APP_CEG_MODULE_COUNT

    def PrepareRspGroupModuleNo(self):
        if self.is_activated is False:
            if self.module_numbers_in_group > 0:
                for key in self.dict_param.keys():
                    self.InitStatusParam(key)

    def SetActivate(self):
        self.is_demand_activated = CEG_TRUE

    def SetDeactivate(self):
        self.is_demand_activated = CEG_FALSE

    def CheckModuleAddress(self, module_no):
        res = CEG_FALSE
        if self.is_activated and module_no in self.dict_param.keys():
            res = CEG_TRUE
        return res

    def InitStatusParam(self, module_no):
        if not self.is_activated: return

        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            self.dict_param[module_no].state0 = 0
            self.dict_param[module_no].state1 = 0
            self.dict_param[module_no].state2 = 0
            self.alarm_state_parsing(module_no)
            self.dict_param[module_no].alarm_state.dc_side_is_off = CEG_DEF_DC_SIDE_OFF_ON
            self.dict_param[module_no].output_voltage = float(0)
            self.dict_param[module_no].output_current = float(0)
            self.dict_param[module_no].input_voltage = float(0)

    def InitStatusParamAll(self):
        for module_ID in self.dict_param.keys():
            self.InitStatusParam(module_ID)
        self.group_dc_side_voltage = float(0)
        self.group_dc_side_total_current = float(0)

    def WriteGroupDCOutput(self, f_dc_voltage, f_dc_current):
        self.SetGroup_SystemOutput(f_dc_voltage, f_dc_current)

    def WriteGroupControlOn(self, onoff):
        if onoff == CEG_DEF_CONTROL_OFF:
            self.SetGroup_ControlOFF()
        else:
            self.SetGroup_ControlON()

    def WriteGroupWalkIn(self, enable):
        if enable == CEG_DEF_WALK_IN_DISABLE:
            self.SetGroup_WalkInDisable()
        else:
            self.SetGroup_WalkInEnable()

    def WriteModuleControlOn(self, module_no, onoff):
        if onoff == CEG_DEF_CONTROL_ON:
            self.SetSingle_ControlON(module_no)
        else:
            self.SetSingle_ControlOFF(module_no)

    def WriteModuleWalkIn(self, module_no, enable):
        if enable == CEG_DEF_WALK_IN_ENABLE:
            self.SetSingle_WalkInEnable(module_no)
        else:
            self.SetSingle_WalkInDisable(module_no)

    def WriteModuleLedBlink(self, module_no, onoff):
        if onoff == CEG_DEF_GREEN_LED_BLINK:
            self.SetSingle_GreenLedBlink(module_no)
        else:
            self.SetSingle_GreenLedNormal(module_no)

    def GetGroupDCOutVoltage(self):
        return self.group_dc_side_voltage

    def GetGroupDCOutTotalCurrent(self):
        return self.group_dc_side_total_current

    def GetGroupNo(self):
        return self.group_address

    def GetModuleCountInGroup(self):
        return self.module_numbers_in_group

    def GetGroupControlOn(self):
        res = CEG_TRUE
        for module_ID in self.dict_param.keys():
            if self.dict_param[module_ID].alarm_state.dc_side_is_off == CEG_DEF_DC_SIDE_OFF_ON:
                res &= CEG_FALSE
        return res

    def GetGroupWalkInEnable(self):
        res = True
        for module_ID in APP_CEG_MODULE_ID_LIST:
            if not self.GetModuleWalkInEnable(module_ID):
                res &= False
        return res

    def GetGroupAlarm(self):
        res = CEG_FALSE
        for module_ID in self.dict_param.keys():
            if self.dict_param[module_ID].alarm_code > 0:
                res |= CEG_TRUE
        return res

    def GetAlarm(self, module_no):
        res = CEG_FALSE
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            if self.dict_param[module_no].alarm_code > 0:
                res = CEG_TRUE
        return res

    def GetAlarmCode(self, module_no):
        alarm_code = 0
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            alarm_code = self.dict_param[module_no].alarm_code
        return alarm_code

    def GetModuleTemperature(self, module_no):
        temperature = 0
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            temperature = self.dict_param[module_no].temperature
        return temperature

    def GetModuleDCInputVoltage(self, module_no):
        voltage = 0
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            voltage = self.dict_param[module_no].input_voltage
        return voltage

    def GetModuleDCOutputVoltage(self, module_no):
        voltage = 0
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            voltage = self.dict_param[module_no].output_voltage
        return voltage

    def GetModuleDCOutputCurrent(self, module_no):
        current = 0
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            current = self.dict_param[module_no].output_current
        return current

    def GetModuleDCSideOFF(self, module_no):
        dc_side_off = 1
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            dc_side_off = self.dict_param[module_no].alarm_state.dc_side_is_off
        return dc_side_off

    def GetModuleWalkInEnable(self, module_no):
        walk_in = 0
        if self.CheckModuleAddress(module_no) == CEG_TRUE:
            walk_in = self.dict_param[module_no].alarm_state.walk_in_enable
        return walk_in

    def GetParam(self, module_no):
        return self.dict_param[module_no]
