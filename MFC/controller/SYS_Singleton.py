# System level interface class

from common.App_Header import *
from interface.KVASER_Interface import KVASER_Interface
from interface.CEG_Interface import CEG_Group_Interface
from interface.SECC_Interface import SECC_Interface
from interface.DEV_Interface import DEV_Interface
from interface.SBMS_Interface import SBMS_Interface
from interface.SerialCAN_Interface import Serial_Interface, SerialCAN_Interface
from interface.BEG_Group_Interface import BEG_Group_Interface
from network.SockServer import SockServer


class _SYS_Singleton:
    def __init__(self):
        try:
            self.ceg_can = KVASER_Interface(channel=APP_CEG_CAN_CHANNEL_NO, flags=APP_CEG_CAN_FLAG,
                                            bit_rate=APP_CEG_CAN_BIT_RATE)
            self.ceg_can.connect()
            self.ceg_can.open()
            self.secc_can = KVASER_Interface(channel=APP_SECC_CAN_CHANNEL_NO, flags=APP_SECC_CAN_FLAG,
                                             bit_rate=APP_SECC_CAN_BIT_RATE)
            self.secc_can.connect()
            self.secc_can.open()
            self.dev_can = KVASER_Interface(channel=APP_DEVICE_CAN_CHANNEL_NO, flags=APP_DEVICE_CAN_FLAG,
                                            bit_rate=APP_DEVICE_CAN_BIT_RATE)
            self.dev_can.connect()
            self.dev_can.open()
            self.dbg_can = KVASER_Interface(channel=APP_DBG_CAN_CHANNEL_NO, flags=APP_DBG_CAN_FLAG,
                                            bit_rate=APP_DBG_CAN_BIT_RATE)
            self.dbg_can.connect()
            self.dbg_can.open()
            self.sbms_can = self.dev_can
            self.beg_can = self.ceg_can
        except Exception as e:
            logger.warning(f"e->{e}")
        self.ceg = CEG_Group_Interface(self.ceg_can, APP_CEG_MODULE_ID_LIST, APP_CEG_GROUP_NO)
        self.beg = BEG_Group_Interface(self.beg_can, APP_BEG_GROUP_NO)
        self.beg.add_module_list(APP_BEG_MODULE_ID_LIST)
        self.secc = SECC_Interface(self.secc_can)
        self.dev = DEV_Interface(self.dev_can)
        self.sbms = SBMS_Interface(self.sbms_can)
        self.svr = SockServer()

        self.demand_task1_count = 0
        self.demand_task2_count = 0
        self.demand_task2_next_count = 0
        self.demand_task3_count = 0
        self.task1_call_func = [
            self.ceg.DemandGroup_SystemOutput]
        self.task1_call_func_max = len(self.task1_call_func)
        self.task2_call_func = [
            self.ceg.DemandSingle_Output,
            self.ceg.DemandSingle_Input,
            self.ceg.DemandSingle_DiodeOutput,
            self.ceg.DemandSingle_MaxOutput]
        self.task2_call_func_max = len(self.task2_call_func)
        self.task3_call_func = [
            self.beg.read_system_info_dc_voltage,
            self.beg.read_system_info_dc_total_current,
            self.beg.read_module_info_power_module_status,
            self.beg.read_module_info_inverter_status,
            self.beg.read_module_ac_a_phase_voltage,
            self.beg.read_module_ac_a_phase_current,
            self.beg.read_module_ac_b_phase_voltage,
            self.beg.read_module_ac_b_phase_current,
            self.beg.read_module_ac_c_phase_voltage,
            self.beg.read_module_ac_c_phase_current,
            self.beg.read_module_ac_frequency,
            self.beg.read_module_info_temperature
        ]
        self.task3_call_func_max = len(self.task3_call_func)

    def DemandTask1000ms_CEG(self):
        self.ceg.DemandGroup_ModuleNumber()

    def DemandTask100ms_CEG(self):
        """ 100msec period, send system demand (CEG) """
        try:
            func = self.task1_call_func[self.demand_task1_count]
            func()
            self.demand_task1_count += 1
            if self.demand_task1_count >= self.task1_call_func_max:
                self.demand_task1_count = 0
        except Exception as e:
            logger.error(f"e->{e}")

    def DemandTask50ms_CEG(self):
        """ 50msec period, send module demand (CEG) """
        try:
            func = self.task2_call_func[self.demand_task2_count]
            module_ID = self.demand_task2_next_count
            func(module_ID)
            self.ceg.DemandSingle_AlarmStateTemp_Unconditional(module_ID)
            self.demand_task2_next_count += 1
            if self.demand_task2_next_count >= APP_CEG_MODULE_COUNT:
                self.demand_task2_next_count = 0
                self.demand_task2_count += 1
                if self.demand_task2_count >= self.task2_call_func_max:
                    self.demand_task2_count = 0
        except Exception as e:
            logger.error(f"e->{e}")

    def DemandTask50ms_BEG(self):
        """ 50msec period, send module demand (BEG) """
        try:
            func = self.task3_call_func[self.demand_task3_count]
            func()
            self.demand_task3_count += 1
            if self.demand_task3_count >= self.task3_call_func_max:
                self.demand_task3_count = 0
        except Exception as e:
            logger.error(f"e->{e}")

    def Response_Infy(self):
        """ 1msec period (CEG, BEG) """
        frame = self.ceg_can.read()
        self.ceg.ResponseParsing(frame)
        self.beg.process(frame)

    def SECC_SendDebugMessage1(self):
        id_ = APP_CAN_ID_DEBUG_SECC
        tx_data = [0] * 8
        maxV = self.secc.secc_param.secc_chg_param2.f_evMaximumVoltageLimit
        taV = self.secc.secc_param.secc_tg.f_targetVoltage

        tx_data[0] = self.secc.secc_param.secc_status1.seccHeartbeat
        tx_data[1] = self.secc.secc_param.secc_soc.evSOC
        tx_data[2] = self.secc.secc_param.secc_chg_param2.f_evMaximumCurrentLimit
        tx_data[3] = (maxV >> 8) & 0xFF
        tx_data[4] = maxV & 0xFF
        tx_data[5] = self.secc.secc_param.secc_tg.f_targetCurrent
        tx_data[6] = (taV >> 8) & 0xFF
        tx_data[7] = taV & 0xFF
        self.dbg_can.write_wait(id_, bytearray(tx_data))

    def EVSE_SendDebugMessage1(self):
        id_ = APP_CAN_ID_DEBUG_EVSE
        inV = self.ceg.GetModuleDCInputVoltage(APP_CEG_MODULE0_ID)

        self.evse.debug_probe[0] = self.evse.evse_param.is_activated
        self.evse.debug_probe[1] = self.evse.evse_param.hv_relay_state
        self.evse.debug_probe[2] = self.dev.BCU_GetEVHVRelayClosed()
        self.evse.debug_probe[3] = (inV >> 8) & 0xFF
        self.evse.debug_probe[4] = (inV & 0xFF)
        self.dbg_can.write_wait(id_, bytearray(self.evse.debug_probe))


class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class SYS_Singleton(_SYS_Singleton, SingletonInstance):
    pass


TheSys = SYS_Singleton.instance()
