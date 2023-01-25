# SECC (Gridwiz PEPPERMINT) communication interface
# written based on SECC interface C Code

from interface.SECC_Header import *
from interface.KVASER_Interface import KVASER_Interface


class SECC_Interface:
    def __init__(self, can_obj: KVASER_Interface):
        self.is_activated = False
        self.can_obj = can_obj
        if self.can_obj.is_connected and self.can_obj.is_opened:
            self.is_activated = True
        log_msg = "[SECC]"
        log_msg += f"Activated -> {self.is_activated} |"
        logger.info(log_msg)

        self.secc_param = SECC_Parameters()

    #######################
    # porting c code functions
    #######################
    def Init(self):
        self.secc_param.evse_chg_param1.f_evseMaximumCurrentLimit = SECC_MAX_CURRENT_LIMIT
        self.secc_param.evse_chg_param1.f_evseMaximumVoltageLimit = SECC_MAX_VOLTAGE_LIMIT
        self.secc_param.evse_chg_param1.u_evseMaximumPowerLimit = SECC_MAX_POWER_LIMIT
        self.secc_param.evse_chg_param1.f_evsePeakCurrentRipple = 0             # first 0, is DC-DC converter output current precision?

        self.secc_param.evse_chg_param2.f_evseMinimumCurrentLimit = SECC_MIN_CURRENT_LIMIT
        self.secc_param.evse_chg_param2.f_evseMinimumVoltageLimit = SECC_MIN_VOLTAGE_LIMIT
        self.secc_param.evse_chg_param2.f_evseCurrentRegulationTolerance = 0    # if 0, ignore
        self.secc_param.evse_chg_param2.u_evseEnergyToBeDelivered = 0           # if 0, ignore

    def SendEvseConfigurations(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_STATUS, data=self.secc_param.evse_config.ByteArray())

    def SendEvseStatus(self):
        self.secc_param.evse_status.evseHeartbeat += 1
        self.can_obj.write_wait(id_=SECC_ID_EVSE_STATUS, data=self.secc_param.evse_status.ByteArray())

    def SendEvseChgParam1(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_CHARGE_PARAMETERS1,
                                data=self.secc_param.evse_chg_param1.ByteArray())

    def SendEvseChgParam2(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_CHARGE_PARAMETERS2,
                                data=self.secc_param.evse_chg_param2.ByteArray())

    def SendEvsePresVoltCurr(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_PRESENT_VOLT_CURR,
                                data=self.secc_param.evse_volt_curr.ByteArray())

    def EventEvseTimeStamp(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_TIMESTAMP,
                                data=self.secc_param.evse_timestemp.ByteArray())

    def EventEvseSeccReboot(self):
        self.secc_param.evse_reboot.rebootR = SECC_REBOOT_R
        self.secc_param.evse_reboot.rebootE = SECC_REBOOT_E
        self.secc_param.evse_reboot.rebootB = SECC_REBOOT_B
        self.secc_param.evse_reboot.rebootO1 = SECC_REBOOT_O
        self.secc_param.evse_reboot.rebootO2 = SECC_REBOOT_O
        self.secc_param.evse_reboot.rebootT = SECC_REBOOT_T
        self.can_obj.write_wait(id_=SECC_ID_EVSE_SECC_REBOOT,
                                data=self.secc_param.evse_reboot.ByteArray())

    def SendSaAgentConf(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_SA_AGENT_CONN_CONF,
                                data=self.secc_param.secc_saagent_conf.ByteArray())

    def SendEvsePnCConf(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_SECC_PNC_CONF,
                                data=self.secc_param.evse_evsepnc_conf.ByteArray())

    def SendSaAgentCommTimeout(self):
        self.can_obj.write_wait(id_=SECC_ID_EVSE_SA_AGENT_COMM_TIMEOUT,
                                data=self.secc_param.evse_saagent_timeout.ByteArray())

    def RecvSeccProcess(self, id_, data_array, byte_array):
        if id_ == SECC_ID_SECC_STATUS1:
            self.secc_param.secc_status1.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_STATUS2:
            self.secc_param.secc_status2.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EV_SERVICE_SELECTION:
            self.secc_param.secc_sv_sel.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_SESSION_ID:
            self.secc_param.secc_session_id.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EVCC_INFO:
            self.secc_param.secc_evcc_info.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EV_CHG_PARAM1:
            self.secc_param.secc_chg_param1.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EV_CHG_PARAM2:
            self.secc_param.secc_chg_param2.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EV_SOC_RELATED_PARAM:
            self.secc_param.secc_soc.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EV_TGT_VOLTCURR:
            self.secc_param.secc_tg.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_TIMESTAMP:
            self.secc_param.secc_tstamp.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_STATUS3_PNC:
            self.secc_param.secc_status3.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_EMERGENCY_NOTI:
            self.secc_param.secc_emg_noti.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_SA_COMM_STATUS:
            self.secc_param.secc_sa_comm_status.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1
        elif id_ == SECC_ID_SECC_IP_STATUS:
            self.secc_param.secc_ip_status.Parsing(data_array=data_array, byte_array=byte_array)
            self.secc_param.secc_var.rx_count += 1

    def Process1000ms(self):
        self.secc_param.secc_var.secc_activated_check_count += 1
        if self.secc_param.secc_var.secc_activated_check_count >= SECC_ACTIVATED_CHECK_COUNT_MAX:
            self.secc_param.secc_var.secc_activated_check_count = 0
            self.CheckActivate()

    def CheckActivate(self):
        res = SECC_FALSE
        prev_hb = self.secc_param.secc_var.prev_secc_heartbeat
        hb = self.secc_param.secc_status1.seccHeartbeat
        if prev_hb != hb:
            res = SECC_TRUE
        self.secc_param.secc_var.prev_secc_heartbeat = self.secc_param.secc_status1.seccHeartbeat
        self.secc_param.secc_var.is_activated = res

    def IsActivated(self):
        return self.secc_param.secc_var.is_activated

    def GetParam(self) -> SECC_Parameters:
        return self.secc_param

    def SetChargingControl(self, control_mode):
        if control_mode < SECC_CHG_CONTROL_END:
            self.secc_param.evse_status.chargingControl = control_mode

    def SetTimeStamp(self, timestamp):
        self.secc_param.evse_timestemp.evseTimeStamp = timestamp
        self.EventEvseTimeStamp()

    def SetTriggerStateE(self, enable):
        if enable == SECC_DISABLE:
            self.secc_param.evse_status.triggerStateE = SECC_DISABLE
        else:
            self.secc_param.evse_status.triggerStateE = SECC_ENABLE

    def SetReboot(self):
        self.EventEvseSeccReboot()

    def SetControlModeDefault(self):
        self.SetChargingControl(SECC_CHG_CONTROL_NONE)

    def SetInitializePPMT(self):
        self.SetChargingControl(SECC_CHG_CONTROL_INIT_PPMT)

    def SetStartCharging(self):
        self.SetChargingControl(SECC_CHG_CONTROL_START_CHARGING)

    def SetNormalStop(self):
        self.SetChargingControl(SECC_CHG_CONTROL_NORMAL_STOP)

    def SetEmergencyStop(self):
        self.SetChargingControl(SECC_CHG_CONTROL_EMERGENCY_STOP)

    def SetIdleParam(self):
        self.secc_param.evse_config.environmentConfiguration = SECC_DEFAULT

    def SetInitializedParam(self):
        self.secc_param.evse_config.serviceList_HPC1 = SECC_NOT_SUPPORTED
        self.secc_param.evse_config.serviceList_Internet = SECC_NOT_SUPPORTED
        self.secc_param.evse_config.evseIdLength_DIN = 0
        self.secc_param.evse_config.evseIdLength_ISO = 0
        self.secc_param.evse_config.supportedEnergyTransfer_DCcore = SECC_NOT_SUPPORTED
        self.secc_param.evse_config.supportedEnergyTransfer_DCextd = SECC_SUPPORTED
        self.secc_param.evse_config.supportedEnergyTransfer_DCcc = SECC_NOT_SUPPORTED
        self.secc_param.evse_config.supportedEnergyTransfer_DCunique = SECC_NOT_SUPPORTED
        self.secc_param.evse_status.evseIsolationStatus = SECC_ISOL_STATUS_INVALID
        self.secc_param.evse_status.evseProcessing_CPD = SECC_ONGOING
        self.secc_param.evse_status.evseProcessing_CableCheck = SECC_ONGOING
        self.secc_param.evse_status.triggerReNegotiation = SECC_NONE
        self.secc_param.evse_status.evseCurrentLimitAchieved = SECC_FALSE
        self.secc_param.evse_status.evseVoltageLimitAchieved = SECC_FALSE
        self.secc_param.evse_status.evsePowerLimitAchieved = SECC_FALSE

    def SetCableCheckParam_Ongoing(self):
        self.secc_param.evse_status.evseIsolationStatus = SECC_ISOL_STATUS_INVALID
        self.secc_param.evse_status.evseProcessing_CableCheck = SECC_ONGOING
        self.secc_param.evse_status.isolationMonitoringActive = SECC_NOT_ACTIVE     # check it when testing

    def SetCableCheckParam_Finished(self):
        self.secc_param.evse_status.evseIsolationStatus = SECC_ISOL_STATUS_VALID
        self.secc_param.evse_status.evseProcessing_CableCheck = SECC_FINISHED
        self.secc_param.evse_status.isolationMonitoringActive = SECC_ACTIVE

    def SetProcessingAuthEIM(self, finished):
        if finished == SECC_ONGOING:
            self.secc_param.evse_status.evseProcessing_AuthEIM = SECC_ONGOING
        else:
            self.secc_param.evse_status.evseProcessing_AuthEIM = SECC_FINISHED

    def SetProcessingCPD(self, finished):
        if finished == SECC_ONGOING:
            self.secc_param.evse_status.evseProcessing_CPD = SECC_ONGOING
        else:
            self.secc_param.evse_status.evseProcessing_CPD = SECC_FINISHED

    def SetTriggerReNegotiation(self, re_nego):
        if re_nego == SECC_DEFAULT:
            self.secc_param.evse_status.triggerReNegotiation = SECC_DEFAULT
        else:
            self.secc_param.evse_status.triggerReNegotiation = SECC_REQ_RE_NEGO

    def SetPresentVoltage(self, f_voltage):
        self.secc_param.evse_volt_curr.f_evsePresentVoltage = f_voltage

    def SetPresentCurrent(self, f_current):
        self.secc_param.evse_volt_curr.f_evsePresentCurrent = f_current

    def SetCurrentLimitAchieved(self, achieved):
        self.secc_param.evse_status.evseCurrentLimitAchieved = achieved

    def SetVoltageLimitAchieved(self, achieved):
        self.secc_param.evse_status.evseCurrentLimitAchieved = achieved

    def SetPowerLimitAchieved(self, achieved):
        self.secc_param.evse_status.evsePowerLimitAchieved = achieved

    def GetStatus(self):
        return self.secc_param.secc_status3.seccStatus

    def GetCpVoltage(self):
        return self.secc_param.secc_status2.f_cpVoltage

    def GetCpOscillator(self):
        return self.secc_param.secc_status2.cpOscillator

    def GetHpGpLinkStatus(self):
        return self.secc_param.secc_status2.hpgpLinkStatus

    def GetTargetVoltage(self):
        return self.secc_param.secc_tg.f_targetVoltage

    def GetTargetCurrent(self):
        return self.secc_param.secc_tg.f_targetCurrent

    def GetPresentEVSOC(self):
        return self.secc_param.secc_soc.evSOC

    def GetEVErrorCode(self):
        return self.secc_param.secc_status1.evErrorCode

    def GetSECCErrorCode(self):
        return self.secc_param.secc_status1.seccErrorCode

    def GetChargingCompleted(self):
        res = False
        if self.secc_param.secc_soc.chargingComplete == SECC_SOC_CHG_COMPLETE:
            res = True
        return res
