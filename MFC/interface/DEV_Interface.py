from common.App_Header import *
from interface.DEV_Header import *
from interface.KVASER_Interface import KVASER_Interface


class DEV_Interface:
    def __init__(self, can_obj: KVASER_Interface):
        self.is_activated = False
        self.is_demand_activated = False
        self.can_obj = can_obj

        self.ev_hv_relay_opened = False
        self.timeout = [time.time()] * DEV_TIMEOUT_ID_END
        self.selected_mode = APP_RUN_MODE_IDLE
        self.emergency_stop_mode = APP_FALSE

    #######################
    # porting c code functions
    #######################
    def GetDI(self, eDiChannel):
        return 0

    def SetDO(self, eDoChannel):
        pass

    def BCU_Init(self):
        pass

    def BCU_ResetTimeout_EVSE(self):
        self.timeout[DEV_TIMEOUT_ID_EVSE] = time.time()

    def BCU_ResetTimeout_MODE(self):
        self.timeout[DEV_TIMEOUT_ID_MODE] = time.time()

    def BCU_ResetTimeout_HMI(self):
        self.timeout[DEV_TIMEOUT_ID_HMI] = time.time()

    def BCU_ResetTimeout_EVCHG(self):
        self.timeout[DEV_TIMEOUT_ID_EVCHG] = time.time()

    def BCU_Timeout_EVSE(self, msec):
        res = 0
        sec = msec * 0.001
        if (time.time() - self.timeout[DEV_TIMEOUT_ID_EVSE]) > sec:
            res = 1
        return res

    def BCU_Timeout_MODE(self, msec):
        res = 0
        sec = msec * 0.001
        if (time.time() - self.timeout[DEV_TIMEOUT_ID_MODE]) > sec:
            res = 1
        return res

    def BCU_Timeout_HMI(self, msec):
        res = 0
        sec = msec * 0.001
        if (time.time() - self.timeout[DEV_TIMEOUT_ID_HMI]) > sec:
            res = 1
        return res

    def BCU_Timeout_EVCHG(self, msec):
        res = 0
        sec = msec * 0.001
        if (time.time() - self.timeout[DEV_TIMEOUT_ID_EVCHG]) > sec:
            res = 1
        return res

    def BCU_PresentTime_EVCHG(self):
        return self.timeout[DEV_TIMEOUT_ID_EVCHG]

    def BCU_SetEVHVRelayClose(self):
        self.SetDO(DO_HV_EV_RELAY_ON)

    def BCU_SetEVHVRelayOpen(self):
        self.SetDO(DO_HV_EV_RELAY_OFF)

    def BCU_SetRunModeLED(self, led):
        if (led < DO_LED_DRIVE_ON) or (led > DO_LED_OP_STOP_BLINK): return
        self.SetDO(led)

    def BCU_GetEVHVRelayClosed(self):
        res = 0
        if self.GetDI(DI_HV_EV_RELAY_FB):
            res = APP_TRUE
        return res

    def BCU_GetEVHVRelayOpened(self):
        res = 0
        if self.GetDI(DI_HV_EV_RELAY_FB) == APP_FALSE:
            res = APP_TRUE
        return res

    def BCU_GetEmergencyStop(self):
        return self.emergency_stop_mode

    def BCU_GetSelectedRunMode(self):
        if self.BCU_Timeout_MODE(100):
            self.BCU_ResetTimeout_MODE()
            if self.GetDI(DI_RM_DRIVE):
                self.selected_mode = APP_RUN_MODE_DRIVE
            elif self.GetDI(DI_RM_EV_CHG):
                self.selected_mode = APP_RUN_MODE_EV_CHARGING
            elif self.GetDI(DI_RM_BAT_CHG):
                self.selected_mode = APP_RUN_MODE_BATTERY_CHARGING
            else:
                self.selected_mode = APP_RUN_MODE_IDLE

            # stop request mode, it should be able to be set up from anywhere.
            if self.GetDI(DI_RM_OP_STOP):
                self.selected_mode = APP_RUN_MODE_STOPPING

            # emergency stop mode
            if self.emergency_stop_mode:
                self.selected_mode = APP_RUN_MODE_EM_STOP
        return self.selected_mode

