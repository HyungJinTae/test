# DC-DC TEST Program

import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from common.QtWidgets_Functions import *
from controller.SYS_Singleton import TheSys
from controller.EVSE_Header import *
from controller.EVSE import EVSE

form_class = uic.loadUiType("SECC_TEST.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui_initialize()

        self.task1 = QTimer(self)
        QTimer_Init(self.task1, 1, self.Task1ms)
        self.task50 = QTimer(self)
        QTimer_Init(self.task50, 50, self.Task50ms)
        self.task200 = QTimer(self)
        QTimer_Init(self.task200, 200, self.Task200ms)
        self.task500 = QTimer(self)
        QTimer_Init(self.task500, 500, self.Task500ms)

        self.evse = EVSE()
        self.evse.Init()
        self.update_ui_count = 0
        self.activated_check_count = 0

    def ui_initialize(self):
        PushButton_ClickedConnect(self.pbCtrlInitializePPMT, self.on_pbCtrlInitializePPMT)
        PushButton_ClickedConnect(self.pbCtrlEVSENStop, self.on_pbCtrlEVSENStop)
        PushButton_ClickedConnect(self.pbCtrlEVSEEStop, self.on_pbCtrlEVSEEStop)
        PushButton_ClickedConnect(self.pbCtrlInitializePPMT_2, self.on_pbCtrlInitializePPMT_2)
        PushButton_ClickedConnect(self.pbCtrlEVSENStop_2, self.on_pbCtrlEVSENStop_2)
        PushButton_ClickedConnect(self.pbCtrlEVSEEStop_2, self.on_pbCtrlEVSEEStop_2)
        CheckBox_StateChangedConnect(self.cbStartComm, self.on_cbStartComm)

    def ui_update(self):
        self.update_ui_count += 1
        rx_count = TheSys.secc.secc_param.secc_var.rx_count
        alive_count = self.update_ui_count
        active = TheSys.secc.secc_param.secc_var.is_activated
        status = TheSys.secc.secc_param.secc_status3.seccStatus
        secc_version = "{0:d}.{1:d}.{2:d}".format(TheSys.secc.secc_param.secc_status1.seccVersionMajor,
                                                  TheSys.secc.secc_param.secc_status1.seccVersionMinor,
                                                  TheSys.secc.secc_param.secc_status1.seccVersionPatch)
        secc_heartbeat = TheSys.secc.secc_param.secc_status1.seccHeartbeat
        cp_osc = TheSys.secc.secc_param.secc_status2.cpOscillator
        cp_voltage = TheSys.secc.secc_param.secc_status2.f_cpVoltage
        error = bool(status == 252)
        secc_err_code = TheSys.secc.secc_param.secc_status1.seccErrorCode
        ev_err_code = TheSys.secc.secc_param.secc_status1.evErrorCode
        LineEdit_SetTextFromInt(self.leRxCount, rx_count)
        LineEdit_SetTextFromInt(self.leAliveCount, alive_count)
        RadioButton_SetChecked(self.rbStsActive, active)
        RadioButton_SetChecked(self.rbStsInactive, not active)
        LineEdit_SetText(self.leSECCversion, secc_version)
        LineEdit_SetTextFromInt(self.leSECCheartbeat, secc_heartbeat)
        LineEdit_SetTextFromInt(self.leSECCStatus, status)
        LineEdit_SetTextFromInt(self.leCpOsc, cp_osc)
        LineEdit_SetTextFromFloat(self.leCpVoltage, cp_voltage)
        RadioButton_SetChecked(self.rbErrNormal, not error)
        RadioButton_SetChecked(self.rbErrError, error)
        e_code = "{0:08x}".format(secc_err_code)
        LineEdit_SetText(self.leSECCErrCode, e_code)
        e_code = "{0:08x}".format(ev_err_code)
        LineEdit_SetText(self.leEVErrCode, e_code)

    def on_pbCtrlInitializePPMT(self):
        logger.info("")
        self.evse.SetChargingControl(EVSE_START)

    def on_pbCtrlEVSENStop(self):
        logger.info("")
        self.evse.SetNormalStopUser(EVSE_NSTOP_ON)

    def on_pbCtrlEVSEEStop(self):
        logger.info("")
        self.evse.SetEmergencyStopUser(EVSE_ESTOP_ON)

    def on_pbCtrlInitializePPMT_2(self):
        logger.info("")
        self.evse.SetChargingControl(EVSE_STOP)

    def on_pbCtrlEVSENStop_2(self):
        logger.info("")
        self.evse.SetNormalStopUser(EVSE_NSTOP_OFF)

    def on_pbCtrlEVSEEStop_2(self):
        logger.info("")
        self.evse.SetEmergencyStopUser(EVSE_ESTOP_OFF)

    def on_cbStartComm(self):
        logger.info(f"{CheckBox_IsChecked(self.cbStartComm)}")
        if CheckBox_IsChecked(self.cbStartComm):
            self.evse.SetActivate()
        else:
            self.evse.SetDeactivate()

    def Task1ms(self):
        self.evse.RecvDataProcess()

    def Task50ms(self):
        self.evse.Process50ms()
        self.evse.StateMachine()

    def Task200ms(self):
        self.evse.Process200ms()

    def Task500ms(self):
        self.ui_update()
        self.activated_check_count += 1
        if self.activated_check_count > 2:
            TheSys.secc.Process1000ms()
            self.activated_check_count = 0


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
