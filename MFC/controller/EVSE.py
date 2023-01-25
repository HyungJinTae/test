# EVSE controller
# written based on EVSE C Code

from common.App_Header import *
from interface.CEG_Header import *
from controller.EVSE_Header import *
from controller.SYS_Singleton import TheSys


EVSE_AUTH_EIM_ONGOING = SECC_ONGOING
EVSE_AUTH_EIM_FINISHED = SECC_FINISHED
EVSE_CPD_ONGOING = SECC_ONGOING
EVSE_CPD_FINISHED = SECC_FINISHED


class EVSE:
    def __init__(self):
        self.ceg = TheSys.ceg
        self.secc = TheSys.secc
        self.sbms = TheSys.sbms
        self.dev = TheSys.dev
        self.evse_param = EVSE_Param()
        self.debug_probe = [0] * 8

    def GetModuleID(self, moduleID):
        return self.ceg.dict_param[moduleID].module_ID

    #######################
    # porting c code functions
    #######################
    def Init(self):
        self.ceg.Init(APP_CEG_GROUP_NO, APP_CEG_MODULE_COUNT)
        self.secc.Init()
        self.evse_param.evse_state = SECC_ST_IDLE

    def RecvDataProcess(self):
        frame = self.secc.can_obj.read()
        if not (frame is None):
            data_array = self.secc.can_obj.data_list(frame)
            self.secc.RecvSeccProcess(frame.id, data_array=data_array, byte_array=frame.data)

    def check_secc_cp_init(self):
        """ OFF, 12±1V.f, 9±1V.f """
        res = SECC_FALSE
        if (self.secc.GetCpOscillator() == SECC_OFF) and (8.0 < self.secc.GetCpVoltage() < 13.0):
            res = SECC_TRUE
        return res

    def check_secc_cp_wait_plug_in(self):
        """ ON,  9±1V.f """
        res = SECC_FALSE
        if (self.secc.GetCpOscillator() == SECC_ON) and (8.0 < self.secc.GetCpVoltage() < 10.0):
            res = SECC_TRUE
        return res

    def check_secc_cp_waiting_slac(self):
        """ OFF, 0±1V.f -> OFF, 9±1V.f -> ON, 9±1V.f """
        res = SECC_FALSE
        return res

    def check_secc_cp_cable_check(self):
        """ ON, 6±1V.f """
        res = SECC_FALSE
        if (self.secc.GetCpOscillator() == SECC_ON) and (5.0 < self.secc.GetCpVoltage() < 7.0):
            res = SECC_TRUE
        return res

    def check_secc_hpgp_linkdown(self):
        res = SECC_FALSE
        if self.secc.GetHpGpLinkStatus() == SECC_LINK_DOWN:
            res = SECC_TRUE
        return res

    def check_secc_hpgp_linkup(self):
        res = SECC_FALSE
        if self.secc.GetHpGpLinkStatus() == SECC_LINK_UP:
            res = SECC_TRUE
        return res

    def check_hv_relay_closed(self):
        res = SECC_FALSE
        if self.evse_param.hv_relay_state == EVSE_HV_CLOSE_FINISHED:
            res = SECC_TRUE
        return res

    def are_ev_bat_relays_opened(self):
        res = SECC_FALSE
        if self.sbms.SBMS_GetHVRelayOpened() or self.dev.BCU_GetEVHVRelayOpened():
            res = SECC_TRUE
        return res

    def evse_control_parameter_reset(self):
        self.secc.SetProcessingCPD(SECC_ONGOING)
        self.secc.SetCableCheckParam_Ongoing()
        self.secc.SetTriggerReNegotiation(SECC_DEFAULT)
        self.secc.SetVoltageLimitAchieved(SECC_FALSE)
        self.secc.SetCurrentLimitAchieved(SECC_FALSE)
        self.secc.SetPowerLimitAchieved(SECC_FALSE)

        self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)
        self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)   # just in case

    def hv_relay_close_process(self):
        state = self.evse_param.hv_relay_state
        if state == EVSE_HV_NONE:
            state = EVSE_HV_BATTERY_RELAY_CLOSE
        elif state == EVSE_HV_BATTERY_RELAY_CLOSE:
            state = EVSE_HV_BATTERY_RELAY_CLOSE_FB
        elif state == EVSE_HV_BATTERY_RELAY_CLOSE_FB:
            if self.sbms.SBMS_GetHVRelayClosed():
                state = EVSE_HV_OUT_RELAY_CLOSE
            else:
                state = EVSE_HV_BATTERY_RELAY_CLOSE
        elif state == EVSE_HV_OUT_RELAY_CLOSE:
            self.dev.BCU_SetEVHVRelayClose()
            state = EVSE_HV_OUT_RELAY_CLOSE_FB
        elif state == EVSE_HV_OUT_RELAY_CLOSE_FB:
            if self.dev.BCU_GetEVHVRelayClosed():
                state = EVSE_HV_CLOSE_FINISHED
            else:
                state = EVSE_HV_OUT_RELAY_CLOSE
        elif state == EVSE_HV_CLOSE_FINISHED:
            pass

        self.evse_param.hv_relay_state = state

    def update_evse_present_voltage(self):
        self.evse_param.f_present_voltage = self.ceg.GetGroupDCOutVoltage()
        self.evse_param.f_present_current = self.ceg.GetGroupDCOutTotalCurrent()
        self.evse_param.f_present_kw = (self.evse_param.f_present_voltage * self.evse_param.f_present_current) * EVSE_MULT_W_TO_KW
        self.secc.SetPresentVoltage(self.evse_param.f_present_voltage)
        self.secc.SetPresentCurrent(self.evse_param.f_present_current)

    def update_evse_limit_achieved(self):
        target_watt = self.evse_param.f_target_voltage * self.evse_param.f_target_current
        if self.evse_param.f_present_voltage >= EVSE_DC_OUTPUT_V_MAX:
            self.secc.SetVoltageLimitAchieved(SECC_TRUE)
        if self.evse_param.f_present_current >= EVSE_TOTAL_CURRENT_A_MAX:
            self.secc.SetCurrentLimitAchieved(SECC_TRUE)
        if target_watt >= EVSE_TOTAL_POWER_W_MAX:
            self.secc.SetPowerLimitAchieved(SECC_TRUE)

    def current_demand_running(self):
        self.evse_param.f_target_voltage = self.secc.GetTargetVoltage()
        self.evse_param.f_target_current = self.secc.GetTargetCurrent()

        # check max voltage/ current / power
        self.evse_param.f_target_voltage = min(self.evse_param.f_target_current, EVSE_DC_OUTPUT_V_MAX)
        self.evse_param.f_target_current = min(self.evse_param.f_target_current, EVSE_TOTAL_CURRENT_A_MAX)
        # for test
        if APP_DC_INPUT_SRC == APP_DC_INPUT_FZ10:
            self.evse_param.f_target_current = min(self.evse_param.f_target_current, self.evse_param.f_target_current_max)
        target_watt = self.evse_param.f_target_voltage * self.evse_param.f_target_current
        if target_watt >= EVSE_TOTAL_POWER_W_MAX:
            self.evse_param.f_target_current = EVSE_TOTAL_POWER_W_MAX / self.evse_param.f_target_voltage
        self.ceg.WriteGroupDCOutput(self.evse_param.f_target_voltage, self.evse_param.f_target_current)

    def write_precharge_default(self):
        self.evse_param.f_target_voltage = self.secc.GetTargetVoltage()
        self.evse_param.f_target_current = EVSE_PRE_CHARGE_CURRENT
        self.evse_param.f_target_voltage = min(self.evse_param.f_target_voltage, EVSE_DC_OUTPUT_V_MAX)
        self.ceg.WriteGroupDCOutput(self.evse_param.f_target_voltage, self.evse_param.f_target_current)
        self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_ON)

    def transition(self, evse_state):
        if evse_state == SECC_ST_IDLE:
            self.dev.BCU_SetEVHVRelayOpen()
            if self.evse_param.timestamp > 0:
                self.secc.SetTimeStamp(self.evse_param.timestamp)
            self.secc.SetIdleParam()
            self.secc.SetTriggerStateE(SECC_DISABLE)
        elif evse_state == SECC_ST_INITIALIZED:
            self.secc.SetInitializedParam()
            self.secc.SetTriggerStateE(SECC_DISABLE)
            self.dev.BCU_ResetTimeout_EVSE()
        elif evse_state == SECC_ST_WAITING_PLUG_IN:
            pass
        elif evse_state == SECC_ST_WAITING_SLAC:
            self.dev.BCU_ResetTimeout_EVSE()
        elif evse_state == SECC_ST_AUTHORIZATION_EIM:
            self.dev.BCU_ResetTimeout_EVSE()
            self.secc.SetProcessingAuthEIM(SECC_ONGOING)
        elif evse_state == SECC_ST_AUTHORIZATION_PNC:
            pass
        elif evse_state == SECC_ST_CHARGE_PARAMETER_DISCOVERY:
            self.secc.SetProcessingCPD(SECC_ONGOING)
        elif evse_state == SECC_ST_CABLE_CHECK:
            self.dev.BCU_ResetTimeout_EVSE()
            self.secc.SetCableCheckParam_Ongoing()
            self.evse_param.hv_relay_state = EVSE_HV_NONE
        elif evse_state == SECC_ST_PRE_CHARGE:
            self.dev.BCU_ResetTimeout_EVSE()
            self.secc.SetProcessingCPD(SECC_ONGOING)
            self.secc.SetCableCheckParam_Ongoing()
            self.write_precharge_default()
            self.evse_param.dcdc_state = EVSE_DCDC_NONE
        elif evse_state == SECC_ST_WELDING_DETECTION:
            pass
        elif evse_state == SECC_ST_POWER_DELIVERY_START:
            self.dev.BCU_ResetTimeout_EVSE()
        elif evse_state == SECC_ST_POWER_DELIVERY_EV_INIT_STOP:
            pass
        elif evse_state == SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP:
            pass
        elif evse_state == SECC_ST_POWER_DELIVERY_RENOGOTIATE:
            self.secc.SetTriggerReNegotiation(SECC_DEFAULT)
        elif evse_state == SECC_ST_CURRENT_DEMAND:
            self.evse_param.f_present_kw = float(0)
            self.evse_param.f_present_kwh = float(0)
        elif evse_state == SECC_ST_METERING_RECEIPT:
            pass
        elif evse_state == SECC_ST_TERMINATE:
            self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)
            self.evse_control_parameter_reset()
            self.dev.BCU_SetEVHVRelayOpen()
            self.dev.BCU_SetEVHVRelayOpen()   # just in case
        elif evse_state == SECC_ST_PAUSE:
            pass
        elif evse_state == SECC_ST_ERROR:
            self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)
            self.evse_control_parameter_reset()
            self.dev.BCU_SetEVHVRelayOpen()
            self.dev.BCU_SetEVHVRelayOpen()   # just in case

        self.evse_param.evse_state = evse_state

    def StateMachine(self):
        """ 50 msec period """
        if self.evse_param.is_activated == EVSE_DEACTIVATED: return

        state = self.evse_param.evse_state
        secc_status = self.secc.GetStatus()

        if state == SECC_ST_IDLE:
            if secc_status == SECC_ST_IDLE:
                self.transition(SECC_ST_IDLE)
                if self.evse_param.charging_control == EVSE_START:
                    self.secc.SetInitializePPMT()
            elif secc_status == SECC_ST_INITIALIZED:
                self.transition(SECC_ST_INITIALIZED)
            elif self.GetSeccReboot():
                self.secc.SetReboot()
                self.transition(SECC_ST_IDLE)
        elif state == SECC_ST_INITIALIZED:
            if secc_status == SECC_ST_IDLE:
                self.transition(SECC_ST_IDLE)
            elif secc_status == SECC_ST_INITIALIZED:
                if self.GetSeccReboot():
                    self.secc.SetReboot()
                    self.transition(SECC_ST_IDLE)
                elif self.GetNormalStop():
                    self.secc.SetNormalStop()
                elif self.GetEmergencyStop():
                    self.secc.SetEmergencyStop()
                else:
                    if self.dev.BCU_Timeout_EVSE(EVSE_WAIT_INITIALIZE_TIMEOUT_MS):
                        if self.check_secc_cp_init():
                            self.secc.SetStartCharging()
            elif secc_status == SECC_ST_WAITING_PLUG_IN:
                self.transition(SECC_ST_WAITING_PLUG_IN)
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_WAITING_PLUG_IN:
            if secc_status == SECC_ST_WAITING_PLUG_IN:
                if self.GetNormalStop():
                    self.secc.SetNormalStop()
                elif self.GetEmergencyStop():
                    self.secc.SetEmergencyStop()
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_WAITING_SLAC:
                if self.check_secc_cp_wait_plug_in():
                    self.transition(SECC_ST_WAITING_SLAC)
        elif state == SECC_ST_WAITING_SLAC:
            if secc_status == SECC_ST_WAITING_SLAC:
                if self.dev.BCU_Timeout_EVSE(EVSE_WAITING_SLAC_TIMEOUT_MS):
                    self.secc.SetNormalStop()
            elif secc_status == SECC_ST_PROCESSING_SLAC:
                self.transition(SECC_ST_PROCESSING_SLAC)
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
        elif state == SECC_ST_PROCESSING_SLAC:
            if secc_status == SECC_ST_PROCESSING_SLAC:
                if self.check_secc_hpgp_linkdown():
                    pass
            elif secc_status == SECC_ST_SDP:
                if self.check_secc_hpgp_linkup():
                    self.transition(SECC_ST_SDP)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_SDP:
            """SECC_ST_SDP 에서 SECC_ST_ESTABLISHING_TCP_TLS 를 1 cycle 만 받음. 
            SECC_ST_SAP 받는 부분은 매뉴얼에는 없지만 받을 수 있게 처리함."""
            if secc_status == SECC_ST_ESTABLISHING_TCP_TLS:
                self.transition(SECC_ST_ESTABLISHING_TCP_TLS)
            elif secc_status == SECC_ST_SAP:
                self.transition(SECC_ST_SAP)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_ESTABLISHING_TCP_TLS:
            if secc_status == SECC_ST_SAP:
                self.transition(SECC_ST_SAP)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_SAP:
            if secc_status == SECC_ST_SESSION_SETUP:
                self.transition(SECC_ST_SESSION_SETUP)
        elif state == SECC_ST_SESSION_SETUP:
            if secc_status == SECC_ST_SERVICE_DISCOVERY:
                self.transition(SECC_ST_SERVICE_DISCOVERY)
        elif state == SECC_ST_SERVICE_DISCOVERY:
            if secc_status == SECC_ST_SERVICE_DETIALS:
                self.transition(SECC_ST_SERVICE_DETIALS)
            elif secc_status == SECC_ST_PAYMENT_SERVICE_SELECTION:
                self.transition(SECC_ST_PAYMENT_SERVICE_SELECTION)
        elif state == SECC_ST_SERVICE_DETIALS:
            if secc_status == SECC_ST_PAYMENT_SERVICE_SELECTION:
                self.transition(SECC_ST_PAYMENT_SERVICE_SELECTION)
        elif state == SECC_ST_SESSION_STOP_TERMINATE:
            if secc_status == SECC_ST_SESSION_STOP_TERMINATE:
                pass
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
        elif state == SECC_ST_SESSION_STOP_PAUSE:
            pass
        elif state == SECC_ST_PAYMENT_SERVICE_SELECTION:
            if secc_status == SECC_ST_PAYMENT_SERVICE_SELECTION:
                """
                to do something
                - if selectedPaymentOption:
                -   ..
                - if selectedService_*:
                -   ..
                """
                pass
            elif secc_status == SECC_ST_CERTIFICATE_INSTALLATION:
                self.transition(SECC_ST_CERTIFICATE_INSTALLATION)
            elif secc_status == SECC_ST_CERTIFICATE_UPDATE:
                self.transition(SECC_ST_CERTIFICATE_UPDATE)
            elif secc_status == SECC_ST_PAYMENT_DETAILS:
                self.transition(SECC_ST_PAYMENT_DETAILS)
            elif secc_status == SECC_ST_AUTHORIZATION_EIM:
                self.transition(SECC_ST_AUTHORIZATION_EIM)
        elif state == SECC_ST_CERTIFICATE_INSTALLATION:
            if secc_status == SECC_ST_PAYMENT_DETAILS:
                self.transition(SECC_ST_PAYMENT_DETAILS)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_CERTIFICATE_UPDATE:
            if secc_status == SECC_ST_PAYMENT_DETAILS:
                self.transition(SECC_ST_PAYMENT_DETAILS)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_PAYMENT_DETAILS:
            if secc_status == SECC_ST_AUTHORIZATION_PNC:
                self.transition(SECC_ST_AUTHORIZATION_PNC)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
        elif state == SECC_ST_AUTHORIZATION_EIM:
            if secc_status == SECC_ST_AUTHORIZATION_EIM:
                if self.dev.BCU_Timeout_EVSE(EVSE_AUTHORIZATION_EIM_TIMEOUT_MS):
                    self.secc.SetNormalStop()
                else:
                    if self.GetProcessingAuthEIM() == EVSE_AUTH_EIM_FINISHED:
                        self.secc.SetProcessingAuthEIM(SECC_FINISHED)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_CHARGE_PARAMETER_DISCOVERY:
                self.transition(SECC_ST_CHARGE_PARAMETER_DISCOVERY)
        elif state == SECC_ST_AUTHORIZATION_PNC:
            if secc_status == SECC_ST_CHARGE_PARAMETER_DISCOVERY:
                self.transition(SECC_ST_CHARGE_PARAMETER_DISCOVERY)
        elif state == SECC_ST_CHARGE_PARAMETER_DISCOVERY:
            if secc_status == SECC_ST_CHARGE_PARAMETER_DISCOVERY:
                if self.GetProcessingCPD() == EVSE_CPD_FINISHED:
                    self.secc.SetProcessingCPD(SECC_FINISHED)
                else:   # if ongoing, set EVSE Maximum*Limit and Minimum*Limit
                    pass
            elif secc_status == SECC_ST_CABLE_CHECK:
                self.transition(SECC_ST_CABLE_CHECK)
        elif state == SECC_ST_CABLE_CHECK:
            if secc_status == SECC_ST_CABLE_CHECK:
                if self.check_secc_cp_cable_check():
                    if self.GetIMDValid():
                        if self.check_hv_relay_closed():
                            self.secc.SetCableCheckParam_Finished()
                        else:
                            self.hv_relay_close_process()
                            if self.dev.BCU_Timeout_EVSE(EVSE_CABLECHECK_TIMEOUT_MS):
                                self.secc.SetNormalStop()
                    else:
                        if self.dev.BCU_Timeout_EVSE(EVSE_CABLECHECK_TIMEOUT_MS):
                            self.secc.SetNormalStop()
            elif secc_status == SECC_ST_PRE_CHARGE:
                self.transition(SECC_ST_PRE_CHARGE)
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP:
                self.ceg.CEG_WriteGroupDCOutput(self.evse_param.f_target_voltage, EVSE_TOTAL_CURRENT_A_STOP)
                self.transition(SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP)
            else:
                if self.GetNormalStop():
                    self.secc.SetNormalStop()
        elif state == SECC_ST_PRE_CHARGE:
            if secc_status == SECC_ST_PRE_CHARGE:
                if self.GetIMDValid():
                    if self.ceg.GetGroupControlOn() == CEG_DEF_CONTROL_OFF:
                        self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_ON)
                    else:
                        # check tolerance between the targetVoltage and evsePresentVoltage in SECC
                        self.evse_param.f_target_voltage = self.secc.GetTargetVoltage()
                        self.evse_param.f_target_current = EVSE_PRE_CHARGE_CURRENT  # SECC_GetTargetCurrent();
                        self.evse_param.f_target_voltage = min(self.evse_param.f_target_voltage, EVSE_DC_OUTPUT_V_MAX)
                        self.ceg.CEG_WriteGroupDCOutput(self.evse_param.f_target_voltage, self.evse_param.f_target_current)
                        self.update_evse_present_voltage()

                        # for test
                        if APP_DC_INPUT_SRC == APP_DC_INPUT_FZ10:
                            self.evse_param.f_target_current_max = APP_MAX_CURRENT_LIMIT_FZ10

                    # check error
                    if self.are_ev_bat_relays_opened():
                        self.secc.SetNormalStop()
                else:
                    self.secc.SetEmergencyStop()

                if self.dev.BCU_Timeout_EVSE(EVSE_PRE_CHARGE_TIMEOUT_MS):
                    self.secc.SetNormalStop()
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_POWER_DELIVERY_START:
                if self.GetIMDValid():
                    if self.are_ev_bat_relays_opened():
                        self.secc.SetNormalStop()
                    else:
                        self.transition(SECC_ST_POWER_DELIVERY_START)
                else:
                    self.secc.SetEmergencyStop()
        elif state == SECC_ST_WELDING_DETECTION:
            if secc_status == SECC_ST_WELDING_DETECTION:
                self.update_evse_present_voltage()
                if self.ceg.GetGroupDCOutTotalCurrent() <= EVSE_TOTAL_CURRENT_A_IS_STOPPED:
                    self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)
            elif secc_status == SECC_ST_SESSION_STOP_TERMINATE:
                self.transition(SECC_ST_SESSION_STOP_TERMINATE)
            elif secc_status == SECC_ST_ERROR:
                self.transition(SECC_ST_ERROR)
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
        elif state == SECC_ST_POWER_DELIVERY_START:
            if secc_status == SECC_ST_POWER_DELIVERY_START:
                if self.GetIMDValid():
                    if self.are_ev_bat_relays_opened():
                        self.secc.SetNormalStop()
                else:
                    self.secc.SetEmergencyStop()
            elif secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_CURRENT_DEMAND:
                self.transition(SECC_ST_CURRENT_DEMAND)
        elif state == SECC_ST_POWER_DELIVERY_EV_INIT_STOP:
            if secc_status == SECC_ST_POWER_DELIVERY_EV_INIT_STOP:
                pass
            elif secc_status == SECC_ST_WELDING_DETECTION:
                self.transition(SECC_ST_WELDING_DETECTION)
            elif secc_status == SECC_ST_SESSION_STOP_TERMINATE:
                self.transition(SECC_ST_SESSION_STOP_TERMINATE)
        elif state == SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP:
            if secc_status == SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP:
                pass
            elif secc_status == SECC_ST_WELDING_DETECTION:
                self.transition(SECC_ST_WELDING_DETECTION)
            elif secc_status == SECC_ST_SESSION_STOP_TERMINATE:
                self.transition(SECC_ST_SESSION_STOP_TERMINATE)
        elif state == SECC_ST_POWER_DELIVERY_RENOGOTIATE:
            if secc_status == SECC_ST_CHARGE_PARAMETER_DISCOVERY:
                self.transition(SECC_ST_CHARGE_PARAMETER_DISCOVERY)
        elif state == SECC_ST_CURRENT_DEMAND:
            if secc_status == SECC_ST_CURRENT_DEMAND:
                if self.GetIMDValid():
                    if self.ceg.GetGroupControlOn() and (self.ceg.GEG_GetGroupAlarm() == CEG_FALSE):
                        self.current_demand_running()
                        self.update_evse_present_voltage()
                        self.update_evse_limit_achieved()
                        self.debug_probe[5] = 0

                    # check stop cases
                    if self.ceg.GetGroupAlarm():
                        self.secc.SetNormalStop()
                        self.debug_probe[5] = 1
                    elif self.are_ev_bat_relays_opened():
                        self.secc.SetNormalStop()
                        self.debug_probe[5] = 2
                    elif self.GetNormalStop():
                        self.secc.SetNormalStop()
                        self.debug_probe[5] = 3
                    elif self.GetEmergencyStop():
                        self.secc.SetEmergencyStop()
                        self.debug_probe[5] = 4
                    elif self.GetTriggerReNego():
                        self.secc.SetTriggerReNegotiation(SECC_REQ_RE_NEGO)
                        self.debug_probe[5] = 5
                    elif self.secc.GetPresentEVSOC() >= EVSE_SOC_MAX:
                        self.secc.SetNormalStop()
                        self.debug_probe[5] = 6
                    elif self.secc.GetChargingCompleted():
                        self.secc.SetNormalStop()
                        self.debug_probe[5] = 7
                else:
                    self.secc.SetEmergencyStop()
                    self.debug_probe[5] = 6
            elif secc_status == SECC_ST_POWER_DELIVERY_EV_INIT_STOP:
                self.ceg.GEG_WriteGroupDCOutput(self.evse_param.f_target_voltage, EVSE_TOTAL_CURRENT_A_STOP)
                self.transition(SECC_ST_POWER_DELIVERY_EV_INIT_STOP)
            elif secc_status == SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP:
                self.ceg.CEG_WriteGroupDCOutput(self.evse_param.f_target_voltage, EVSE_TOTAL_CURRENT_A_STOP)
                self.transition(SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP)
            elif secc_status == SECC_ST_ERROR:
                self.dev.BCU_SetEVHVRelayOpen()
                self.transition(SECC_ST_ERROR)
            elif secc_status == SECC_ST_TERMINATE:
                self.ceg.CEG_WriteGroupDCOutput(self.evse_param.f_target_voltage, EVSE_TOTAL_CURRENT_A_STOP)
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_POWER_DELIVERY_RENOGOTIATE:
                self.ceg.CEG_WriteGroupDCOutput(self.evse_param.f_target_voltage, EVSE_TOTAL_CURRENT_A_STOP)
                self.transition(SECC_ST_POWER_DELIVERY_RENOGOTIATE)
        elif state == SECC_ST_METERING_RECEIPT:
            pass
        elif state == SECC_ST_TERMINATE:
            if secc_status == SECC_ST_TERMINATE:
                pass
            elif secc_status == SECC_ST_IDLE:
                if self.secc.GetHpGpLinkStatus() == SECC_LINK_DOWN:
                    self.transition(SECC_ST_IDLE)
        elif state == SECC_ST_PAUSE:
            pass
        elif state == SECC_ST_ERROR:
            if secc_status == SECC_ST_TERMINATE:
                self.transition(SECC_ST_TERMINATE)
            elif secc_status == SECC_ST_IDLE:
                self.transition(SECC_ST_IDLE)

    #########################
    # Set Functions
    #########################

    def SetActivate_DCDCOnly(self):
        self.ceg.SetActivate()

    def SetActivate(self):
        self.ceg.SetActivate()
        self.evse_param.is_activated = EVSE_ACTIVATED

    def SetDeactivate(self):
        self.ceg.InitStatusParamAll()
        self.ceg.SetDeactivate()
        self.evse_param.is_activated = EVSE_DEACTIVATED

    def SetChargingControl(self, control):
        self.evse_param.charging_control = control

    def SetNormalStopUser(self, nstop):
        self.evse_param.normalstop_user = nstop

    def SetEmergencyStopUser(self, estop):
        self.evse_param.emergencystop_user = estop

    def SetTimestamp(self, timestamp):
        self.evse_param.timestamp = timestamp

    def SendTargetVoltageCurrent_Dir(self, f_voltage, f_current):
        self.ceg.WriteGroupDCOutput(f_voltage, f_current)

    def SendDCDCControlON_Dir(self, onoff):
        if onoff == APP_CEG_CONTROL_ON:
            self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_ON)
        else:
            self.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)

    def SendDCDCWalkInEnable_Dir(self, enable):
        if enable == APP_CEG_WALKIN_ENABLE:
            self.ceg.WriteGroupWalkIn(CEG_DEF_WALK_IN_ENABLE)
        else:
            self.ceg.WriteGroupWalkIn(CEG_DEF_WALK_IN_DISABLE)

    def SendDCDCLedBlink_Dir(self, blink):
        if blink == APP_CEG_MODULE_ID_1_BLINK:
            self.ceg.WriteModuleLedBlink(APP_CEG_MODULE0_ID, CEG_DEF_GREEN_LED_BLINK)
        elif blink == APP_CEG_MODULE_ID_1_NORMAL:
            self.ceg.WriteModuleLedBlink(APP_CEG_MODULE0_ID, CEG_DEF_GREEN_LED_NORMAL)
        elif blink == APP_CEG_MODULE_ID_2_BLINK:
            self.ceg.WriteModuleLedBlink(APP_CEG_MODULE1_ID, CEG_DEF_GREEN_LED_BLINK)
        elif blink == APP_CEG_MODULE_ID_2_NORMAL:
            self.ceg.WriteModuleLedBlink(APP_CEG_MODULE1_ID, CEG_DEF_GREEN_LED_NORMAL)

    #########################
    # Get Functions
    #########################
    def GetProcessingAuthEIM(self):
        # for Hi-Charger, right way set signal finished
        return EVSE_AUTH_EIM_FINISHED

    def GetProcessingCPD(self):
        # for Hi-Charger, right way set signal finished
        return EVSE_CPD_FINISHED

    def GetIMDValid(self):
        res = EVSE_IMD_NOK
        if self.sbms.SBMS_GetIMDstatusOK() == APP_TRUE:
            res = EVSE_IMD_OK
        return res

    def GetEmergencyStop(self):
        res = EVSE_FALSE
        if self.evse_param.emergencystop_user == EVSE_NSTOP_ON:
            res = EVSE_TRUE
        return res

    def GetTriggerReNego(self):
        res = 0
        return res

    def GetNormalStop(self):
        res = EVSE_FALSE
        if self.evse_param.normalstop_user == EVSE_NSTOP_ON:
            res = EVSE_TRUE
        return res

    def GetSeccReboot(self):
        res = 0
        return res

    def GetState(self):
        return self.evse_param.evse_state

    def GetDCControlON(self):
        return self.ceg.GetGroupControlOn()

    def GetDCDCAlarm(self):
        return self.ceg.GetGroupAlarm()

    def GetEVPresentSOC_100mP(self):
        return self.secc.GetPresentEVSOC() * EVSE_MULT_UINT8_TO_UINT16

    def GetEVPresentVoltage_100mV(self):
        return self.ceg.GetGroupDCOutVoltage() * EVSE_MULT_UINT8_TO_UINT16

    def GetEVPresentCurrent_100mA(self):
        return self.ceg.GetGroupDCOutTotalCurrent() * EVSE_MULT_UINT8_TO_UINT16

    def GetBATPresentSOC_100mP(self):
        return 0

    def GetDCPresentVoltage_mV(self):
        return self.ceg.GetGroupDCOutVoltage() * EVSE_MULT_FLOAT_TO_UINT32

    def GetDCPresentCurrent_mA(self):
        return self.ceg.GetGroupDCOutTotalCurrent() * EVSE_MULT_FLOAT_TO_UINT32

    def GetDCPresentKWH(self):
        return self.evse_param.f_present_kwh

    def GetEVErrorCode(self):
        return self.secc.GetEVErrorCode()

    def GetSECCErrorCode(self):
        return self.secc.GetSECCErrorCode()

    def GetDCDCErrorCode(self):
        res = 0
        reg1 = TheSys.ceg.GetParam(APP_CEG_MODULE0_ID)
        reg2 = TheSys.ceg.GetParam(APP_CEG_MODULE1_ID)

        if reg1.alarm_state.output_short: res = EVSE_ERR_DCDC1_OUTPUT_SHORT
        elif reg1.alarm_state.inner_comm_interrupt: res = EVSE_ERR_DCDC1_INNER_COMM_INTR
        elif reg1.alarm_state.pfc_side_abnormal: res = EVSE_ERR_DCDC1_PFC_SIDE_ABNORMAL
        elif reg1.alarm_state.discharge_abnormal: res = EVSE_ERR_DCDC1_DCHG_ABNORMAL
        elif reg1.alarm_state.mdl_fault: res = EVSE_ERR_DCDC1_MDL_FAULT
        elif reg1.alarm_state.mdl_protect: res = EVSE_ERR_DCDC1_MDL_PROTECT
        elif reg1.alarm_state.fan_fault: res = EVSE_ERR_DCDC1_FAN_FAULT
        elif reg1.alarm_state.over_temperature: res = EVSE_ERR_DCDC1_OT
        elif reg1.alarm_state.output_over_voltage: res = EVSE_ERR_DCDC1_OUTPUT_OV
        elif reg1.alarm_state.can_comm_interrupt: res = EVSE_ERR_DCDC1_CAN_COMM_INTR
        elif reg1.alarm_state.power_limit: res = EVSE_ERR_DCDC1_POWER_LIMIT
        elif reg1.alarm_state.mdl_ID_repetition: res = EVSE_ERR_DCDC1_MDL_REPETITION
        elif reg1.alarm_state.load_unsharing: res = EVSE_ERR_DCDC1_LOAD_SHARING
        elif reg1.alarm_state.input_phase_lost: res = EVSE_ERR_DCDC1_INPUT_PHASE_LOST
        elif reg1.alarm_state.input_under_voltage: res = EVSE_ERR_DCDC1_INPUT_UV
        elif reg1.alarm_state.input_over_voltage: res = EVSE_ERR_DCDC1_INPUT_OV

        if reg2.alarm_state.output_short: res = EVSE_ERR_DCDC2_OUTPUT_SHORT
        elif reg2.alarm_state.inner_comm_interrupt: res = EVSE_ERR_DCDC2_INNER_COMM_INTR
        elif reg2.alarm_state.pfc_side_abnormal: res = EVSE_ERR_DCDC2_PFC_SIDE_ABNORMAL
        elif reg2.alarm_state.discharge_abnormal: res = EVSE_ERR_DCDC2_DCHG_ABNORMAL
        elif reg2.alarm_state.mdl_fault: res = EVSE_ERR_DCDC2_MDL_FAULT
        elif reg2.alarm_state.mdl_protect: res = EVSE_ERR_DCDC2_MDL_PROTECT
        elif reg2.alarm_state.fan_fault: res = EVSE_ERR_DCDC2_FAN_FAULT
        elif reg2.alarm_state.over_temperature: res = EVSE_ERR_DCDC2_OT
        elif reg2.alarm_state.output_over_voltage: res = EVSE_ERR_DCDC2_OUTPUT_OV
        elif reg2.alarm_state.can_comm_interrupt: res = EVSE_ERR_DCDC2_CAN_COMM_INTR
        elif reg2.alarm_state.power_limit: res = EVSE_ERR_DCDC2_POWER_LIMIT
        elif reg2.alarm_state.mdl_ID_repetition: res = EVSE_ERR_DCDC2_MDL_REPETITION
        elif reg2.alarm_state.load_unsharing: res = EVSE_ERR_DCDC2_LOAD_SHARING
        elif reg2.alarm_state.input_phase_lost: res = EVSE_ERR_DCDC2_INPUT_PHASE_LOST
        elif reg2.alarm_state.input_under_voltage: res = EVSE_ERR_DCDC2_INPUT_UV
        elif reg2.alarm_state.input_over_voltage: res = EVSE_ERR_DCDC2_INPUT_OV

        return res

    def GetDCGroupNo(self):
        return self.ceg.GetGroupNo()

    def GetDCModuleCount_InGroup(self):
        return self.ceg.GetModuleCountInGroup()

    def GetDCGroupAlarm(self):
        return self.ceg.REG_GetGroupAlarm()

    def GetDCPresentTemperature_mT(self, module_no):
        return self.ceg.GetModuleTemperature(module_no) * EVSE_MULT_FLOAT_TO_UINT32

    def GetDCPresentTemperature(self, module_no):
        return self.ceg.GetModuleTemperature(module_no)

    def GetDCAlarm(self, module_no):
        return self.ceg.GetAlarm(module_no)

    def GetDCAlarmCode(self, module_no):
        return self.ceg.CEG_GetAlramCode(module_no)

    def GetDCSideOFF(self, module_no):
        return self.ceg.GetModuleDCSideOFF(module_no)

    def GetDCWalkInEnable(self, module_no):
        return self.ceg.GetModuleWalkInEnable(module_no)

    def GetDCOutputVoltage_mV(self, module_no):
        return self.ceg.GetModuleDCOutputVoltage(module_no) * EVSE_MULT_FLOAT_TO_UINT32

    def GetDCOutputCurrent_mA(self, module_no):
        return self.ceg.GetModuleDCOutputCurrent(module_no) * EVSE_MULT_FLOAT_TO_UINT32

    def GetDCInputVoltage_mV(self, module_no):
        return self.ceg.GetModuleDCInputVoltage(module_no) * EVSE_MULT_FLOAT_TO_UINT32

    #########################
    # EVSE Send Process
    #########################
    def ProcessUnconditional(self):
        # 50 ms
        self.secc.SendEvseStatus()

    def Process50ms(self):
        if self.evse_param.is_activated == EVSE_DEACTIVATED: return
        self.secc.SendEvsePresVoltCurr()

    def Process200ms(self):
        if self.evse_param.is_activated == EVSE_DEACTIVATED: return
        self.secc.SendEvseConfigurations()
        self.secc.SendEvseChgParam1()
        self.secc.SendEvseChgParam2()

    def Process1000ms(self):
        if self.evse_param.is_activated == EVSE_DEACTIVATED: return
        self.evse_param.f_present_kwh += (self.evse_param.f_present_kw * EVSE_MULT_KW_TO_KWH)

    def SendDebugMessage1(self):
        id_ = APP_CAN_ID_DEBUG_EVSE
        inV = self.ceg.GetModuleDCInputVoltage(APP_CEG_MODULE1_ID)

        self.debug_probe[0] = self.evse_param.is_activated
        self.debug_probe[1] = self.evse_param.hv_relay_state
        self.debug_probe[2] = self.dev.BCU_GetEVHVRelayClosed()
        self.debug_probe[3] = (inV >> 8) & 0xFF
        self.debug_probe[4] = (inV & 0xFF)

        TheSys.dbg_can.write_wait(id_, bytearray(self.debug_probe))
