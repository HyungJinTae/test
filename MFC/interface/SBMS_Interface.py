# System BMS Communication Interface

from interface.SBMS_Header import *
from interface.KVASER_Interface import KVASER_Interface


class SBMS_Interface:
    def __init__(self, can_obj: KVASER_Interface):
        self.is_activated = False
        self.is_demand_activated = False
        self.can_obj = can_obj

        self.sbms_param = SBMS_Param()

    #######################
    # porting c code functions
    #######################
    def SBMS_Init(self):
        pass

    def SBMS_SetActivate(self):
        self.sbms_param.is_activated = SBMS_ACTIVATED

    def SBMS_SetDeactivate(self):
        self.sbms_param.is_activated = SBMS_DEACTIVATED

    def SBMS_SetHVRelayOpen(self):
        self.sbms_param.hv_relay = SBMS_RELAY_OPENED

    def SBMS_SetHVRelayClose(self):
        self.sbms_param.hv_relay = SBMS_RELAY_CLOSED

    def SBMS_GetIMDstatusOK(self):
        return self.sbms_param.imd_status

    def SBMS_GetHVRelayClosed(self):
        res = APP_FALSE
        if self.sbms_param.hv_relay_status == SBMS_RELAY_CLOSED:
            res = APP_TRUE
        return res

    def SBMS_GetHVRelayOpened(self):
        res = APP_FALSE
        if self.sbms_param.hv_relay_status == SBMS_RELAY_OPENED:
            res = APP_TRUE
        return res

    def SBMS_GetBatterySOC(self):
        return 0

    def SBMS_GetBatteryVoltage(self):
        return 0

    def SBMS_GetBatteryCurrent(self):
        return 0

    def SBMS_GetMaxPowerAmountWh(self):
        return 0

    def SBMS_GetIMDStatus(self):
        return 0

    def SBMS_GetActivate(self):
        return self.sbms_param.is_activated

    def SBMS_GetState(self):
        return self.sbms_param.state

    def SBMS_GetErrorCode(self):
        return 0

    def SBMS_StateMachine(self):
        # for test
        self.sbms_param.hv_relay_status = self.sbms_param.hv_relay
        self.sbms_param.imd_status = APP_TRUE


