
from common.App_Header import *
from interface.HMI_Header import *
from interface.DEV_Interface import DEV_Interface
from interface.SBMS_Interface import SBMS_Interface
from controller.EVSE import EVSE
from controller.HMI_Updater import HMI_Updater


class HMI_Interface:
    def __init__(self):
        self.hmi_param = HMI_Param()
        self.updater = HMI_Updater()

    #######################
    # porting c code functions
    #######################
    def Init(self, evse: EVSE, dev: DEV_Interface, sbms: SBMS_Interface):
        self.evse = evse
        self.dev = dev
        self.sbms = sbms

    def SendScuStatus(self):
        self.hmi_param.scu_status.scuHeartbeat += 1
        self.hmi_param.scu_status.scuGroupNo_DCDC = APP_CEG_GROUP_NO
        self.hmi_param.scu_status.scuModuleCount_InGroup_DCDC = APP_CEG_MODULE_COUNT
        self.hmi_param.scu_status.scuVersionMajor = APP_VERSION_MAJOR
        self.hmi_param.scu_status.scuVersionMinor = APP_VERSION_MINOR
        self.updater.SendDataFrame(HMI_ID_SCU_STATUS1, self.hmi_param.scu_status.ByteArray())

    def SendScuEVStatus(self):
        soc = self.evse.GetEVPresentSOC_100mP()
        voltage = self.evse.GetEVPresentVoltage_100mV()
        current = self.evse.GetEVPresentCurrent_100mA()
        temperature0 = self.evse.GetDCPresentTemperature(APP_CEG_MODULE0_ID)
        temperature1 = self.evse.GetDCPresentTemperature(APP_CEG_MODULE1_ID)
        self.hmi_param.ev_status.evSOC = soc
        self.hmi_param.ev_status.evPresentVoltage = voltage
        self.hmi_param.ev_status.evPresentCurrent = current
        self.hmi_param.ev_status.dcdcTemperature_0 = temperature0
        self.hmi_param.ev_status.dcdcTemperature_1 = temperature1
        self.updater.SendDataFrame(HMI_ID_SCU_EV_STATUS, self.hmi_param.ev_status.ByteArray())

    def SendScuBATStatus(self):
        soc = self.sbms.SBMS_GetBatterySOC()
        voltage = self.sbms.SBMS_GetBatteryVoltage()
        current = self.sbms.SBMS_GetBatteryCurrent()
        self.hmi_param.bat_status.batSOC = soc
        self.hmi_param.bat_status.batPresentVoltage = voltage
        self.hmi_param.bat_status.batPresentCurrent = current
        self.updater.SendDataFrame(HMI_ID_SCU_BAT_STATUS, self.hmi_param.bat_status.ByteArray())

    def SendScuErrorCode(self):
        self.updater.SendDataFrame(HMI_ID_SCU_ERROR_CODE, self.hmi_param.scu_ecode.ByteArray())

    def SendScuCHGParam1(self):
        self.updater.SendDataFrame(HMI_ID_SCU_CHG_PARAMETERS1, self.hmi_param.chg_param1.ByteArray())

    def SendScuCHGParam2(self):
        self.updater.SendDataFrame(HMI_ID_SCU_CHG_PARAMETERS2, self.hmi_param.chg_param2.ByteArray())

    def SendScuDCPresentOutput(self):
        voltage = self.evse.GetDCPresentVoltage_mV()
        current = self.evse.GetDCPresentCurrent_mA()
        self.hmi_param.scu_group_dc_out.dcdcPresentVoltage = voltage
        self.hmi_param.scu_group_dc_out.dcdcPresentCurrent = current
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC_PRESENT_VOLT_CURR, self.hmi_param.scu_group_dc_out.ByteArray())

    def SendScuDCDC1Status1(self):
        self.hmi_param.scu_dc1_status1.dcdcModuleNo = APP_CEG_MODULE0_ID
        self.hmi_param.scu_dc1_status1.dcdcAlarm = self.evse.GetDCAlarm(APP_CEG_MODULE0_ID)
        alarm_code = self.evse.GetDCAlarmCode(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc1_status1.dcdcAlarmCode[0] = (alarm_code >> 0) & 0xFF
        self.hmi_param.scu_dc1_status1.dcdcAlarmCode[1] = (alarm_code >> 8) & 0xFF
        self.hmi_param.scu_dc1_status1.dcdcAlarmCode[2] = (alarm_code >> 16) & 0xFF
        self.hmi_param.scu_dc1_status1.dcdcStatus_DCsideOff = self.evse.GetDCSideOFF(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc1_status1.dcdcStatus_walkinEnable = self.evse.GetDCWalkInEnable(APP_CEG_MODULE0_ID)
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC1_STATUS1, self.hmi_param.scu_dc1_status1.ByteArray())

    def SendScuDCDC1Status2(self):
        temperature = self.evse.GetDCPresentTemperature_mT(APP_CEG_MODULE0_ID)
        voltage = self.evse.GetDCInputVoltage_mV(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc1_status2.dcdcPresentTemperature = temperature
        self.hmi_param.scu_dc1_status2.dcdcInputVoltage = voltage
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC1_STATUS2, self.hmi_param.scu_dc1_status2.data)

    def SendScuDCDC1Output(self):
        voltage = self.evse.GetDCOutputVoltage_mV(APP_CEG_MODULE0_ID)
        current = self.evse.GetDCOutputCurrent_mA(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc1_output.dcdcOutputVoltage = voltage
        self.hmi_param.scu_dc1_output.dcdcOutputCurrent = current
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC1_INPUT_VOLTAGE, self.hmi_param.scu_dc1_output.ByteArray())

    def SendScuDCDC2Status1(self):
        self.hmi_param.scu_dc2_status1.dcdcModuleNo = APP_CEG_MODULE1_ID
        self.hmi_param.scu_dc2_status1.dcdcAlarm = self.evse.GetDCAlarm(APP_CEG_MODULE1_ID)
        alarm_code = self.evse.GetDCAlarmCode(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc2_status1.dcdcAlarmCode[0] = (alarm_code >> 0) & 0xFF
        self.hmi_param.scu_dc2_status1.dcdcAlarmCode[1] = (alarm_code >> 8) & 0xFF
        self.hmi_param.scu_dc2_status1.dcdcAlarmCode[2] = (alarm_code >> 16) & 0xFF
        self.hmi_param.scu_dc2_status1.dcdcStatus_DCsideOff = self.evse.GetDCSideOFF(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc2_status1.dcdcStatus_walkinEnable = self.evse.GetDCWalkInEnable(APP_CEG_MODULE1_ID)
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC2_STATUS1, self.hmi_param.scu_dc2_status1.ByteArray())

    def SendScuDCDC2Status2(self):
        temperature = self.evse.GetDCPresentTemperature_mT(APP_CEG_MODULE1_ID)
        voltage = self.evse.GetDCInputVoltage_mV(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc2_status2.dcdcPresentTemperature = temperature
        self.hmi_param.scu_dc2_status2.dcdcInputVoltage = voltage
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC2_STATUS2, self.hmi_param.scu_dc2_status2.data)

    def SendScuDCDC2Output(self):
        voltage = self.evse.GetDCOutputVoltage_mV(APP_CEG_MODULE1_ID)
        current = self.evse.GetDCOutputCurrent_mA(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc2_output.dcdcOutputVoltage = voltage
        self.hmi_param.scu_dc2_output.dcdcOutputCurrent = current
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC2_INPUT_VOLTAGE, self.hmi_param.scu_dc2_output.ByteArray())

    def SendScuDCDC3Status1(self):  # TEST_Code
        self.hmi_param.scu_dc3_status1.dcdcModuleNo = APP_CEG_MODULE0_ID
        self.hmi_param.scu_dc3_status1.dcdcAlarm = self.evse.GetDCAlarm(APP_CEG_MODULE0_ID)
        alarm_code = self.evse.GetDCAlarmCode(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc3_status1.dcdcAlarmCode[0] = (alarm_code >> 0) & 0xFF
        self.hmi_param.scu_dc3_status1.dcdcAlarmCode[1] = (alarm_code >> 8) & 0xFF
        self.hmi_param.scu_dc3_status1.dcdcAlarmCode[2] = (alarm_code >> 16) & 0xFF
        self.hmi_param.scu_dc3_status1.dcdcStatus_DCsideOff = self.evse.GetDCSideOFF(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc3_status1.dcdcStatus_walkinEnable = self.evse.GetDCWalkInEnable(APP_CEG_MODULE0_ID)
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC3_STATUS1, self.hmi_param.scu_dc3_status1.ByteArray())

    def SendScuDCDC3Status2(self):  # TEST_Code
        temperature = self.evse.GetDCPresentTemperature_mT(APP_CEG_MODULE0_ID)
        voltage = self.evse.GetDCInputVoltage_mV(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc3_status2.dcdcPresentTemperature = temperature
        self.hmi_param.scu_dc3_status2.dcdcInputVoltage = voltage
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC3_STATUS2, self.hmi_param.scu_dc3_status2.data)

    def SendScuDCDC3Output(self):  # TEST_Code
        voltage = self.evse.GetDCOutputVoltage_mV(APP_CEG_MODULE0_ID)
        current = self.evse.GetDCOutputCurrent_mA(APP_CEG_MODULE0_ID)
        self.hmi_param.scu_dc3_output.dcdcOutputVoltage = voltage
        self.hmi_param.scu_dc3_output.dcdcOutputCurrent = current
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC3_INPUT_VOLTAGE, self.hmi_param.scu_dc3_output.ByteArray())

    def SendScuDCDC4Status1(self):  # TEST_Code
        self.hmi_param.scu_dc4_status1.dcdcModuleNo = APP_CEG_MODULE1_ID
        self.hmi_param.scu_dc4_status1.dcdcAlarm = self.evse.GetDCAlarm(APP_CEG_MODULE1_ID)
        alarm_code = self.evse.GetDCAlarmCode(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc4_status1.dcdcAlarmCode[0] = (alarm_code >> 0) & 0xFF
        self.hmi_param.scu_dc4_status1.dcdcAlarmCode[1] = (alarm_code >> 8) & 0xFF
        self.hmi_param.scu_dc4_status1.dcdcAlarmCode[2] = (alarm_code >> 16) & 0xFF
        self.hmi_param.scu_dc4_status1.dcdcStatus_DCsideOff = self.evse.GetDCSideOFF(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc4_status1.dcdcStatus_walkinEnable = self.evse.GetDCWalkInEnable(APP_CEG_MODULE1_ID)
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC4_STATUS1, self.hmi_param.scu_dc4_status1.ByteArray())

    def SendScuDCDC4Status2(self):  # TEST_Code
        temperature = self.evse.GetDCPresentTemperature_mT(APP_CEG_MODULE1_ID)
        voltage = self.evse.GetDCInputVoltage_mV(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc4_status2.dcdcPresentTemperature = temperature
        self.hmi_param.scu_dc4_status2.dcdcInputVoltage = voltage
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC4_STATUS2, self.hmi_param.scu_dc4_status2.data)

    def SendScuDCDC4Output(self):  # TEST_Code
        voltage = self.evse.GetDCOutputVoltage_mV(APP_CEG_MODULE1_ID)
        current = self.evse.GetDCOutputCurrent_mA(APP_CEG_MODULE1_ID)
        self.hmi_param.scu_dc4_output.dcdcOutputVoltage = voltage
        self.hmi_param.scu_dc4_output.dcdcOutputCurrent = current
        self.updater.SendDataFrame(HMI_ID_SCU_DCDC4_INPUT_VOLTAGE, self.hmi_param.scu_dc4_output.ByteArray())

    def SendMonData100ms_count(self):
        if self.hmi_param.hmi_conf.hmiRunMode == APP_RUN_MODE_DCDC_TEST: return

        count = self.hmi_param.mon_send_count
        if count == HMI_MON_STATUS1:
            self.SendScuStatus()
        elif count == HMI_MON_EV_STATUS:
            self.SendScuEVStatus()
        elif count == HMI_MON_BAT_STATUS:
            self.SendScuBATStatus()
        elif count == HMI_MON_ERROR_CODE:
            self.SendScuErrorCode()
        elif count == HMI_MON_CHG_PARAM1:
            self.SendScuCHGParam1()
        elif count == HMI_MON_CHG_PARAM2:
            self.SendScuCHGParam2()

        count += 1
        if count >= HMI_MON_END:
            count = 0
        self.hmi_param.mon_send_count = count

    def SendMonData100ms_count_InDCtestMode(self):
        if self.hmi_param.hmi_conf.hmiRunMode != APP_RUN_MODE_DCDC_TEST: return

        count = self.hmi_param.mon_send_count
        if count == HMI_DCDC_MON_STATUS1:
            self.SendScuStatus()
        elif count == HMI_DCDC_MON_DCDC_PRESENT:
            self.SendScuDCPresentOutput()
        elif count == HMI_DCDC_MON_DCDC1_STATUS1:
            self.SendScuDCDC1Status1()
        elif count == HMI_DCDC_MON_DCDC1_STATUS2:
            self.SendScuDCDC1Status2()
        elif count == HMI_DCDC_MON_DCDC1_OUTPUT:
            self.SendScuDCDC1Output()
        elif count == HMI_DCDC_MON_DCDC2_STATUS1:
            self.SendScuDCDC2Status1()
        elif count == HMI_DCDC_MON_DCDC2_STATUS2:
            self.SendScuDCDC2Status2()
        elif count == HMI_DCDC_MON_DCDC2_OUTPUT:
            self.SendScuDCDC2Output()
        elif count == HMI_DCDC_MON_DCDC3_STATUS1:  # TEST_Code
            self.SendScuDCDC3Status1()
        elif count == HMI_DCDC_MON_DCDC3_STATUS2:  # TEST_Code
            self.SendScuDCDC3Status2()
        elif count == HMI_DCDC_MON_DCDC3_OUTPUT:  # TEST_Code
            self.SendScuDCDC3Output()
        elif count == HMI_DCDC_MON_DCDC4_STATUS1:  # TEST_Code
            self.SendScuDCDC4Status1()
        elif count == HMI_DCDC_MON_DCDC4_STATUS2:  # TEST_Code
            self.SendScuDCDC4Status2()
        elif count == HMI_DCDC_MON_DCDC4_OUTPUT:  # TEST_Code
            self.SendScuDCDC4Output()

        count += 1
        if count >= HMI_DCDC_MON_END:
            count = 0
        self.hmi_param.mon_send_count = count

    def RecvDataProcess(self, id_, data_array, byte_array):
        if id_ == HMI_ID_HMI_CONFIGURATIONS:
            self.hmi_param.hmi_conf.Parsing(data_array=data_array, byte_array=byte_array)
        elif id_ == HMI_ID_HMI_STATUS:
            self.hmi_param.hmi_status.Parsing(data_array=data_array, byte_array=byte_array)
        elif id_ == HMI_ID_HMI_TIMESTAMP:
            self.hmi_param.hmi_timestamp.Parsing(data_array=data_array, byte_array=byte_array)
        elif id_ == HMI_ID_HMI_DCDC_TARGET_VOLT_CURR:
            self.hmi_param.hmi_dc_tg.Parsing(data_array=data_array, byte_array=byte_array)
        elif id_ == HMI_ID_HMI_DCDC_STATUS:
            self.hmi_param.hmi_dc_status.Parsing(data_array=data_array, byte_array=byte_array)

    def CheckAlive(self):
        prev_hb = self.hmi_param.prev_heart_beat
        hb = self.hmi_param.hmi_status.hmiHeartbeat

        if prev_hb == hb:
            if self.dev.BCU_Timeout_HMI(HMI_TIMEOUT_HEARTBEAT_MS):
                self.hmi_param.is_activated = HMI_DEACTIVATED
        else:
            self.hmi_param.is_activated = HMI_ACTIVATED
            self.dev.BCU_ResetTimeout_HMI()

    def GetParam(self):
        return self.hmi_param
