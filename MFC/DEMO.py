# DEMO Program

import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from common.App_Header import *
from common.QtWidgets_Functions import *
from interface.HMI_Header import *
from controller.HMI_Singleton import TheHmi
from controller.TaskOS import TaskOS

from controller.SYS_Singleton import TheSys

form_class = uic.loadUiType("DEMO.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui_initialize()

        self.tos = TaskOS()
        self.tos.Init()

        self.state = 0
        self.ev_power = float(0)
        self.bat_power = float(0)
        self.ev_power_kwh = float(0)
        self.Hour_Epd = 0
        self.Min_Epd = 0
        self.Sec_Epd = 0
        self.Hour_Rmd = 0
        self.Min_Rmd = 0
        self.Sec_Rmd = 0
        self.Sec = 0

        self.task50 = QTimer(self)
        QTimer_Init(self.task50, 50, self.state_machine)

        self.task1000 = QTimer(self)
        QTimer_Init(self.task1000, 1000, self.ui_update)

    def ui_initialize(self):
        PushButton_ClickedConnect(self.pbChgStart, self.on_pbChgStart)
        PushButton_ClickedConnect(self.pbChgStop, self.on_pbChgStop)
        LineEdit_SetTextFromInt(self.leSetChgTime, 15)
        LineEdit_SetTextFromInt(self.leSetChgAmount, 5)
        RadioButton_SetChecked(self.rbSetChgTime, True)
        PushButton_ClickedConnect(self.pbAcStart, self.on_pbAcStart)
        PushButton_ClickedConnect(self.pbAcStop, self.on_pbAcStop)
        PushButton_ClickedConnect(self.pbAirCoolerTempSet, self.on_pbAirCoolerTempSet)
        PushButton_ClickedConnect(self.pbAirCoolerHumiditySet, self.on_pbAirCoolerHumiditySet)
        PushButton_ClickedConnect(self.pbAirCoolerTempDifferenceSet, self.on_pbAirCoolerTempDifferenceSet)
        PushButton_ClickedConnect(self.pbInvStart, self.on_pbInvStart)
        PushButton_ClickedConnect(self.pbInvStop, self.on_pbInvStop)

    def ui_update(self):
        #if TabWidget_CurrentIndex(self.tabWidget) == 0:
        self.ui_update_tap1()
        #elif TabWidget_CurrentIndex(self.tabWidget) == 1:
        self.ui_update_tap2()

    def ui_update_tap1(self):
        """ EV Monitoring """
        ev_soc = TheHmi.GetParam().ev_status.evSOC
        ev_voltage = TheHmi.GetParam().ev_status.evPresentVoltage
        ev_current = TheHmi.GetParam().ev_status.evPresentCurrent
        self.ev_power = (ev_voltage * ev_current) * 0.001
        self.ev_power_kwh += (self.ev_power / 3600)
        LineEdit_SetTextFromFloat(self.leEvSOC, ev_soc)
        LineEdit_SetTextFromFloat(self.leEvVoltage, ev_voltage)
        LineEdit_SetTextFromFloat(self.leEvCurrent, ev_current)
        LineEdit_SetTextFromFloat(self.leEvPower, self.ev_power)
        LineEdit_SetTextFromFloat(self.leEvPowerkWh, self.ev_power_kwh)

        if TheHmi.GetParam().hmi_status.hmiChargingControl is HMI_CHG_CTRL_START_CHG:
            self.Sec += 1
            self.Elapsed_Time_Calc()

            if RadioButton_isChecked(self.rbSetChgTime):
                self.ChgTimeSet_RemainingTime_Calc()
            elif RadioButton_isChecked(self.rbSetChgAmount):
                self.ChgAmountSet_RemainingTime_Calc()

        ev_chg_elapsed_time_text = "{0:02d}:{1:02d}:{2:02d}".format(self.Hour_Epd, self.Min_Epd, self.Sec_Epd)
        ev_chg_remained_time_text = "{0:02d}:{1:02d}:{2:02d}".format(self.Hour_Rmd, self.Min_Rmd, self.Sec_Rmd)
        LineEdit_SetText(self.leEvChgEpdTime, ev_chg_elapsed_time_text)
        LineEdit_SetText(self.leEvChgRmdTime, ev_chg_remained_time_text)

        """ BAT Monitoring """
        bat_soc = TheHmi.GetParam().bat_status.batSOC
        bat_voltage = TheHmi.GetParam().bat_status.batPresentVoltage
        bat_current = TheHmi.GetParam().bat_status.batPresentCurrent
        self.bat_power = (bat_voltage * bat_current) * 0.001
        LineEdit_SetTextFromFloat(self.leBatSOC, bat_soc)
        LineEdit_SetTextFromFloat(self.leBatVoltage, bat_voltage)
        LineEdit_SetTextFromFloat(self.leBatCurrent, bat_current)
        LineEdit_SetTextFromFloat(self.leBatPower, self.bat_power)

        """ SCU, SECC State """
        LineEdit_SetTextFromInt(self.leScuState1, TheHmi.GetParam().scu_status.scuRunMode)
        LineEdit_SetTextFromInt(self.leScuState2, TheHmi.GetParam().scu_status.scuStatus)
        LineEdit_SetTextFromInt(self.leSeccState, TheHmi.GetParam().scu_status.scuSECCactivated)

        """ Error Monitoring """
        secc_ecode_txt = "0x{0:08x}".format(TheHmi.GetParam().scu_ecode.scuECode_SECC)
        LineEdit_SetText(self.leSeccErrCode, secc_ecode_txt)
        if TheHmi.GetParam().scu_ecode.scuECode_SECC != 0:
            RadioButton_SetChecked(self.rbSECCError, True)
        else:
            RadioButton_SetChecked(self.rbSECCError, False)
        ceg_ecode_txt = "0x{0:08x}".format(TheHmi.GetParam().scu_ecode.scuECode_DCDC)
        LineEdit_SetText(self.leCegErrrCode, ceg_ecode_txt)
        if TheHmi.GetParam().scu_ecode.scuECode_DCDC != 0:
            RadioButton_SetChecked(self.rbCEGError, True)
        else:
            RadioButton_SetChecked(self.rbCEGError, False)
        bat_ecode_txt = "0x{0:08x}".format(TheHmi.GetParam().scu_ecode.scuECode_SBMS)
        LineEdit_SetText(self.leBatErrCode, bat_ecode_txt)
        if TheHmi.GetParam().scu_ecode.scuECode_SBMS != 0:
            RadioButton_SetChecked(self.rbBATError, True)
        else:
            RadioButton_SetChecked(self.rbBATError, False)

    def ui_update_tap2(self):
        LineEdit_SetTextFromFloat(self.leInvL1Voltage, TheSys.beg.dict_param[0].ac_a_phase_voltage)
        LineEdit_SetTextFromFloat(self.leInvL2Voltage, TheSys.beg.dict_param[0].ac_b_phase_voltage)
        LineEdit_SetTextFromFloat(self.leInvL3Voltage, TheSys.beg.dict_param[0].ac_c_phase_voltage)
        LineEdit_SetTextFromFloat(self.leInvL1Current, TheSys.beg.dict_param[0].ac_a_phase_current)
        LineEdit_SetTextFromFloat(self.leInvL2Current, TheSys.beg.dict_param[0].ac_b_phase_current)
        LineEdit_SetTextFromFloat(self.leInvL3Current, TheSys.beg.dict_param[0].ac_c_phase_current)

        if TheHmi.GetParam().aircooler_conf.AcRunMode == 0:
            RadioButton_SetChecked(self.rbAcStartMon, False)
            RadioButton_SetChecked(self.rbAcStopMon, True)
        else:
            RadioButton_SetChecked(self.rbAcStopMon, False)
            RadioButton_SetChecked(self.rbAcStartMon, True)

        LineEdit_SetTextFromFloat(self.leAcTempMon, TheHmi.GetParam().aircooler_conf.AcSetTemp)
        LineEdit_SetTextFromInt(self.leAcHumidityMon, TheHmi.GetParam().aircooler_conf.AcSetHumidity)
        LineEdit_SetTextFromFloat(self.leAcTempDiffMon, TheHmi.GetParam().aircooler_conf.AcSetTempDiff)

        LineEdit_SetTextFromFloat(self.leAcPresentTempInMon, TheHmi.GetParam().aircooler_status.AcPresentTempIn)
        LineEdit_SetTextFromFloat(self.leAcPresentTempOutMon, TheHmi.GetParam().aircooler_status.AcPresentTempOut)
        LineEdit_SetTextFromInt(self.leAcPresentHumidityMon, TheHmi.GetParam().aircooler_status.AcPresentHumidity)

        ac_ecode_txt = "0x{0:04x}".format(TheHmi.GetParam().aircooler_status.AcError)
        LineEdit_SetText(self.leAcErrorCode, ac_ecode_txt)

    def state_machine(self):
        hmiRunMode = TheHmi.GetParam().hmi_conf.hmiRunMode
        scuRunMode = TheHmi.GetParam().scu_status.scuRunMode

        if self.state == 0:
            if hmiRunMode == APP_RUN_MODE_EV_CHARGING:
                self.state = 1
        elif self.state == 1:
            if scuRunMode == APP_RUN_MODE_STOPPING:
                TheHmi.GetParam().hmi_status.hmiChargingControl = HMI_CHG_CTRL_STOP_CHG
                self.state = 2
        elif self.state == 2:
            if scuRunMode == APP_RUN_MODE_IDLE:
                TheHmi.GetParam().hmi_conf.hmiRunMode = APP_RUN_MODE_IDLE
                self.state = 0

    def on_pbAcStart(self):
        TheHmi.GetParam().aircooler_conf.AcRunMode = 1

    def on_pbAcStop(self):
        TheHmi.GetParam().aircooler_conf.AcRunMode = 0

    def on_pbAirCoolerTempSet(self):
        TheHmi.GetParam().aircooler_conf.AcSetTemp = LineEdit_GetTextToFloat(self.leAcSetTemp)

    def on_pbAirCoolerHumiditySet(self):
        TheHmi.GetParam().aircooler_conf.AcSetHumidity = LineEdit_GetTextToInt(self.leAcSetHumidity)

    def on_pbAirCoolerTempDifferenceSet(self):
        TheHmi.GetParam().aircooler_conf.AcSetTempDiff = LineEdit_GetTextToFloat(self.leAcSetTempDiff)

    def on_pbChgStart(self):
        chg_start = False
        try:
            time_ = LineEdit_GetTextToInt(self.leSetChgTime)
            amount = LineEdit_GetTextToInt(self.leSetChgAmount)
            chg_start = True
        except Exception as e:
            logger.warning(f"e->{e}")
            time_ = 0
            amount = 0
            LineEdit_SetTextFromInt(self.leSetChgTime, time_)
            LineEdit_SetTextFromInt(self.leSetChgAmount, amount)

        TheHmi.GetParam().hmi_conf.hmiChargingTime_min = time_
        TheHmi.GetParam().hmi_conf.hmiChargingAmount_kWh = amount
        if RadioButton_isChecked(self.rbSetChgTime):
            TheHmi.GetParam().hmi_conf.hmiChargingMode = HMI_CHG_MODE_CHARGING_TIME
        elif RadioButton_isChecked(self.rbSetChgAmount):
            TheHmi.GetParam().hmi_conf.hmiChargingMode = HMI_CHG_MODE_CHARGING_AMOUNT
        else:
            TheHmi.GetParam().hmi_conf.hmiChargingMode = HMI_CHG_MODE_NONE

        if chg_start:
            TheHmi.GetParam().hmi_status.hmiChargingControl = HMI_CHG_CTRL_START_CHG
            TheHmi.GetParam().hmi_conf.hmiRunMode = APP_RUN_MODE_EV_CHARGING
        logger.debug(f"{TheHmi.GetParam().hmi_status.hmiChargingControl}, {time_}, {amount}")

    def on_pbChgStop(self):
        TheHmi.GetParam().hmi_status.hmiChargingControl = HMI_CHG_CTRL_STOP_CHG
        logger.debug(f"{TheHmi.GetParam().hmi_status.hmiChargingControl}")
        self.Charge_Stop_Init()

    def on_pbInvStart(self):
        TheSys.beg.group_dc_side_voltage = LineEdit_GetTextToFloat(self.leInvDCVoltage)
        TheSys.beg.group_dc_side_total_current = LineEdit_GetTextToFloat(self.leInvDCCurrent)

    def on_pbInvStop(self):
        pass

    def Elapsed_Time_Calc(self):
        Set_Hour = 0
        Set_Min = 0
        Set_Sec = self.Sec

        if Set_Sec > 59:
            Set_Min = Set_Sec / 60
            Set_Sec = Set_Sec % 60
            if Set_Min > 59:
                Set_Hour = Set_Min / 60
                Set_Min = Set_Min % 60

        self.Hour_Epd = int(Set_Hour)
        self.Min_Epd = int(Set_Min)
        self.Sec_Epd = int(Set_Sec)

    def ChgTimeSet_RemainingTime_Calc(self):
        Set_Hour = 0
        Set_Min = 0
        Set_Sec = (TheHmi.GetParam().hmi_conf.hmiChargingTime_min * 60) - self.Sec

        if Set_Sec == 0:
            self.on_pbChgStop()

        if Set_Sec > 59:
            Set_Min = Set_Sec / 60
            Set_Sec = Set_Sec % 60
            if Set_Min > 59:
                Set_Hour = Set_Min / 60
                Set_Min = Set_Min % 60

        self.Hour_Rmd = int(Set_Hour)
        self.Min_Rmd = int(Set_Min)
        self.Sec_Rmd = int(Set_Sec)

    def ChgAmountSet_RemainingTime_Calc(self):
        Set_Hour = 0
        Set_Min = 0
        Set_Sec = 0


        kWh = (self.ev_power / 3600)
        if kWh != 0:
            Set_Sec = int(TheHmi.GetParam().hmi_conf.hmiChargingAmount_kWh / kWh) - self.Sec

        if Set_Sec == 0:
            self.on_pbChgStop()

        if Set_Sec > 59:
            Set_Min = Set_Sec / 60
            Set_Sec = Set_Sec % 60
            if Set_Min > 59:
                Set_Hour = Set_Min / 60
                Set_Min = Set_Min % 60

        self.Hour_Rmd = int(Set_Hour)
        self.Min_Rmd = int(Set_Min)
        self.Sec_Rmd = int(Set_Sec)

    def Charge_Stop_Init(self):
        self.Sec = 0
        self.Hour_Epd = 0
        self.Min_Epd = 0
        self.Sec_Epd = 0
        self.Hour_Rmd = 0
        self.Min_Rmd = 0
        self.Sec_Rmd = 0
        self.ev_power_kwh = 0

if __name__ == "__main__":
    try:
        logger.info("Start..")
        logger.debug("Start..")
        app = QApplication(sys.argv)
        myWindow = WindowClass()
        myWindow.show()
        app.exec_()
    except Exception as e:
        logger.error(f"e->{e}")