# BEG TEST Program

import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from common.QtWidgets_Functions import *
from controller.SYS_Singleton import TheSys

form_class = uic.loadUiType("BEG_TEST.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui_initialize()

        self.task1 = QTimer(self)
        self.task1.start(1)
        self.task1.timeout.connect(self.Task1ms)
        self.task500 = QTimer(self)
        self.task500.start(500)
        self.task500.timeout.connect(self.Task500ms)

        self.selectedModuleID = 0
        self.update_ui_count = 0

    def ui_initialize(self):
        PushButton_ClickedConnect(self.pbCtrlVo, self.on_pbCtrlVo)
        PushButton_ClickedConnect(self.pbCtrlIo, self.on_pbCtrlIo)
        RadioButton_ClickedConnect(self.rbModeRectify, self.on_rbCtrlMode)
        RadioButton_ClickedConnect(self.rbModeInverter, self.on_rbCtrlMode)
        RadioButton_ClickedConnect(self.rbCtrlOn, self.on_rbCtrlOnOff)
        RadioButton_ClickedConnect(self.rbCtrlOff, self.on_rbCtrlOnOff)
        RadioButton_ClickedConnect(self.rbCtrlAllOn, self.on_rbCtrlOnOff)
        RadioButton_ClickedConnect(self.rbCtrlAllOff, self.on_rbCtrlOnOff)
        RadioButton_ClickedConnect(self.rbCtrlWalkInEnable, self.on_rbCtrlWalkIn)
        RadioButton_ClickedConnect(self.rbCtrlWalkInDisable, self.on_rbCtrlWalkIn)
        ComboBox_AddItem(self.cbbModuleAddress, "MODULE 0")
        ComboBox_IndexChangedConnect(self.cbbModuleAddress, self.on_cbbModuleAddress)
        CheckBox_StateChangedConnect(self.cbStartQuery, self.on_cbStartQuery)
        CheckBox_SetChecked(self.cbStartQuery, TheSys.beg.is_activated)

    def on_pbCtrlVo(self):
        voltage = LineEdit_GetTextToFloat(self.leCtrlVo)
        logger.debug(f"{voltage}")
        TheSys.beg.write_system_info_dc_voltage(voltage)

    def on_pbCtrlIo(self):
        current = LineEdit_GetTextToFloat(self.leCtrlIo)
        logger.debug(f"{current}")
        TheSys.beg.write_system_info_dc_total_current(current)

    def on_rbCtrlMode(self):
        if RadioButton_isChecked(self.rbModeInverter):
            TheSys.beg.write_single_module_ac_info_working_mode_inverter(self.selectedModuleID)
        elif RadioButton_isChecked(self.rbModeRectify):
            TheSys.beg.write_single_module_ac_info_working_mode_rectification(self.selectedModuleID)

    def on_rbCtrlOnOff(self):
        logger.debug(f"{RadioButton_isChecked(self.rbCtrlOn)}, {RadioButton_isChecked(self.rbCtrlOff)},"
                     f"{RadioButton_isChecked(self.rbCtrlAllOn)}, {RadioButton_isChecked(self.rbCtrlAllOff)}")
        if RadioButton_isChecked(self.rbCtrlOn):
            TheSys.beg.write_single_module_info_control_on(self.selectedModuleID)
        elif RadioButton_isChecked(self.rbCtrlOff):
            TheSys.beg.write_single_module_info_control_off(self.selectedModuleID)
        elif RadioButton_isChecked(self.rbCtrlAllOn):
            TheSys.beg.write_module_info_control_on()
        elif RadioButton_isChecked(self.rbCtrlAllOff):
            TheSys.beg.write_module_info_control_off()

    def on_rbCtrlWalkIn(self):
        logger.debug(f"{RadioButton_isChecked(self.rbCtrlWalkInEnable)}, {RadioButton_isChecked(self.rbCtrlWalkInDisable)}")
        if RadioButton_isChecked(self.rbCtrlWalkInEnable):
            TheSys.beg.write_single_module_info_work_in_enable(self.selectedModuleID)
        elif RadioButton_isChecked(self.rbCtrlWalkInDisable):
            TheSys.beg.write_single_module_info_work_in_disable(self.selectedModuleID)

    def on_cbbModuleAddress(self):
        self.selectedModuleID = ComboBox_CurrentIndex(self.cbbModuleAddress)
        logger.debug(f"{self.selectedModuleID}")

    def on_cbStartQuery(self):
        logger.debug(f"{CheckBox_IsChecked(self.cbStartQuery)}")
        if CheckBox_IsChecked(self.cbStartQuery):
            TheSys.beg.is_activated = True
        else:
            TheSys.beg.is_activated = False

    def Task1ms(self):
        TheSys.Response_Infy()

    def Task500ms(self):
        self.update_ui()

    def update_ui(self):
        try:
            self.update_ui_count += 1
            LineEdit_SetTextFromFloat(self.leAcVin_A, TheSys.beg.dict_param[self.selectedModuleID].ac_a_phase_voltage)
            LineEdit_SetTextFromFloat(self.leAcVin_B, TheSys.beg.dict_param[self.selectedModuleID].ac_b_phase_voltage)
            LineEdit_SetTextFromFloat(self.leAcVin_C, TheSys.beg.dict_param[self.selectedModuleID].ac_c_phase_voltage)
            LineEdit_SetTextFromFloat(self.leDcVo,
                                      TheSys.beg.dict_param[self.selectedModuleID].power_module_dc_side_voltage)
            LineEdit_SetTextFromFloat(self.leDcIo,
                                      TheSys.beg.dict_param[self.selectedModuleID].power_module_dc_side_current)
            LineEdit_SetTextFromFloat(self.leTemp,
                                      TheSys.beg.dict_param[self.selectedModuleID].power_module_temperature)
            RadioButton_SetChecked(self.rbStsActive, TheSys.beg.is_activated)
            RadioButton_SetChecked(self.rbStsInactive, not TheSys.beg.is_activated)
            RadioButton_SetChecked(self.rbStsOn,
                                   not TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_pfc_side_off)
            RadioButton_SetChecked(self.rbStsRectify,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.rectifier_mode)
            RadioButton_SetChecked(self.rbStsInverter,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.inverter_mode)
            RadioButton_SetChecked(self.rbStsPowerLimit,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_power_limit_status)
            RadioButton_SetChecked(self.rbStsWalkIn,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_walk_in_enable)
            RadioButton_SetChecked(self.rbAlmNormal,
                                   not TheSys.beg.dict_param[self.selectedModuleID].alarm)
            RadioButton_SetChecked(self.rbAlmAlarm,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm)
            RadioButton_SetChecked(self.rbAlmCommErr,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_communication_interrupt_alarm)
            RadioButton_SetChecked(self.rbAlmOverVin,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.input_over_voltage_protection)
            RadioButton_SetChecked(self.rbAlmLowVin,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.input_low_voltage_alarm)
            RadioButton_SetChecked(self.rbAlmVinUnbalance,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.three_phase_input_unbalance_alarm)
            RadioButton_SetChecked(self.rbAlmAcFail,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_fault_alarm)
            RadioButton_SetChecked(self.rbAlmOverVo,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.output_over_voltage_alarm)
            RadioButton_SetChecked(self.rbAlmProtect,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_protection_alarm)
            RadioButton_SetChecked(self.rbAlmOverTemp,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.over_temperature_alarm)
            RadioButton_SetChecked(self.rbAlmFan,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.fan_fault_alarm)
            RadioButton_SetChecked(self.rbAlmLoadSharing,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_load_sharing_alarm)
            RadioButton_SetChecked(self.rbAlmLossPhase,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.three_phase_input_phase_lost_alarm)
            RadioButton_SetChecked(self.rbAlmVoShort,
                                   TheSys.beg.dict_param[self.selectedModuleID].alarm_status.mdl_output_short_current)
            text = "{0:08x}".format(TheSys.beg.dict_param[self.selectedModuleID].alarm_code)
            LineEdit_SetText(self.leAlarmCode, text)
            LineEdit_SetTextFromInt(self.leRxCount, TheSys.beg.dict_param[self.selectedModuleID].rx_count)
            LineEdit_SetTextFromInt(self.leAliveCount, self.update_ui_count)
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
