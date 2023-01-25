
from common.Setting import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer


def QTimer_Init(timer: QTimer, msec: int,  func):
    timer.start(msec)
    timer.timeout.connect(func)


def PushButton_ClickedConnect(pb: QPushButton, func):
    pb.clicked.connect(func)


def LineEdit_SetTextFromFloat(le: QLineEdit, fVal):
    le.setText("{0:3.1f}".format(fVal))


def LineEdit_SetTextFromInt(le: QLineEdit, iVal):
    le.setText(f"{iVal}")


def LineEdit_SetText(le: QLineEdit, text):
    le.setText(f"{text}")


def LineEdit_GetTextToFloat(le: QLineEdit):
    text = le.text()
    f_res = float(0)
    try:
        f_res = float(text)
    except Exception as e:
        logger.warning(f"e->{e}")
    return f_res


def LineEdit_GetTextToInt(le: QLineEdit):
    text = le.text()
    res = int(0)
    try:
        res = int(text)
    except Exception as e:
        logger.warning(f"e->{e}")
    return res


def RadioButton_ClickedConnect(rb: QRadioButton, func):
    rb.clicked.connect(func)


def RadioButton_SetChecked(rb: QRadioButton, checked: bool):
    rb.setChecked(checked)


def RadioButton_isChecked(rb: QRadioButton):
    return rb.isChecked()


def ComboBox_AddItem(cbb: QComboBox, text: str):
    cbb.addItem(text)


def ComboBox_CurrentIndex(cbb: QComboBox):
    return cbb.currentIndex()


def ComboBox_ClearComboBoxItem(cbb: QComboBox):
    cbb.clear()


def ComboBox_IndexChangedConnect(cbb: QComboBox, func):
    cbb.currentIndexChanged.connect(func)


def ComboBox_DeleteComboBoxItem(cbb: QComboBox):
    idx = cbb.currentIndex()
    cbb.removeItem(idx)


def CheckBox_StateChangedConnect(cb: QCheckBox, func):
    cb.stateChanged.connect(func)


def CheckBox_IsChecked(cb: QCheckBox):
    return cb.isChecked()


def CheckBox_SetChecked(cb: QCheckBox, checked: bool):
    cb.setChecked(checked)


def TabWidget_CurrentIndex(tab: QTabWidget):
    return tab.currentIndex()


def TabWidget_SetCurrentIndex(tab: QTabWidget, tabno):
    tab.setCurrentIndex(tabno)
