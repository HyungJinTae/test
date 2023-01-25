import sys
from common.App_Header import *
from common.QtWidgets_Functions import *
from interface.DEV_Header import *
from interface.SECC_Header import *
from interface.HMI_Header import *
from controller.EVSE_Header import *
from controller.SCU_Header import *
from controller.EVSE import EVSE
from controller.SYS_Singleton import TheSys
from controller.HMI_Singleton import TheHmi

import random # TEST_Code

class SCU:
    def __init__(self):
        self.evse = EVSE()
        self.sbms = TheSys.sbms
        self.scu_param = SCU_Param()

    #######################
    # porting c code functions
    #######################
    def Init(self):
        self.evse.Init()
        self.scu_param = SCU_Param()
        self.scu_param.state = SCU_ST_BOOT

    def Task50ms(self):
        self.StateMachine()
        self.UpdateSCUStatus()

        self.evse.StateMachine()
        self.sbms.SBMS_StateMachine()
        self.evse.ProcessUnconditional()
        self.evse.Process50ms()
        # EVSE_RequestDCDCInfo50ms
        TheSys.DemandTask50ms_CEG()
        TheSys.DemandTask50ms_BEG()

    def Task200ms(self):
        self.evse.Process200ms()
        self.TEST_Code_DEMO_Monitoring()  # TEST_Code

    def Task1000ms(self):
        TheSys.secc.Process1000ms()
        TheSys.DemandTask1000ms_CEG()
        self.evse.Process1000ms()

        self.CalcEvBatParameters()
        self.UpdateLedStatus()

    def TEST_Code_DEMO_Monitoring(self):  # TEST_Code
        if TheHmi.GetParam().hmi_status.hmiChargingControl is HMI_CHG_CTRL_START_CHG:
            self.TEST_Code_update_Tab1()
        elif TheHmi.GetParam().hmi_status.hmiChargingControl is HMI_CHG_CTRL_STOP_CHG:
            self.TEST_Code_init_Tab1()
        self.TEST_Code_update_Tab2()


    def TEST_Code_update_Tab1(self):  # TEST_Code
        TheHmi.GetParam().ev_status.evSOC = random.uniform(50, 55)
        TheHmi.GetParam().ev_status.evPresentVoltage = random.uniform(500, 501)
        TheHmi.GetParam().ev_status.evPresentCurrent = random.uniform(100, 101)

        TheHmi.GetParam().bat_status.batSOC = random.uniform(20, 25)
        TheHmi.GetParam().bat_status.batPresentVoltage = random.uniform(300, 301)
        TheHmi.GetParam().bat_status.batPresentCurrent = random.uniform(10, 11)
        self.update_HMIerrorcode_parameter(0, 1, 1, 1)

    def TEST_Code_update_Tab2(self):  # TEST_Code
        TheSys.beg.dict_param[0].ac_a_phase_voltage = 221
        TheSys.beg.dict_param[0].ac_b_phase_voltage = 222
        TheSys.beg.dict_param[0].ac_c_phase_voltage = 219
        TheSys.beg.dict_param[0].ac_a_phase_current = 10
        TheSys.beg.dict_param[0].ac_b_phase_current = 20
        TheSys.beg.dict_param[0].ac_c_phase_current = 30

        TheHmi.GetParam().aircooler_status.AcPresentTempIn = 12.5
        TheHmi.GetParam().aircooler_status.AcPresentTempOut = 7.6
        TheHmi.GetParam().aircooler_status.AcPresentHumidity = 35
        TheHmi.GetParam().aircooler_status.AcError = 100

    def TEST_Code_init_Tab1(self):  # TEST_Code
        TheHmi.GetParam().ev_status.evSOC = 0
        TheHmi.GetParam().ev_status.evPresentVoltage = 0
        TheHmi.GetParam().ev_status.evPresentCurrent = 0

        TheHmi.GetParam().bat_status.batSOC = 0
        TheHmi.GetParam().bat_status.batPresentVoltage = 0
        TheHmi.GetParam().bat_status.batPresentCurrent = 0
        self.reset_HMIerrorstatus()

    def UpdateLedStatus(self):
        TheSys.dev.BCU_SetRunModeLED(self.scu_param.ev_led_status)
        TheSys.dev.BCU_SetRunModeLED(self.scu_param.bat_led_status)
        TheSys.dev.BCU_SetRunModeLED(self.scu_param.stop_led_status)
        TheSys.dev.BCU_SetRunModeLED(self.scu_param.drive_led_status)

    def update_led_status(self, status):
        if status == DO_LED_DRIVE_ON or status == DO_LED_DRIVE_OFF or status == DO_LED_DRIVE_BLINK:
            self.scu_param.drive_led_status = status
        elif status == DO_LED_EV_CHG_ON or status == DO_LED_EV_CHG_OFF or status == DO_LED_EV_CHG_BLINK:
            self.scu_param.ev_led_status = status
        elif status == DO_LED_BAT_CHG_ON or status == DO_LED_BAT_CHG_OFF or status == DO_LED_BAT_CHG_BLINK:
            self.scu_param.bat_led_status = status
        elif status == DO_LED_OP_STOP_ON or status == DO_LED_OP_STOP_OFF or status == DO_LED_OP_STOP_BLINK:
            self.scu_param.stop_led_status = status

    def update_ev_parameters(self):
        present_voltage = TheSys.ceg.GetGroupDCOutVoltage()
        present_current = TheSys.ceg.GetGroupDCOutTotalCurrent()
        present_power = present_voltage * present_current
        present_wh = present_power * SCU_MULT_POWER_WATT_TO_WATT_HOUR
        target_chg_time_sec = self.scu_param.ev_chg_time_sec
        target_chg_amount_wh = self.scu_param.ev_chg_amount_wh

        self.scu_param.charging_amount_wh += present_wh

        if self.scu_param.ev_chg_mode == SCU_CHG_MODE_TIME:
            TheHmi.GetParam().chg_param1.evChargingAmount = self.scu_param.charging_amount_wh
            TheHmi.GetParam().chg_param1.evElapsedTime = TheSys.dev.BCU_PresentTime_EVCHG()
            TheHmi.GetParam().chg_param1.evRemainingTime = target_chg_time_sec - TheSys.dev.BCU_PresentTime_EVCHG()
        elif self.scu_param.ev_chg_mode == SCU_CHG_MODE_AMOUNT:
            # power = c x v
            # ws = power * second
            # wh = ws / 3600 = power * second / 3600
            # => second = wh * 3600 / power
            remained_wh = target_chg_amount_wh - self.scu_param.charging_amount_wh
            remaining_time = (remained_wh * 3600) / present_power
            TheHmi.GetParam().chg_param1.evChargingAmount = self.scu_param.charging_amount_wh
            TheHmi.GetParam().chg_param1.evElapsedTime = TheSys.dev.BCU_PresentTime_EVCHG()
            TheHmi.GetParam().chg_param1.evRemainingTime = remaining_time

    def update_bat_parameters(self):
        pass

    def reset_ev_bat_parameters(self):
        self.scu_param.charging_amount_wh = float(0)
        TheHmi.GetParam().chg_param1.evChargingAmount = 0
        TheHmi.GetParam().chg_param1.evElapsedTime = 0
        TheHmi.GetParam().chg_param1.evRemainingTime = 0
        TheHmi.GetParam().chg_param1.batChargingAmount = 0
        TheHmi.GetParam().chg_param2.batElapsedTime = 0
        TheHmi.GetParam().chg_param2.batRemainingTime = 0

    def CalcEvBatParameters(self):
        if (self.scu_param.state == SCU_ST_EV_CHG_RUNNING) and (self.scu_param.sub_state == SCU_SUB_ST_EV_RUN):
            self.update_ev_parameters()
        elif (self.scu_param.state == SCU_ST_BAT_CHG_RUNNING) and (self.scu_param.sub_state == SCU_SUB_ST_BAT_RUN):
            self.update_bat_parameters()

    def UpdateSECCStatus(self):
        if TheSys.secc.IsActivated():
            TheHmi.GetParam().scu_status.scuSECCactivated = APP_TRUE
        else:
            TheHmi.GetParam().scu_status.scuSECCactivated = APP_FALSE

    def UpdateSCUStatus(self):
        evse_state = self.evse.GetState()
        run_mode = TheHmi.GetParam().hmi_conf.hmiRunMode

        if run_mode == APP_RUN_MODE_EV_CHARGING or run_mode == APP_RUN_MODE_IDLE:
            if evse_state == SECC_ST_IDLE:
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_IDLE
            elif (evse_state >= SECC_ST_INITIALIZED) and (evse_state < SECC_ST_CABLE_CHECK):
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_INITIALIZE
            elif (evse_state == SECC_ST_CABLE_CHECK) or (evse_state == SECC_ST_PRE_CHARGE):
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_CABLE_CHECK
            elif (evse_state == SECC_ST_POWER_DELIVERY_START) or (evse_state == SECC_ST_CURRENT_DEMAND):
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_CHARGING
            elif((evse_state == SECC_ST_POWER_DELIVERY_EV_INIT_STOP)
                 or (evse_state == SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP)
                 or (evse_state == SECC_ST_POWER_DELIVERY_RENOGOTIATE)
                 or (evse_state == SECC_ST_WELDING_DETECTION)):
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_CHARGE_STOPPING
            elif evse_state == SECC_ST_ERROR:
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_CHARGE_ERROR
            elif (evse_state == SECC_ST_TERMINATE) or (evse_state == SECC_ST_SESSION_STOP_TERMINATE):
                TheHmi.GetParam().scu_status.scuStatus = SCU_STS_EV_CHARGER_CHARGE_TERMINATE

    def EVChargingRunning(self):
        sub_state = self.scu_param.sub_state
        ev_chg_amount_kwh = self.scu_param.ev_chg_amount_wh * 0.001
        ev_chg_time_msec = self.scu_param.ev_chg_time_sec * 1000
        if sub_state == SCU_SUB_ST_EV_IDLE:
            sub_state = SCU_SUB_ST_EV_START
        elif sub_state == SCU_SUB_ST_EV_START:
            # update default parameter
            if self.scu_param.ev_chg_time_sec == 0:
                self.scu_param.ev_chg_time_sec = SCU_DEFAULT_EV_CHG_TIME_SEC
            if self.scu_param.ev_chg_amount_wh == 0:
                self.scu_param.ev_chg_amount_wh = SCU_DEFAULT_EV_CHG_AMOUNT_WH
            sub_state = SCU_SUB_ST_EV_RUN_WAIT
        elif sub_state == SCU_SUB_ST_EV_RUN_WAIT:
            # SECC start charging
            if self.evse.GetState() == SECC_ST_CURRENT_DEMAND:
                TheSys.dev.BCU_ResetTimeout_EVCHG()
                sub_state = SCU_SUB_ST_EV_RUN
        elif sub_state == SCU_SUB_ST_EV_RUN:
            if self.scu_param.ev_chg_mode == SCU_CHG_MODE_TIME:
                # timeout setting minutes
                if TheSys.dev.BCU_Timeout_EVCHG(ev_chg_time_msec): sub_state = SCU_SUB_ST_EV_STOP
            elif self.scu_param.ev_chg_mode == SCU_CHG_MODE_AMOUNT:
                # reached setting KWH
                if self.evse.GetDCpresentKWH() >= ev_chg_amount_kwh: sub_state = SCU_SUB_ST_EV_STOP
            # had wrong EV charging mode
            else:
                sub_state = SCU_SUB_ST_EV_STOP
        elif sub_state == SCU_SUB_ST_EV_STOP:
            pass
        self.scu_param.sub_state = sub_state

    def DCDCtestRunning(self):
        sub_state = self.scu_param.sub_state
        if sub_state == SCU_SUB_ST_TM_IDLE:
            sub_state = SCU_SUB_ST_TM_DIRECT
        elif sub_state == SCU_SUB_ST_TM_DIRECT:
            control = TheHmi.GetParam().hmi_dc_status.dcdcControlOn
            walkin = TheHmi.GetParam().hmi_dc_status.dcdcWalkInEnable
            blink = TheHmi.GetParam().hmi_dc_status.dcdcLedBlink
            f_voltage = TheHmi.GetParam().hmi_dc_tg.f_dcdcTargetVoltage
            f_current = TheHmi.GetParam().hmi_dc_tg.f_dcdcTargetCurrent
            self.evse.SendTargetVoltageCurrent_Dir(f_voltage, f_current)
            self.evse.SendDCDCcontrolON_Dir(control)
            self.evse.SendDCDCWalkinEnable_Dir(walkin)
            self.evse.SendDCDCLedBlink_Dir(blink)
        self.scu_param.sub_state = sub_state

    def AdminRunning(self):
        sub_state = self.scu_param.sub_state
        timestamp = 0
        if sub_state == SCU_SUB_ST_AM_IDLE:
            self.evse.SetActivate()
            timestamp = TheHmi.GetParam().hmi_timestamp.hmiTimestamp_EVSE
            if  timestamp > 0: sub_state = SCU_SUB_ST_AM_SET_TIMESTEMP
        elif sub_state == SCU_SUB_ST_AM_SET_TIMESTEMP:
            if TheSys.secc.IsActivated():
                self.evse.SetTimestamp(timestamp)
                TheHmi.GetParam().hmi_timestamp.hmiTimestamp_EVSE = 0
                sub_state = SCU_SUB_ST_AM_END
        elif sub_state == SCU_SUB_ST_AM_END:
            pass
        self.scu_param.sub_state = sub_state

    def BATChargingRunning(self):
        pass

    def is_idle_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_IDLE:
            res = APP_TRUE
        return res

    def is_ev_chg_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_EV_CHARGING:
            res = APP_TRUE
        return res

    def is_bat_chg_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_BATTERY_CHARGING:
            res = APP_TRUE
        return res

    def is_chg_stop_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_STOPPING:
            res = APP_TRUE
        return res

    def is_test_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_DCDC_TEST:
            res = APP_TRUE
        return res

    def is_drive_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_DRIVE:
            res = APP_TRUE
        return res

    def is_shutdown_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        hmi_activate = TheHmi.GetParam().is_activated
        if (selected == APP_RUN_MODE_IDLE) and (req_mode == APP_RUN_MODE_SHUTDOWN):
            res = APP_TRUE
        elif (selected == APP_RUN_MODE_EM_STOP) and (hmi_activate == HMI_DEACTIVATED):
            res = APP_TRUE
        return res

    def is_emergency_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        hmi_activate = TheHmi.GetParam().is_activated
        if (selected == APP_RUN_MODE_EM_STOP) and (hmi_activate == HMI_ACTIVATED):
            res = APP_TRUE
        return res

    def is_admin_mode_selected(self, selected, req_mode):
        res = APP_FALSE
        if req_mode == APP_RUN_MODE_ADMIN:
            res = APP_TRUE
        return res

    def is_chg_stop_requested(self, req_chg_ctrl):
        res = APP_FALSE
        if req_chg_ctrl == HMI_CHG_CTRL_STOP_CHG:
            res = APP_TRUE
        return res

    def is_chg_start_requested(self, req_chg_ctrl):
        res = APP_FALSE
        if req_chg_ctrl == HMI_CHG_CTRL_START_CHG:
            res = APP_TRUE
        return res

    def is_evse_terminated(self, evse_state):
        res = APP_FALSE
        if evse_state == SECC_ST_TERMINATE:
            res = APP_TRUE
        return res

    def had_evse_error(self, evse_state):
        res = APP_FALSE
        if evse_state == SECC_ST_ERROR:
            res = APP_TRUE
        return res

    def had_dcdc_error(self):
        res = APP_FALSE
        if TheSys.ceg.GetGroupAlarm():
            res = APP_TRUE
        return res

    def is_evse_state_idle(self, evse_state):
        res = APP_FALSE
        if evse_state == SECC_ST_IDLE:
            res = APP_TRUE
        return res

    def is_secc_status_idle(self, secc_state):
        res = APP_FALSE
        if secc_state == SECC_ST_IDLE:
            res = APP_TRUE
        return res

    def update_HMIerrorcode_parameter(self, ev_ecode, secc_ecode, dcdc_ecode, sbms_ecode):
        TheHmi.GetParam().scu_status.scuError = APP_TRUE
        TheHmi.GetParam().scu_ecode.scuECode_EV = ev_ecode
        TheHmi.GetParam().scu_ecode.scuECode_SECC = secc_ecode
        TheHmi.GetParam().scu_ecode.scuECode_DCDC = dcdc_ecode
        TheHmi.GetParam().scu_ecode.scuECode_SBMS = sbms_ecode

    def reset_HMIerrorstatus(self):
        TheHmi.GetParam().scu_status.scuError = APP_FALSE
        TheHmi.GetParam().scu_ecode.scuECode_EV = 0
        TheHmi.GetParam().scu_ecode.scuECode_SECC = 0
        TheHmi.GetParam().scu_ecode.scuECode_DCDC = 0
        TheHmi.GetParam().scu_ecode.scuECode_SBMS = 0

    def update_scu_status_direct(self, scu_status):
        TheHmi.GetParam().scu_status.scuStatus = scu_status

    def change_scu_run_mode(self, scu_run_mode):
        """
          APP_RUN_MODE_IDLE = 0,
          APP_RUN_MODE_DCDC_TEST,
          APP_RUN_MODE_ADMIN,
          APP_RUN_MODE_EV_CHARGING = 10,
          APP_RUN_MODE_BATTERY_CHARGING,
          APP_RUN_MODE_DRIVE = 20,
          APP_RUN_MODE_STOPPING = 30,
          APP_RUN_MODE_BOOT = 40,
          APP_RUN_MODE_EM_STOP,
          APP_RUN_MODE_SHUTDOWN = 99,
        """
        TheHmi.GetParam().scu_status.scuRunMode = scu_run_mode

    def scu_transition(self, req_state):
        if req_state == SCU_ST_IDLE:
            self.update_led_status(DO_LED_DRIVE_OFF)
            self.update_led_status(DO_LED_EV_CHG_OFF)
            self.update_led_status(DO_LED_BAT_CHG_OFF)
            self.update_led_status(DO_LED_OP_STOP_OFF)
            self.scu_param.sub_state = SCU_SUB_ST_EV_IDLE
            self.reset_HMIerrorstatus()
            self.reset_ev_bat_parameters()
            self.evse.SetDeactivate()
            self.evse.SetNormalStopUser(EVSE_NSTOP_OFF)
            self.evse.SetEmergencyStopUser(EVSE_ESTOP_OFF)
            self.evse.SetChargingControl(EVSE_STOP)
            self.change_scu_run_mode(APP_RUN_MODE_IDLE)
        elif req_state == SCU_ST_EV_CHG_WAIT:
            self.evse.SetActivate()
            self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
            self.update_led_status(DO_LED_EV_CHG_ON)
        elif req_state == SCU_ST_EV_CHG_SBMS_RELAY_CLOSE:
            self.evse.SetNormalStopUser(EVSE_NSTOP_OFF)
        elif req_state == SCU_ST_EV_CHG_RUNNING:
            self.evse.SendDCDCWalkInEnable_Dir(APP_CEG_WALKIN_ENABLE)
        elif req_state == SCU_ST_BAT_CHG_WAIT:
            self.evse.SetDeactivate()
            self.update_led_status(DO_LED_BAT_CHG_ON)
        elif req_state == SCU_ST_BAT_CHG_RUNNING:
            pass
        elif req_state == SCU_ST_STOPPING:
            self.evse.SetChargingControl(EVSE_STOP)
            self.change_scu_run_mode(APP_RUN_MODE_STOPPING)
            self.update_led_status(DO_LED_OP_STOP_BLINK)
        elif req_state == SCU_ST_STOPED:
            self.change_scu_run_mode(APP_RUN_MODE_STOPPING)
            self.update_led_status(DO_LED_OP_STOP_ON)
        elif req_state == SCU_ST_DCDC_TEST_WAIT:
            self.evse.SetActivate_DCDCOnly()
            self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)
            self.change_scu_run_mode(APP_RUN_MODE_DCDC_TEST)
        elif req_state == SCU_ST_DCDC_TEST:
            pass
        elif req_state == SCU_ST_DRIVE_WAIT:
            self.update_led_status(DO_LED_DRIVE_ON)
        elif req_state == SCU_ST_DRIVING:
            pass
        elif req_state == SCU_ST_ERROR:
            self.evse.SetChargingControl(EVSE_STOP)
            self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)
        elif req_state == SCU_ST_SHUTDOWN:
            pass
        elif req_state == SCU_ST_EMERGENCY_STOP:
            self.change_scu_run_mode(APP_RUN_MODE_EM_STOP)
        elif req_state == SCU_ST_ADMIN:
            self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
            TheSys.dev.SetEVHVRelayOpen()
        elif req_state == SCU_ST_END:
            pass
        self.scu_param.state = req_state

    def StateMachine(self):
        state = self.scu_param.state
        selected = TheSys.dev.BCU_GetSelectedRunMode()
        req_mode = TheHmi.GetParam().hmi_conf.hmiRunMode
        ev_chg_ctrl = TheHmi.GetParam().hmi_status.hmiChargingControl
        bat_chg_ctrl = TheHmi.GetParam().hmi_status.hmiBatteryCharging
        evse_state = self.evse.GetState()
        secc_status = TheSys.secc.GetStatus()

        # update present SCU status
        self.UpdateSCUStatus()

        # update SECC alive status
        self.UpdateSECCStatus()

        log = "s:{0:1d}|".format(state)
        log += "m:{0:1d},{1:1d}|".format(req_mode, TheHmi.GetParam().scu_status.scuRunMode)
        log += "a:{0:1d},{1:d}|".format(TheSys.secc.IsActivated(),
                                        TheHmi.GetParam().hmi_status.hmiChargingControl)
        log += "ss:{0:1d},{1:1d}|".format(evse_state, secc_status)
        logger.debug(log)

        # check shutdown mode
        if self.is_shutdown_mode_selected(selected, req_mode):
            if TheSys.dev.BCU_GetKeyLockOpened():
                self.scu_transition(SCU_ST_SHUTDOWN)
            else:
                self.update_scu_status_direct(SCU_STS_SHUTDN_KEY_LOCK_STILL_ON)

        # check emergency mode
        if self.is_emergency_mode_selected(selected, req_mode):
            self.scu_transition(SCU_ST_EMERGENCY_STOP)

        if state == SCU_ST_BOOT:
            TheSys.sbms.SBMS_SetActivate()
            TheSys.sbms.SBMS_SetHVRelayClose()
            if TheSys.sbms.SBMS_GetHVRelayClosed():
                self.scu_transition(SCU_ST_IDLE)
        elif state == SCU_ST_IDLE:
            # self.change_scu_run_mode(selected)
            self.change_scu_run_mode(req_mode)
            if self.is_ev_chg_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_EV_CHG_WAIT)
            elif self.is_bat_chg_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_BAT_CHG_WAIT)
            elif self.is_drive_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_DRIVE_WAIT)
            elif self.is_test_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_DCDC_TEST_WAIT)
            elif self.is_chg_stop_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_STOPPING)
            elif self.is_admin_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_ADMIN)
        elif state == SCU_ST_EV_CHG_WAIT:
            if self.is_chg_start_requested(ev_chg_ctrl):
                # update EV charging parameter
                self.scu_param.ev_chg_mode = TheHmi.GetParam().hmi_conf.hmiChargingMode
                self.scu_param.ev_chg_time_sec = TheHmi.GetParam().hmi_conf.hmiChargingTime_min * SCU_MULT_MIN_TO_SEC
                self.scu_param.ev_chg_amount_wh = TheHmi.GetParam().hmi_conf.hmiChargingAmount_kWh * SCU_MULT_KWH_TO_WH

                self.scu_param.ev_chg_time_sec = min(self.scu_param.ev_chg_time_sec, SCU_MAX_EV_CHG_TIME_SEC)
                self.scu_param.ev_chg_amount_wh = min(self.scu_param.ev_chg_amount_wh, SCU_MAX_EV_CHG_AMOUNT_WH)

                if self.scu_param.ev_chg_mode > SCU_CHG_MODE_NONE:
                    self.scu_transition(SCU_ST_EV_CHG_SBMS_RELAY_CLOSE)
            else:
                if self.is_chg_stop_mode_selected(selected, req_mode) or self.is_chg_stop_requested(ev_chg_ctrl):
                    self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
                    self.scu_transition(SCU_ST_STOPPING)
        elif state == SCU_ST_EV_CHG_SBMS_RELAY_CLOSE:
            # EV relay is controlled in EVSE_StateMachine()
            # BAT relay is already closed
            if TheSys.sbms.SBMS_GetHVRelayClosed():
                if self.is_evse_state_idle(evse_state) and self.is_secc_status_idle(secc_status):
                    self.evse.SetChargingControl(EVSE_START)
                    self.scu_transition(SCU_ST_EV_CHG_RUNNING)
            else:
                if self.is_chg_stop_mode_selected(selected, req_mode) or self.is_chg_stop_requested(ev_chg_ctrl):
                    self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
                    self.scu_transition(SCU_ST_STOPPING)
        elif state == SCU_ST_EV_CHG_RUNNING:
            self.EVChargingRunning()
            # stop case 1 : EVSE abnormal
            if self.is_evse_terminated(evse_state):
                self.scu_transition(SCU_ST_STOPPING)
            # stop case 1 : EVSE had error
            elif self.had_evse_error(evse_state):
                self.scu_transition(SCU_ST_ERROR)
            # stop case 1 : DCDC converter had error
            elif self.had_dcdc_error():
                self.scu_transition(SCU_ST_ERROR)
            # stop case 2 : received stop signal from user
            if self.is_chg_stop_mode_selected(selected, req_mode) or self.is_chg_stop_requested(ev_chg_ctrl):
                self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
                self.scu_transition(SCU_ST_STOPPING)
            # stop case 3 : reached setting time or KWH
            if self.scu_param.sub_state == SCU_SUB_ST_EV_STOP:
                self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
                self.scu_transition(SCU_ST_STOPPING)

            # led control
            if secc_status == SECC_ST_CURRENT_DEMAND:
                self.update_led_status(DO_LED_EV_CHG_BLINK)
        elif state == SCU_ST_BAT_CHG_WAIT:
            if self.is_chg_start_requested(bat_chg_ctrl):
                self.scu_transition(SCU_ST_BAT_CHG_RUNNING)
            else:
                if self.is_chg_stop_mode_selected(selected, req_mode) or self.is_chg_stop_requested(bat_chg_ctrl):
                    self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
                    self.scu_transition(SCU_ST_STOPPING)
        elif state == SCU_ST_BAT_CHG_RUNNING:
            self.BATChargingRunning()
            if self.is_chg_stop_mode_selected(selected, req_mode) or self.is_chg_stop_requested(bat_chg_ctrl):
                self.scu_transition(SCU_ST_STOPPING)
        elif state == SCU_ST_STOPPING:
            self.update_led_status(DO_LED_EV_CHG_OFF)
            if self.is_evse_state_idle(evse_state) and self.is_secc_status_idle(secc_status):
                self.scu_transition(SCU_ST_STOPED)
        elif state == SCU_ST_STOPED:
            self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)
            self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)    # just in case
            TheSys.dev.BCU_SetEVHVRelayOpen()
            if TheSys.dev.BCU_GetEVHVRelayOpened():
                self.scu_transition(SCU_ST_IDLE)
        elif state == SCU_ST_DCDC_TEST_WAIT:
            if self.sbms.SBMS_GetHVRelayClosed():
                self.scu_transition(SCU_ST_DCDC_TEST)
            else:
                self.scu_transition(SCU_ST_STOPED)
        elif state == SCU_ST_DCDC_TEST:
            self.DCDCtestRunning()
            # stop case 1: change mode to idle
            if self.is_idle_mode_selected(selected, req_mode) or self.is_chg_stop_mode_selected(selected, req_mode):
                self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)
                self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)    # just in case
                self.scu_transition(SCU_ST_STOPED)
        elif state == SCU_ST_DRIVE_WAIT:
            self.sbms.SBMS_SetHVRelayClose()
            if self.sbms.SBMS_GetHVRelayClosed():
                self.scu_transition(SCU_ST_DRIVING)
        elif state == SCU_ST_DRIVING:
            # stop case 1
            if self.is_idle_mode_selected(selected, req_mode) or self.is_chg_stop_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_STOPED)
            self.update_led_status(DO_LED_DRIVE_BLINK)
        elif state == SCU_ST_ERROR:
            # EVHV relay is already opened in EVSE_StateMachine, but below is just in case.
            TheSys.dev.BCU_SetEVHVRelayOpen()
            self.update_HMIerrorcode_parameter(self.evse.GetEVErrorCode(),
                                               self.evse.GetSECCErrorCode(),
                                               self.evse.GetDCDCErrorCode(),
                                               TheSys.sbms.SBMS_GetErrorCode())
            self.scu_transition(SCU_ST_STOPPING)
        elif state == SCU_ST_SHUTDOWN:
            self.evse.SetNormalStopUser(EVSE_NSTOP_ON)
            TheSys.dev.BCU_SetEVHVRelayOpen()
            self.sbms.SBMS_SetHVRelayOpen()
            if TheSys.dev.BCU_GetEVHVRelayOpened() and self.sbms.SBMS_GetHVRelayOpened():
                self.change_scu_run_mode(APP_RUN_MODE_SHUTDOWN)
                TheSys.dev.BCU_SetPowerHoldRelayOpen()  # POWER OFF
        elif state == SCU_ST_EMERGENCY_STOP:
            # already processed in external interrupt service routine
            if TheSys.dev.BCU_GetEmergencyStop() == APP_FALSE:
                self.scu_transition(SCU_ST_STOPPING)
        elif state == SCU_ST_ADMIN:
            self.AdminRunning()
            if self.is_idle_mode_selected(selected, req_mode) or self.is_chg_stop_mode_selected(selected, req_mode):
                self.scu_transition(SCU_ST_IDLE)

    def EventExtEmergencyStop(self):
        self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)
        self.evse.SendDCDCControlON_Dir(APP_CEG_CONTROL_OFF)    # just in case
        self.evse.SetEmergencyStopUser(EVSE_ESTOP_ON)
        TheSys.dev.BCU_SetEVHVRelayOpen()
        # SBMS_SetHVRelayOpen(); ///\todo

    def SendDebugMessage(self):
        pass
