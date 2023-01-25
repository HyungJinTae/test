
HMI_DATA_LENGTH = 8
HMI_DATA_UINT32_TO_FLOAT_MULT = 0.001
HMI_TIMEOUT_HEARTBEAT_MS = 10000

HMI_ACTIVATED = 1
HMI_DEACTIVATED = 0

HMI_TRUE = 1
HMI_FALSE = 0

HMI_ID_HMI_CONFIGURATIONS = 0x15EC1001
HMI_ID_HMI_STATUS = 0x15EC1002
HMI_ID_HMI_TIMESTAMP = 0x15EC1003
HMI_ID_HMI_DCDC_TARGET_VOLT_CURR = 0x15EC1004
HMI_ID_HMI_DCDC_STATUS = 0x15ECF001

HMI_ID_SCU_STATUS1 = 0x15EC1101
HMI_ID_SCU_DCDC_PRESENT_VOLT_CURR = 0x15EC1102
HMI_ID_SCU_EV_STATUS = 0x15EC1103
HMI_ID_SCU_BAT_STATUS = 0x15EC1104
HMI_ID_SCU_ERROR_CODE = 0x15EC1105
HMI_ID_SCU_CHG_PARAMETERS1 = 0x15EC1106
HMI_ID_SCU_CHG_PARAMETERS2 = 0x15EC1107


HMI_ID_SCU_DCDC1_STATUS1 = 0x15B11101
HMI_ID_SCU_DCDC1_STATUS2 = 0x15B11102
HMI_ID_SCU_DCDC1_INPUT_VOLTAGE = 0x15B11103
HMI_ID_SCU_DCDC2_STATUS1 = 0x15B21101
HMI_ID_SCU_DCDC2_STATUS2 = 0x15B21102
HMI_ID_SCU_DCDC2_INPUT_VOLTAGE = 0x15B21103
HMI_ID_SCU_DCDC3_STATUS1 = 0x15B31101
HMI_ID_SCU_DCDC3_STATUS2 = 0x15B31102
HMI_ID_SCU_DCDC3_INPUT_VOLTAGE = 0x15B31103
HMI_ID_SCU_DCDC4_STATUS1 = 0x15B41101
HMI_ID_SCU_DCDC4_STATUS2 = 0x15B41102
HMI_ID_SCU_DCDC4_INPUT_VOLTAGE = 0x15B41103

HMI_CHG_MODE_NONE = 0
HMI_CHG_MODE_CHARGING_TIME = (HMI_CHG_MODE_NONE + 1)
HMI_CHG_MODE_CHARGING_AMOUNT = (HMI_CHG_MODE_CHARGING_TIME + 1)

HMI_CHG_CTRL_NONE = 0
HMI_CHG_CTRL_START_CHG = (HMI_CHG_CTRL_NONE + 1)
HMI_CHG_CTRL_STOP_CHG = 15

HMI_DCDC_MON_STATUS1 = 0
HMI_DCDC_MON_DCDC_PRESENT = (HMI_DCDC_MON_STATUS1 + 1)
HMI_DCDC_MON_DCDC1_STATUS1 = (HMI_DCDC_MON_DCDC_PRESENT + 1)
HMI_DCDC_MON_DCDC1_STATUS2 = (HMI_DCDC_MON_DCDC1_STATUS1 + 1)
HMI_DCDC_MON_DCDC1_OUTPUT = (HMI_DCDC_MON_DCDC1_STATUS2 + 1)
HMI_DCDC_MON_DCDC2_STATUS1 = (HMI_DCDC_MON_DCDC1_OUTPUT + 1)
HMI_DCDC_MON_DCDC2_STATUS2 = (HMI_DCDC_MON_DCDC2_STATUS1 + 1)
HMI_DCDC_MON_DCDC2_OUTPUT = (HMI_DCDC_MON_DCDC2_STATUS2 + 1)
HMI_DCDC_MON_DCDC3_STATUS1 = (HMI_DCDC_MON_DCDC2_OUTPUT + 1)  # TEST_Code
HMI_DCDC_MON_DCDC3_STATUS2 = (HMI_DCDC_MON_DCDC3_STATUS1 + 1)  # TEST_Code
HMI_DCDC_MON_DCDC3_OUTPUT = (HMI_DCDC_MON_DCDC3_STATUS2 + 1)  # TEST_Code
HMI_DCDC_MON_DCDC4_STATUS1 = (HMI_DCDC_MON_DCDC3_OUTPUT + 1)  # TEST_Code
HMI_DCDC_MON_DCDC4_STATUS2 = (HMI_DCDC_MON_DCDC4_STATUS1 + 1)  # TEST_Code
HMI_DCDC_MON_DCDC4_OUTPUT = (HMI_DCDC_MON_DCDC4_STATUS2 + 1)  # TEST_Code
HMI_DCDC_MON_END = (HMI_DCDC_MON_DCDC4_OUTPUT + 1)  # TEST_Code

HMI_MON_STATUS1 = 0
HMI_MON_EV_STATUS = (HMI_MON_STATUS1 + 1)
HMI_MON_BAT_STATUS = (HMI_MON_EV_STATUS + 1)
HMI_MON_ERROR_CODE = (HMI_MON_BAT_STATUS + 1)
HMI_MON_CHG_PARAM1 = (HMI_MON_ERROR_CODE + 1)
HMI_MON_CHG_PARAM2 = (HMI_MON_CHG_PARAM1 + 1)
HMI_MON_END = (HMI_MON_CHG_PARAM2 + 1)

HMI_BIT_MASK_1 = 0x01
HMI_BIT_MASK_2 = 0x03
HMI_BIT_MASK_3 = 0x07
HMI_BIT_MASK_4 = 0x0F
HMI_BIT_MASK_5 = 0x1F
HMI_BIT_MASK_6 = 0x3F
HMI_BIT_MASK_7 = 0x7F
HMI_BIT_MASK_8 = 0xFF


def HMI_DataToValue(data, bit, mask=HMI_BIT_MASK_8):
    return (data >> bit) & mask


def HMI_ValueToData(value, bit, mask=HMI_BIT_MASK_8):
    return (value & mask) << bit


def HMI_IntFromByteArray(byte_array, multiple=1, byteorder='little', signed=True):
    i_res = int.from_bytes(byte_array, byteorder=byteorder, signed=signed)
    return int(i_res * multiple)


def HMI_FloatFromByteArray(byte_array, multiple=0.1, byteorder='little', signed=True):
    i_res = HMI_IntFromByteArray(byte_array, byteorder=byteorder, signed=signed)
    return float(i_res) * multiple


def HMI_Copy(data_from, data_to, size):
    for idx in range(size):
        data_to[idx] = data_from[idx]


def HMI_IntToDataArray(iData, multiple=float(1), byte_length=2, byteorder='little', signed=True):
    iData_new = int(iData * multiple)
    return list(iData_new.to_bytes(byte_length, byteorder=byteorder, signed=signed))


def HMI_FloatToDataArray(fData, multiple=float(10), byte_length=2, byteorder='little', signed=True):
    iData = int(fData * multiple)
    return HMI_IntToDataArray(iData, byte_length, byteorder=byteorder, signed=signed)


class HMI_HmiConfig:
    def __init__(self):
        self.hmiRunMode = 0
        self.hmiChargingMode = 0
        self.hmiChargingTime_min = 0
        self.hmiChargingAmount_kWh = 0

    def Parsing(self, data_array, byte_array):
        self.hmiRunMode = data_array[0]
        self.hmiChargingMode = data_array[1]
        self.hmiChargingTime_min = data_array[2]
        self.hmiChargingAmount_kWh = data_array[3]


class HMI_HmiStatus:
    def __init__(self):
        self.hmiHeartbeat = 0
        self.hmiChargingControl = 0
        self.hmiBatteryCharging = 0

    def Parsing(self, data_array, byte_array):
        self.hmiHeartbeat = data_array[0]
        self.hmiChargingControl = data_array[1]
        self.hmiBatteryCharging = data_array[2]


class HMI_HmiTimestamp:
    def __init__(self):
        self.hmiTimestamp_EVSE = 0

    def Parsing(self, data_array, byte_array):
        self.hmiTimestamp_EVSE = HMI_IntFromByteArray(byte_array, multiple=1)


class HMI_HmiDCtg:
    def __init__(self):
        self.f_dcdcTargetVoltage = float(0)
        self.f_dcdcTargetCurrent = float(0)

    def Parsing(self, data_array, byte_array):
        self.f_dcdcTargetVoltage = HMI_FloatFromByteArray(byte_array[0:4], multiple=0.001)
        self.f_dcdcTargetCurrent = HMI_FloatFromByteArray(byte_array[4:8], multiple=0.001)


class HMI_HmiDCstatus:
    def __init__(self):
        self.dcdcControlOn = 0
        self.dcdcWalkInEnable = 0
        self.dcdcLedBlink = 0

    def Parsing(self, data_array, byte_array):
        self.dcdcControlOn = data_array[0]
        self.dcdcWalkInEnable = data_array[1]
        self.dcdcLedBlink = data_array[2]


class HMI_ScuStatus1:
    def __init__(self):
        self.scuHeartbeat = 0
        self.scuStatus = 0
        self.scuGroupNo_DCDC = 0
        self.scuModuleCount_InGroup_DCDC = 0
        self.scuError = 0
        self.scuRunMode = 0
        self.scuVersionMajor = 0    #: 4
        self.scuVersionMinor = 0    #: 4
        self.scuSECCactivated = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.scuHeartbeat & 0xFF
        data[1] = self.scuStatus & 0xFF
        data[2] = self.scuGroupNo_DCDC & 0xFF
        data[3] = self.scuModuleCount_InGroup_DCDC & 0xFF
        data[4] = self.scuError & 0xFF
        data[5] = self.scuRunMode & 0xFF
        data[6] = (self.scuVersionMajor & 0x0F)
        data[6] += ((self.scuVersionMinor & 0x0F) << 4)
        data[7] = self.scuSECCactivated & 0xFF
        return bytearray(data)


class HMI_ScuDCoutput:
    def __init__(self):
        self.dcdcPresentVoltage = 0     # mV
        self.dcdcPresentCurrent = 0     # mV

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.dcdcPresentVoltage, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.dcdcPresentCurrent, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[4:], len(data_array))
        return bytearray(data)


class HMI_ScuEvStatus:
    def __init__(self):
        self.evSOC = 0
        self.evPresentVoltage = 0
        self.evPresentCurrent = 0
        self.dcdcTemperature_0 = 0
        self.dcdcTemperature_1 = 0

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.evSOC, byte_length=2, multiple=10)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.evPresentVoltage, byte_length=2, multiple=10)
        HMI_Copy(data_array, data[2:], len(data_array))
        data_array = HMI_IntToDataArray(self.evPresentCurrent, byte_length=2, multiple=10)
        HMI_Copy(data_array, data[4:], len(data_array))
        data[6] = self.dcdcTemperature_0 & 0xFF
        data[7] = self.dcdcTemperature_1 & 0xFF
        return bytearray(data)


class HMI_ScuBatStatus:
    def __init__(self):
        self.batSOC = 0
        self.batPresentVoltage = 0
        self.batPresentCurrent = 0

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.batSOC, byte_length=2, multiple=10)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.batPresentVoltage, byte_length=2, multiple=10)
        HMI_Copy(data_array, data[2:], len(data_array))
        data_array = HMI_IntToDataArray(self.batPresentCurrent, byte_length=2, multiple=10)
        HMI_Copy(data_array, data[4:], len(data_array))
        return bytearray(data)


class HMI_ScuErrorCode:
    def __init__(self):
        self.scuECode_EV = 0
        self.scuECode_SECC = 0
        self.scuECode_DCDC = 0
        self.scuECode_SBMS = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.scuECode_EV & 0xFF
        data[1] = self.scuECode_SECC & 0xFF
        data[2] = self.scuECode_DCDC & 0xFF
        data[3] = self.scuECode_SBMS & 0xFF
        return bytearray(data)


class HMI_ScuCHGparam1:
    def __init__(self):
        self.evElapsedTime = 0      # sec
        self.evRemainingTime = 0    # sec
        self.evChargingAmount = 0   # wh
        self.batChargingAmount = 0  # wh

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.evElapsedTime, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.evRemainingTime, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[2:], len(data_array))
        data_array = HMI_IntToDataArray(self.evChargingAmount, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[4:], len(data_array))
        data_array = HMI_IntToDataArray(self.batChargingAmount, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[6:], len(data_array))
        return bytearray(data)


class HMI_ScuCHGparam2:
    def __init__(self):
        self.batElapsedTime = 0     # sec
        self.batRemainingTime = 0   # sec

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.batElapsedTime, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.batRemainingTime, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[4:], len(data_array))
        return bytearray(data)


class HMI_ScuDCstatus1:
    def __init__(self):
        self.dcdcModuleNo = 0
        self.dcdcAlarm = 0
        self.dcdcAlarmCode = [0] * 3
        self.dcdcStatus_DCsideOff = 0
        self.dcdcStatus_walkinEnable = 0
        self.dcdcStatus_PFCsideOFF = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.dcdcModuleNo & 0xFF
        data[1] = self.dcdcAlarm & 0xFF
        HMI_Copy(self.dcdcAlarmCode, data[2:], len(self.dcdcAlarmCode))
        data[5] = self.dcdcStatus_DCsideOff & 0xFF
        data[6] = self.dcdcStatus_walkinEnable & 0xFF
        data[7] = self.dcdcStatus_PFCsideOFF & 0xFF
        return bytearray(data)


class HMI_ScuDCstatus2:
    def __init__(self):
        self.dcdcPresentTemperature = 0
        self.dcdcInputVoltage = 0

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.dcdcPresentTemperature, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.dcdcInputVoltage, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[4:], len(data_array))
        return bytearray(data)


class HMI_ScuDCmdlOut:
    def __init__(self):
        self.dcdcOutputVoltage = 0
        self.dcdcOutputCurrent = 0

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.dcdcOutputVoltage, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.dcdcOutputCurrent, byte_length=4, multiple=1)
        HMI_Copy(data_array, data[4:], len(data_array))
        return bytearray(data)


# TEST_Code
class HMI_AirCloorConfig:
    def __init__(self):
        self.AcRunMode = 0
        self.AcSetTemp = 0
        self.AcSetHumidity = 0
        self.AcSetTempDiff = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.AcRunMode & 0xFF
        data_array = HMI_IntToDataArray(self.AcSetTemp, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[1:], len(data_array))
        data[3] = self.AcSetHumidity & 0xFF
        data[4] = self.AcSetTempDiff & 0xFF
        return bytearray(data)


# TEST_Code
class HMI_AirCloorStatus:
    def __init__(self):
        self.AcPresentTempIn = 0
        self.AcPresentTempOut = 0
        self.AcPresentHumidity = 0
        self.AcError = 0

    def ByteArray(self):
        data = [0] * 8
        data_array = HMI_IntToDataArray(self.AcPresentTempIn, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[0:], len(data_array))
        data_array = HMI_IntToDataArray(self.AcPresentTempOut, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[2:], len(data_array))
        data[4] = self.AcPresentHumidity & 0xFF
        data_array = HMI_IntToDataArray(self.AcError, byte_length=2, multiple=1)
        HMI_Copy(data_array, data[5:], len(data_array))
        return bytearray(data)


class HMI_Param:
    def __init__(self):
        self.is_activated = 0
        self.mon_send_count = 0  # monitoring data send count
        self.prev_heart_beat = 0
        self.hmi_conf = HMI_HmiConfig()
        self.hmi_status = HMI_HmiStatus()
        self.hmi_timestamp = HMI_HmiTimestamp()
        self.hmi_dc_tg = HMI_HmiDCtg()
        self.hmi_dc_status = HMI_HmiDCstatus()
        self.scu_status = HMI_ScuStatus1()
        self.scu_group_dc_out = HMI_ScuDCoutput()
        self.scu_dc1_status1 = HMI_ScuDCstatus1()
        self.scu_dc1_status2 = HMI_ScuDCstatus2()
        self.scu_dc1_output = HMI_ScuDCmdlOut()
        self.scu_dc2_status1 = HMI_ScuDCstatus1()
        self.scu_dc2_status2 = HMI_ScuDCstatus2()
        self.scu_dc2_output = HMI_ScuDCmdlOut()
        self.ev_status = HMI_ScuEvStatus()
        self.bat_status = HMI_ScuBatStatus()
        self.scu_ecode = HMI_ScuErrorCode()
        self.chg_param1 = HMI_ScuCHGparam1()
        self.chg_param2 = HMI_ScuCHGparam2()
        self.aircooler_conf = HMI_AirCloorConfig()  # TEST_Code
        self.aircooler_status = HMI_AirCloorStatus()  # TEST_Code
        self.scu_dc3_status1 = HMI_ScuDCstatus1()  # TEST_Code
        self.scu_dc3_status2 = HMI_ScuDCstatus2()  # TEST_Code
        self.scu_dc3_output = HMI_ScuDCmdlOut()  # TEST_Code
        self.scu_dc4_status1 = HMI_ScuDCstatus1()  # TEST_Code
        self.scu_dc4_status2 = HMI_ScuDCstatus2()  # TEST_Code
        self.scu_dc4_output = HMI_ScuDCmdlOut()  # TEST_Code
