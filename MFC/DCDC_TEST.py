# DC-DC TEST Program

import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from interface.CEG_Header import *
from common.QtWidgets_Functions import *
from controller.SYS_Singleton import TheSys

form_class = uic.loadUiType("DCDC_TEST.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pstack = TheSys
        self.pstack.ceg.SetDemandEnable(enable=True)
        self.ui_initialize()

        self.cmd_pstack_voltage = LineEdit_GetTextToFloat(self.leSetOutputVoltage)
        self.cmd_pstack_total_current = float(0)
        self.update_ui_count = 0

        self.task1 = QTimer(self)
        self.task1.start(1)
        self.task1.timeout.connect(self.Task1ms)
        self.task50 = QTimer(self)
        self.task50.start(50)
        self.task50.timeout.connect(self.Task50ms)
        self.task100 = QTimer(self)
        self.task100.start(100)
        self.task100.timeout.connect(self.Task100ms)
        self.task500 = QTimer(self)
        self.task500.start(500)
        self.task500.timeout.connect(self.Task500ms)

    def ui_initialize(self):
        PushButton_ClickedConnect(self.pbSetOutputVoltage, self.on_pbSetOutputVoltage)
        PushButton_ClickedConnect(self.pbSetOutputTotalCurrent, self.on_pbSetOutputTotalCurrent)
        PushButton_ClickedConnect(self.pbSetControlOn, self.on_pbSetControlOn)
        PushButton_ClickedConnect(self.pbSetControlOff, self.on_pbSetControlOff)
        PushButton_ClickedConnect(self.pbSetWalkInOn, self.on_pbSetWalkInOn)
        PushButton_ClickedConnect(self.pbSetWalkInOff, self.on_pbSetWalkInOff)
        RadioButton_ClickedConnect(self.rbModule0_Blink, self.on_rbModule0_Blink)
        RadioButton_ClickedConnect(self.rbModule1_Blink, self.on_rbModule1_Blink)

    def on_pbSetOutputVoltage(self):
        self.cmd_pstack_voltage = LineEdit_GetTextToFloat(self.leSetOutputVoltage)
        logger.debug(f"{self.cmd_pstack_voltage}[V], {self.cmd_pstack_total_current}[A]")
        self.pstack.ceg.WriteGroupDCOutput(self.cmd_pstack_voltage, self.cmd_pstack_total_current)

    def on_pbSetOutputTotalCurrent(self):
        self.cmd_pstack_total_current = LineEdit_GetTextToFloat(self.leSetOutputTotalCurrent)
        logger.debug(f"{self.cmd_pstack_voltage}[V], {self.cmd_pstack_total_current}[A]")
        self.pstack.ceg.WriteGroupDCOutput(self.cmd_pstack_voltage, self.cmd_pstack_total_current)

    def on_pbSetControlOn(self):
        logger.debug(f"")
        self.pstack.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_ON)

    def on_pbSetControlOff(self):
        logger.debug(f"")
        self.pstack.ceg.WriteGroupControlOn(CEG_DEF_CONTROL_OFF)

    def on_pbSetWalkInOn(self):
        logger.debug(f"")
        self.pstack.ceg.WriteGroupWalkIn(CEG_DEF_WALK_IN_ENABLE)

    def on_pbSetWalkInOff(self):
        logger.debug(f"")
        self.pstack.ceg.WriteGroupWalkIn(CEG_DEF_WALK_IN_DISABLE)

    def on_rbModule0_Blink(self):
        logger.debug(f"")
        if RadioButton_isChecked(self.rbModule0_Blink):
            self.pstack.ceg.WriteModuleLedBlink(APP_CEG_MODULE0_ID, CEG_DEF_GREEN_LED_BLINK)
        else:
            self.pstack.ceg.WriteModuleLedBlink(APP_CEG_MODULE0_ID, CEG_DEF_GREEN_LED_NORMAL)

    def on_rbModule1_Blink(self):
        logger.debug(f"")
        if RadioButton_isChecked(self.rbModule1_Blink):
            self.pstack.ceg.WriteModuleLedBlink(APP_CEG_MODULE1_ID, CEG_DEF_GREEN_LED_BLINK)
        else:
            self.pstack.ceg.WriteModuleLedBlink(APP_CEG_MODULE1_ID, CEG_DEF_GREEN_LED_NORMAL)

    def Task1ms(self):
        self.pstack.Response_Infy()

    def Task50ms(self):
        self.pstack.DemandTask50ms_CEG()

    def Task100ms(self):
        self.pstack.DemandTask100ms_CEG()

    def Task500ms(self):
        self.pstack.DemandTask1000ms_CEG()
        self.update_ui()

    def update_ui(self):
        try:
            self.update_ui_count += 1
            LineEdit_SetTextFromInt(self.leAliveCount, self.update_ui_count)
            LineEdit_SetTextFromInt(self.leRxCount, self.pstack.ceg.demand_response_count)
            LineEdit_SetTextFromInt(self.leGroupNo, self.pstack.ceg.group_address)
            LineEdit_SetTextFromInt(self.leGroupModuleCount, self.pstack.ceg.module_numbers_in_group)
            LineEdit_SetTextFromFloat(self.lePresentVoltage, self.pstack.ceg.group_dc_side_voltage)
            LineEdit_SetTextFromFloat(self.lePresentTotalCurrent, self.pstack.ceg.group_dc_side_total_current)
            RadioButton_SetChecked(self.rbControlOn, self.pstack.ceg.GetGroupControlOn())
            RadioButton_SetChecked(self.rbWalkInOn, self.pstack.ceg.GetGroupWalkInEnable())
            RadioButton_SetChecked(self.rbDCsideOff, not self.pstack.ceg.GetGroupControlOn())
            # module 0
            LineEdit_SetTextFromInt(self.leModule0_No, self.pstack.ceg.dict_param[APP_CEG_MODULE0_ID].module_ID)
            LineEdit_SetTextFromFloat(self.leModule0_Voltage, self.pstack.ceg.GetModuleDCOutputVoltage(APP_CEG_MODULE0_ID))
            LineEdit_SetTextFromFloat(self.leModule0_Current, self.pstack.ceg.GetModuleDCOutputCurrent(APP_CEG_MODULE0_ID))
            LineEdit_SetTextFromInt(self.leModule0_Temp, self.pstack.ceg.GetModuleTemperature(APP_CEG_MODULE0_ID))
            LineEdit_SetTextFromFloat(self.leModule0_InputVoltage, self.pstack.ceg.GetModuleDCInputVoltage(APP_CEG_MODULE0_ID))
            alarm_code_text = "{0:08x}".format(self.pstack.ceg.GetAlarmCode(APP_CEG_MODULE0_ID))
            LineEdit_SetText(self.leModule0_AlarmCode, alarm_code_text)
            RadioButton_SetChecked(self.rbModule0_Alarm, self.pstack.ceg.GetAlarm(APP_CEG_MODULE0_ID))
            # module 1
            LineEdit_SetTextFromInt(self.leModule1_No, self.pstack.ceg.dict_param[APP_CEG_MODULE1_ID].module_ID)
            LineEdit_SetTextFromFloat(self.leModule1_Voltage, self.pstack.ceg.GetModuleDCOutputVoltage(APP_CEG_MODULE1_ID))
            LineEdit_SetTextFromFloat(self.leModule1_Current, self.pstack.ceg.GetModuleDCOutputCurrent(APP_CEG_MODULE1_ID))
            LineEdit_SetTextFromInt(self.leModule1_Temp, self.pstack.ceg.GetModuleTemperature(APP_CEG_MODULE1_ID))
            LineEdit_SetTextFromFloat(self.leModule1_InputVoltage, self.pstack.ceg.GetModuleDCInputVoltage(APP_CEG_MODULE1_ID))
            alarm_code_text = "{0:08x}".format(self.pstack.ceg.GetAlarmCode(APP_CEG_MODULE1_ID))
            LineEdit_SetText(self.leModule1_AlarmCode, alarm_code_text)
            RadioButton_SetChecked(self.rbModule1_Alarm, self.pstack.ceg.GetAlarm(APP_CEG_MODULE1_ID))
        except Exception as e:
            logger.warning(f"e->{e}")


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
