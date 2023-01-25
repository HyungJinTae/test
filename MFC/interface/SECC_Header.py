# SECC (Gridwiz PEPPERMINT) communication interface Header
# written based on EVSE C Code

from common.App_Header import *

SECC_CAN_CHANNEL = 1
SECC_CAN_DATA_LENGTH = 8
SECC_MULT_FLOAT_TO_SHORT = 10
SECC_MULT_SHORT_TO_FLOAT = 0.1
SECC_UINT32_TO_UINT16 = 0.1
SECC_UINT16_TO_UINT32 = 10

SECC_ACTIVATED_CHECK_COUNT_MAX = 2

SECC_MAX_POWER_LIMIT = APP_MAX_POWER_LIMIT
SECC_MIN_CURRENT_LIMIT = APP_MIN_CURRENT_LIMIT
SECC_MAX_CURRENT_LIMIT = APP_MAX_CURRENT_LIMIT
SECC_MIN_VOLTAGE_LIMIT = 0.0
SECC_MAX_VOLTAGE_LIMIT = APP_MAX_VOLTAGE_LIMIT
SECC_PEAK_CURRENT_LIMIT = APP_MAX_CURRENT_LIMIT

SECC_ID_EVSE_CONFIGURATIONS = 0x15ECC001
SECC_ID_EVSE_STATUS = 0x15ECC002
SECC_ID_EVSE_CHARGE_PARAMETERS1 = 0x15ECC003
SECC_ID_EVSE_CHARGE_PARAMETERS2 = 0x15ECC004
SECC_ID_EVSE_PRESENT_VOLT_CURR = 0x15ECC005
SECC_ID_EVSE_DIN_ID_1 = 0x15ECC006
SECC_ID_EVSE_DIN_ID_2 = 0x15ECC007
SECC_ID_EVSE_DIN_ID_3 = 0x15ECC008
SECC_ID_EVSE_DIN_ID_4 = 0x15ECC009
SECC_ID_EVSE_ISO_ID_1 = 0x15ECC00A
SECC_ID_EVSE_ISO_ID_2 = 0x15ECC00B
SECC_ID_EVSE_ISO_ID_3 = 0x15ECC00C
SECC_ID_EVSE_ISO_ID_4 = 0x15ECC00D
SECC_ID_EVSE_ISO_ID_5 = 0x15ECC00E
SECC_ID_EVSE_TIMESTAMP = 0x15ECC00F
SECC_ID_EVSE_SECC_REBOOT = 0x15ECC0FF

SECC_ID_SECC_STATUS1 = 0x15ECC101
SECC_ID_SECC_STATUS2 = 0x15ECC102
SECC_ID_SECC_EV_SERVICE_SELECTION = 0x15ECC103
SECC_ID_SECC_SESSION_ID = 0x15ECC104
SECC_ID_SECC_EVCC_INFO = 0x15ECC105
SECC_ID_SECC_EV_CHG_PARAM1 = 0x15ECC106
SECC_ID_SECC_EV_CHG_PARAM2 = 0x15ECC107
SECC_ID_SECC_EV_SOC_RELATED_PARAM = 0x15ECC108
SECC_ID_SECC_EV_TGT_VOLTCURR = 0x15ECC109
SECC_ID_SECC_TIMESTAMP = 0x15ECC10A
SECC_ID_SECC_STATUS3_PNC = 0x15ECC10B
SECC_ID_SECC_EMERGENCY_NOTI = 0x15ECC1FF
SECC_ID_EVSE_SA_AGENT_CONN_CONF = 0x15ECD001
SECC_ID_EVSE_SECC_PNC_CONF = 0x15ECD002
SECC_ID_EVSE_SA_AGENT_COMM_TIMEOUT = 0x15ECD003
SECC_ID_SECC_SA_COMM_STATUS = 0x15ECD101
SECC_ID_SECC_IP_STATUS = 0x15ECD102


SECC_REBOOT_R = 0x52
SECC_REBOOT_E = 0x45
SECC_REBOOT_B = 0x42
SECC_REBOOT_O = 0x4F
SECC_REBOOT_T = 0x54

SECC_FALSE = 0
SECC_TRUE = 1

SECC_OFF = 0
SECC_ON = 1

SECC_DISABLE = 0
SECC_ENABLE = 1

SECC_DEFAULT = 0
SECC_CUSTOM = 1
SECC_REQ_RE_NEGO = 1

SECC_NONE = SECC_DEFAULT

SECC_NOT_SUPPORTED = 0
SECC_SUPPORTED = 1

SECC_PAYED_SERVICE = 0
SECC_FREE_SERVICE = 1

SECC_NOT_ACTIVE = 0
SECC_ACTIVE = 1

SECC_ONGOING = 0
SECC_FINISHED = 1

SECC_RENEGO_NONE = 0
SECC_RENEGO_REQ = 1

SECC_LINK_DOWN = 0
SECC_LINK_UP = 1

# ##### enumerate #########

SECC_ENVIRON_CONF_DEFAULT = 0     # Default, ISO/DIN selection based on EVCC's priority
SECC_ENVIRON_CONF_FORCE_NON_TLS_EIM = 14
SECC_ENVIRON_CONF_FORCE_DIN = (SECC_ENVIRON_CONF_FORCE_NON_TLS_EIM + 1)
SECC_ENVIRON_CONF_END = (SECC_ENVIRON_CONF_FORCE_DIN + 1)


SECC_SCHED_MANAGE_DEFAULT = 0
SECC_SCHED_MANAGE_OCPP = (SECC_SCHED_MANAGE_DEFAULT + 1)
SECC_SCHED_MANAGE_INTEROP = (SECC_SCHED_MANAGE_OCPP + 1)
SECC_SCHED_MANAGE_END = (SECC_SCHED_MANAGE_INTEROP + 1)


SECC_CHG_CONTROL_NONE = 0
SECC_CHG_CONTROL_INIT_PPMT = (SECC_CHG_CONTROL_NONE + 1)
SECC_CHG_CONTROL_START_CHARGING = (SECC_CHG_CONTROL_INIT_PPMT + 1)
SECC_CHG_CONTROL_NORMAL_STOP = (SECC_CHG_CONTROL_START_CHARGING + 1)
SECC_CHG_CONTROL_EMERGENCY_STOP = (SECC_CHG_CONTROL_NORMAL_STOP + 1)
SECC_CHG_CONTROL_END = (SECC_CHG_CONTROL_EMERGENCY_STOP + 1)


SECC_ISOL_STATUS_INVALID = 0
SECC_ISOL_STATUS_VALID = (SECC_ISOL_STATUS_INVALID + 1)
SECC_ISOL_STATUS_WARNING = (SECC_ISOL_STATUS_VALID + 1)
SECC_ISOL_STATUS_FAULT = (SECC_ISOL_STATUS_WARNING + 1)         # E-Stop due to isolation fault
SECC_ISOL_STATUS_NOIMD_NONE = (SECC_ISOL_STATUS_FAULT + 1)      # ISO: No IMD, DIN: None
SECC_ISOL_STATUS_END = (SECC_ISOL_STATUS_NOIMD_NONE + 1)


SECC_LEGA_ST_IdleWait = 0
SECC_LEGA_ST_Idle = (SECC_LEGA_ST_IdleWait + 1)
SECC_LEGA_ST_Ready = (SECC_LEGA_ST_Idle + 1)
SECC_LEGA_ST_LowLevelComm = (SECC_LEGA_ST_Ready + 1)
SECC_LEGA_ST_HighLevelComm = (SECC_LEGA_ST_LowLevelComm + 1)
SECC_LEGA_ST_AuthorizationEIM = (SECC_LEGA_ST_HighLevelComm + 1)
SECC_LEGA_ST_ChargeParameterDiscovery = (SECC_LEGA_ST_AuthorizationEIM + 1)
SECC_LEGA_ST_CableCheck = (SECC_LEGA_ST_ChargeParameterDiscovery + 1)
SECC_LEGA_ST_PreCharge = (SECC_LEGA_ST_CableCheck + 1)
SECC_LEGA_ST_Charging = (SECC_LEGA_ST_PreCharge + 1)
SECC_LEGA_ST_Renegotiation = (SECC_LEGA_ST_Charging + 1)
SECC_LEGA_ST_EV_InitStopCharging = (SECC_LEGA_ST_Renegotiation + 1)
SECC_LEGA_ST_EVSE_InitStopCharging = (SECC_LEGA_ST_EV_InitStopCharging + 1)
SECC_LEGA_ST_PAUSE = (SECC_LEGA_ST_EVSE_InitStopCharging + 1)
SECC_LEGA_ST_TERMINATE = (SECC_LEGA_ST_PAUSE + 1)
SECC_LEGA_ST_CertificateInstallationPnC = (SECC_LEGA_ST_TERMINATE + 1)
SECC_LEGA_ST_CertificateUpdatePnC = (SECC_LEGA_ST_CertificateInstallationPnC + 1)
SECC_LEGA_ST_ERROR = (SECC_LEGA_ST_CertificateUpdatePnC + 1)
SECC_LEGA_ST_AuthorizationPnC = (SECC_LEGA_ST_ERROR + 1)
SECC_LEGA_ST_MeteringReceiptPnc = (SECC_LEGA_ST_AuthorizationPnC + 1)


SECC_ERR_EV_NO_ERROR = 0
SECC_ERR_EV_FAILED_RESSTemperatureInhibit = (SECC_ERR_EV_NO_ERROR + 1)
SECC_ERR_EV_FAILED_EVShiftPosition = (SECC_ERR_EV_FAILED_RESSTemperatureInhibit + 1)
SECC_ERR_EV_FAILED_ChargerConnectorLockFault = (SECC_ERR_EV_FAILED_EVShiftPosition + 1)
SECC_ERR_EV_FAILED_EVRESSMalfunction = (SECC_ERR_EV_FAILED_ChargerConnectorLockFault + 1)
SECC_ERR_EV_FAILED_ChargingCurrentDifferential = (SECC_ERR_EV_FAILED_EVRESSMalfunction + 1)
SECC_ERR_EV_FAILED_ChargingVoltageOutOfRange = (SECC_ERR_EV_FAILED_ChargingCurrentDifferential + 1)
SECC_ERR_EV_FAILED_ChargingSystemIncompatibility = 10
SECC_ERR_EV_NoData = (SECC_ERR_EV_FAILED_ChargingSystemIncompatibility + 1)


SECC_ERR_SECC_NO_ERROR = 0
SECC_ERR_SECC_FAILED = (SECC_ERR_SECC_NO_ERROR + 1)
SECC_ERR_SECC_FAILED_SequenceError = (SECC_ERR_SECC_FAILED + 1)
SECC_ERR_SECC_FAILED_ServiceIDInvalid = (SECC_ERR_SECC_FAILED_SequenceError + 1)
SECC_ERR_SECC_FAILED_UnknownSession = (SECC_ERR_SECC_FAILED_ServiceIDInvalid + 1)
SECC_ERR_SECC_FAILED_ServiceSelectionInvalid = (SECC_ERR_SECC_FAILED_UnknownSession + 1)
SECC_ERR_SECC_FAILED_PaymentSelectionInvalid = (SECC_ERR_SECC_FAILED_ServiceSelectionInvalid + 1)
SECC_ERR_SECC_FAILED_CertificateExpired = (SECC_ERR_SECC_FAILED_PaymentSelectionInvalid + 1)
SECC_ERR_SECC_FAILED_SignatureError = (SECC_ERR_SECC_FAILED_CertificateExpired + 1)
SECC_ERR_SECC_FAILED_NoCertificateAvailable = (SECC_ERR_SECC_FAILED_SignatureError + 1)
SECC_ERR_SECC_FAILED_CertChainError = (SECC_ERR_SECC_FAILED_NoCertificateAvailable + 1)
SECC_ERR_SECC_FAILED_ChallengeInvalid = (SECC_ERR_SECC_FAILED_CertChainError + 1)
SECC_ERR_SECC_FAILED_ContractCanceled = (SECC_ERR_SECC_FAILED_ChallengeInvalid + 1)
SECC_ERR_SECC_FAILED_WrongChargeParameter = (SECC_ERR_SECC_FAILED_ContractCanceled + 1)
SECC_ERR_SECC_FAILED_PowerDeliveryNotApplied = (SECC_ERR_SECC_FAILED_WrongChargeParameter + 1)
SECC_ERR_SECC_FAILED_TariffSelectionInvalid = (SECC_ERR_SECC_FAILED_PowerDeliveryNotApplied + 1)
SECC_ERR_SECC_FAILED_ChargingProfileInvalid = (SECC_ERR_SECC_FAILED_TariffSelectionInvalid + 1)
SECC_ERR_SECC_FAILED_MeteringSignatureNotValid = (SECC_ERR_SECC_FAILED_ChargingProfileInvalid + 1)
SECC_ERR_SECC_FAILED_NoChargeServiceSelected = (SECC_ERR_SECC_FAILED_MeteringSignatureNotValid + 1)
SECC_ERR_SECC_FAILED_WrongEnergyTransferMode = (SECC_ERR_SECC_FAILED_NoChargeServiceSelected + 1)
SECC_ERR_SECC_FAILED_CertificateRevoked = 22
SECC_ERR_SECC_FAILED_NoNegotiation = (SECC_ERR_SECC_FAILED_CertificateRevoked + 1)
SECC_ERR_SECC_TIMEOUT_CommunicationSetup = 30
SECC_ERR_SECC_TIMEOUT_Sequence = (SECC_ERR_SECC_TIMEOUT_CommunicationSetup + 1)
SECC_ERR_SECC_TIMEOUT_NotificationMaxDelay = (SECC_ERR_SECC_TIMEOUT_Sequence + 1)
SECC_ERR_SECC_TIMEOUT_WeldingDetection = (SECC_ERR_SECC_TIMEOUT_NotificationMaxDelay + 1)
SECC_ERR_SECC_FAULT_WrongCPLevel = 40
SECC_ERR_SECC_FAULT_ProximityError = (SECC_ERR_SECC_FAULT_WrongCPLevel + 1)
SECC_ERR_SECC_FAULT_HLCError = (SECC_ERR_SECC_FAULT_ProximityError + 1)
SECC_ERR_SECC_FAULT_HeartbeatError = (SECC_ERR_SECC_FAULT_HLCError + 1)
SECC_ERR_SECC_FAULT_EVSECANInit = (SECC_ERR_SECC_FAULT_HeartbeatError + 1)
SECC_ERR_SECC_FAULT_HPGPLinkDown = (SECC_ERR_SECC_FAULT_EVSECANInit + 1)
SECC_ERR_SECC_FAULT_TLS_ErrorAlert = (SECC_ERR_SECC_FAULT_HPGPLinkDown + 1)


SECC_PNC_READY_NONE = 0
SECC_PNC_READY_NOT_READY = (SECC_PNC_READY_NONE + 1)
SECC_PNC_READY_READY = (SECC_PNC_READY_NOT_READY + 1)


SECC_ERR_TLS_close_notify = 0
SECC_ERR_TLS_unexpected_message = 10
SECC_ERR_TLS_bad_record_mac = 20
SECC_ERR_TLS_decryption_failed_RESERVED = (SECC_ERR_TLS_bad_record_mac + 1)
SECC_ERR_TLS_record_overflow = (SECC_ERR_TLS_decryption_failed_RESERVED + 1)
SECC_ERR_TLS_decompression_failure = 30
SECC_ERR_TLS_handshake_failure = 40
SECC_ERR_TLS_no_certificate_RESERVED = (SECC_ERR_TLS_handshake_failure + 1)
SECC_ERR_TLS_bad_certificate = (SECC_ERR_TLS_no_certificate_RESERVED + 1)
SECC_ERR_TLS_unsupported_certificate = (SECC_ERR_TLS_bad_certificate + 1)
SECC_ERR_TLS_certificate_revoked = (SECC_ERR_TLS_unsupported_certificate + 1)
SECC_ERR_TLS_certificate_expired = (SECC_ERR_TLS_certificate_revoked + 1)
SECC_ERR_TLS_certificate_unknown = (SECC_ERR_TLS_certificate_expired + 1)
SECC_ERR_TLS_illegal_parameter = (SECC_ERR_TLS_certificate_unknown + 1)
SECC_ERR_TLS_unknown_ca = (SECC_ERR_TLS_illegal_parameter + 1)
SECC_ERR_TLS_access_denied = (SECC_ERR_TLS_unknown_ca + 1)
SECC_ERR_TLS_decode_error = (SECC_ERR_TLS_access_denied + 1)
SECC_ERR_TLS_decrypt_error = (SECC_ERR_TLS_decode_error + 1)
SECC_ERR_TLS_export_restriction_RESERVED = 60
SECC_ERR_TLS_protocol_version = 70
SECC_ERR_TLS_insufficient_security = (SECC_ERR_TLS_protocol_version + 1)
SECC_ERR_TLS_internal_error = 80
SECC_ERR_TLS_user_canceled = 90
SECC_ERR_TLS_no_renegotiation = 100
SECC_ERR_TLS_unsupported_extension = 110


SECC_CHG_PROTOCOL_DIN_SPEC_70121_2014 = 0
SECC_CHG_PROTOCOL_ISO_15118_2_2013 = (SECC_CHG_PROTOCOL_DIN_SPEC_70121_2014 + 1)
SECC_CHG_PROTOCOL_ISO_15118_2_2016 = (SECC_CHG_PROTOCOL_ISO_15118_2_2013 + 1)
SECC_CHG_PROTOCOL_NONE = 0xFF               # default


SECC_PAY_OPTION_CONTRACT = 0
SECC_PAY_OPTION_EXTERNALPAYMENT = (SECC_PAY_OPTION_CONTRACT + 1)
SECC_PAY_OPTION_NONE = 0xFF                 # default


SECC_ENG_TRANSFER_MODE_AC_single_phase_core = 0
SECC_ENG_TRANSFER_MODE_AC_three_phase_core = (SECC_ENG_TRANSFER_MODE_AC_single_phase_core + 1)
SECC_ENG_TRANSFER_MODE_DC_core = (SECC_ENG_TRANSFER_MODE_AC_three_phase_core + 1)
SECC_ENG_TRANSFER_MODE_DC_extended = (SECC_ENG_TRANSFER_MODE_DC_core + 1)
SECC_ENG_TRANSFER_MODE_DC_combo_core = (SECC_ENG_TRANSFER_MODE_DC_extended + 1)
SECC_ENG_TRANSFER_MODE_DC_unique = (SECC_ENG_TRANSFER_MODE_DC_combo_core + 1)
SECC_ENG_TRANSFER_MODE_NONE = 0xFF          # default


SECC_SOC_CHG_NOT_COMPLETE = 0
SECC_SOC_CHG_COMPLETE = (SECC_SOC_CHG_NOT_COMPLETE + 1)
SECC_SOC_CHG_NONE = 3


SECC_ST_IDLE = 0
SECC_ST_INITIALIZED = (SECC_ST_IDLE + 1)
SECC_ST_WAITING_PLUG_IN = (SECC_ST_INITIALIZED + 1)
SECC_ST_WAITING_SLAC = 10
SECC_ST_PROCESSING_SLAC = (SECC_ST_WAITING_SLAC + 1)
SECC_ST_SDP = 20
SECC_ST_ESTABLISHING_TCP_TLS = (SECC_ST_SDP + 1)
SECC_ST_SAP = 30
SECC_ST_SESSION_SETUP = 40
SECC_ST_SESSION_STOP_TERMINATE = (SECC_ST_SESSION_SETUP + 1)
SECC_ST_SESSION_STOP_PAUSE = (SECC_ST_SESSION_STOP_TERMINATE + 1)
SECC_ST_SERVICE_DISCOVERY = 50
SECC_ST_SERVICE_DETIALS = (SECC_ST_SERVICE_DISCOVERY + 1)
SECC_ST_PAYMENT_SERVICE_SELECTION = 60
SECC_ST_CERTIFICATE_INSTALLATION = 70
SECC_ST_CERTIFICATE_UPDATE = (SECC_ST_CERTIFICATE_INSTALLATION + 1)
SECC_ST_PAYMENT_DETAILS = 80
SECC_ST_AUTHORIZATION_EIM = (SECC_ST_PAYMENT_DETAILS + 1)
SECC_ST_AUTHORIZATION_PNC = (SECC_ST_AUTHORIZATION_EIM + 1)
SECC_ST_CHARGE_PARAMETER_DISCOVERY = 90
SECC_ST_CABLE_CHECK = 100
SECC_ST_PRE_CHARGE = (SECC_ST_CABLE_CHECK + 1)
SECC_ST_WELDING_DETECTION = (SECC_ST_PRE_CHARGE + 1)
SECC_ST_POWER_DELIVERY_START = 110
SECC_ST_POWER_DELIVERY_EV_INIT_STOP = (SECC_ST_POWER_DELIVERY_START + 1)
SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP = (SECC_ST_POWER_DELIVERY_EV_INIT_STOP + 1)
SECC_ST_POWER_DELIVERY_RENOGOTIATE = (SECC_ST_POWER_DELIVERY_EVSE_INIT_STOP + 1)
SECC_ST_CURRENT_DEMAND = 120
SECC_ST_METERING_RECEIPT = (SECC_ST_CURRENT_DEMAND + 1)
SECC_ST_TERMINATE = 250
SECC_ST_PAUSE = (SECC_ST_TERMINATE + 1)
SECC_ST_ERROR = (SECC_ST_PAUSE + 1)


SECC_ESTABLISHED_NONE = 0
SECC_ESTABLISHED_NON_TLS = (SECC_ESTABLISHED_NONE + 1)
SECC_ESTABLISHED_PUBLIC_TLS = (SECC_ESTABLISHED_NON_TLS + 1)
SECC_ESTABLISHED_PE_TLS = (SECC_ESTABLISHED_PUBLIC_TLS + 1)


# pkiEnvironmentSelection
SECC_PKI_SEL_NONE = 0
SECC_PKI_SEL_PUBLIC_CPO_CHAIN = (SECC_PKI_SEL_NONE + 1)
SECC_PKI_SEL_PRIVATE_CHAIN = (SECC_PKI_SEL_PUBLIC_CPO_CHAIN + 1)


# certChainValidationOption
SECC_CERT_OPT_NONE = 0
SECC_CERT_OPT_PASSIVE = (SECC_CERT_OPT_NONE + 1)
SECC_CERT_OPT_ACTIVE = (SECC_CERT_OPT_PASSIVE + 1)
SECC_CERT_OPT_FORCED_CSR = (SECC_CERT_OPT_ACTIVE + 1)


# reKeyOption
SECC_KEY_OPT_FALE = 0
SECC_KEY_OPT_TRUE = (SECC_KEY_OPT_FALE + 1)


SECC_SA_INIT_RES_NONE = 0
SECC_SA_INIT_RES_PUBLIC_TLS = (SECC_SA_INIT_RES_NONE + 1)
SECC_SA_INIT_RES_PE_TLS = (SECC_SA_INIT_RES_PUBLIC_TLS + 1)


SECC_SA_DETTAILS_NONE = 0
SECC_SA_DETTAILS_TIMEOUT_HelloResponse = 10
SECC_SA_DETTAILS_TIMEOUT_GetCertStatusResp = (SECC_SA_DETTAILS_TIMEOUT_HelloResponse + 1)
SECC_SA_DETTAILS_TIMEOUT_SignCertResp = (SECC_SA_DETTAILS_TIMEOUT_GetCertStatusResp + 1)
SECC_SA_DETTAILS_TIMEOUT_InstallPerfTimer = (SECC_SA_DETTAILS_TIMEOUT_SignCertResp + 1)
SECC_SA_DETTAILS_TIMEOUT_UpdatePerfTimer = (SECC_SA_DETTAILS_TIMEOUT_InstallPerfTimer + 1)
SECC_SA_DETTAILS_TIMEOUT_AuthResp = (SECC_SA_DETTAILS_TIMEOUT_UpdatePerfTimer + 1)
SECC_SA_DETTAILS_FAULT_saAgentComm = 20
SECC_SA_DETTAILS_FAULT_parseJSON = (SECC_SA_DETTAILS_FAULT_saAgentComm + 1)
SECC_SA_DETTAILS_FAULT_createCSR = (SECC_SA_DETTAILS_FAULT_parseJSON + 1)
SECC_SA_DETTAILS_FAULT_recvCertChain = (SECC_SA_DETTAILS_FAULT_createCSR + 1)
SECC_SA_DETTAILS_FAULT_decodeEXI = 40


# #### structure ##########
SECC_BIT_MASK_1 = 0x01
SECC_BIT_MASK_2 = 0x03
SECC_BIT_MASK_3 = 0x07
SECC_BIT_MASK_4 = 0x0F
SECC_BIT_MASK_5 = 0x1F
SECC_BIT_MASK_6 = 0x3F
SECC_BIT_MASK_7 = 0x7F
SECC_BIT_MASK_8 = 0xFF


def SECC_DataToValue(data, bit, mask=SECC_BIT_MASK_8):
    return (data >> bit) & mask


def SECC_ValueToData(value, bit, mask=SECC_BIT_MASK_8):
    return (value & mask) << bit


def SECC_IntFromByteArray(byte_array, multiple=1, byteorder='little', signed=True):
    i_res = int.from_bytes(byte_array, byteorder=byteorder, signed=signed)
    return int(i_res * multiple)


def SECC_FloatFromByteArray(byte_array, multiple=0.1, byteorder='little', signed=True):
    i_res = SECC_IntFromByteArray(byte_array, byteorder=byteorder, signed=signed)
    return float(i_res) * multiple


def SECC_Copy(data_from, data_to, size):
    for idx in range(size):
        data_to[idx] = data_from[idx]


def SECC_IntToDataArray(iData, multiple=float(1), byte_length=2, byteorder='little', signed=True):
    iData_new = int(iData * multiple)
    return list(iData_new.to_bytes(byte_length, byteorder=byteorder, signed=signed))


def SECC_FloatToDataArray(fData, multiple=float(10), byte_length=2, byteorder='little', signed=True):
    iData = int(fData * multiple)
    return SECC_IntToDataArray(iData, byte_length, byteorder=byteorder, signed=signed)


# 200 ms
# typedef struct SECC_EVSE_CONFIGURATIONS
class SECC_EvseConfig:
    def __init__(self):
        self.evseIdConfig_DIN = 0
        self.evseIdConfig_ISO = 0
        self.rsvd00 = 0
        self.environmentConfiguration = 0
        self.evseIdLength_DIN = 0
        self.evseIdLength_ISO = 0
        self.rsvd01 = 0
        self.supportedEnergyTransfer_DCcore = 0
        self.supportedEnergyTransfer_DCextd = 0
        self.supportedEnergyTransfer_DCcc = 0
        self.supportedEnergyTransfer_DCunique = 0
        self.rsvd02 = 0
        self.serviceList_Internet = 0
        self.rsvd03 = 0
        self.serviceList_HPC1 = 0
        self.rsvd04 = 0
        self.freeService_EVCharging = 0
        self.freeService_Internet = 0
        self.freeService_ContractCert = 0
        self.freeService_OtherCustom = 0
        self.rsvd05 = 0
        self.saScheduleManagement = 0
        self.cpMonitoringMode = 0
        self.rsvd06 = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = SECC_ValueToData(self.evseIdConfig_DIN, 0, SECC_BIT_MASK_1)
        data[0] += SECC_ValueToData(self.evseIdConfig_ISO, 1, SECC_BIT_MASK_1)
        data[0] += SECC_ValueToData(self.rsvd00, 2, SECC_BIT_MASK_2)
        data[0] += SECC_ValueToData(self.environmentConfiguration, 4, SECC_BIT_MASK_4)
        data[1] = self.evseIdLength_DIN & 0xFF
        data[2] = self.evseIdLength_ISO & 0xFF
        data[3] = SECC_ValueToData(self.rsvd01, 0, SECC_BIT_MASK_2)
        data[3] += SECC_ValueToData(self.supportedEnergyTransfer_DCcore, 2, SECC_BIT_MASK_1)
        data[3] += SECC_ValueToData(self.supportedEnergyTransfer_DCextd, 3, SECC_BIT_MASK_1)
        data[3] += SECC_ValueToData(self.supportedEnergyTransfer_DCcc, 4, SECC_BIT_MASK_1)
        data[3] += SECC_ValueToData(self.supportedEnergyTransfer_DCunique, 5, SECC_BIT_MASK_1)
        data[3] += SECC_ValueToData(self.rsvd02, 6, SECC_BIT_MASK_2)
        data[4] = SECC_ValueToData(self.serviceList_Internet, 0, SECC_BIT_MASK_1)
        data[4] += SECC_ValueToData(self.rsvd03, 1, SECC_BIT_MASK_2)
        data[4] += SECC_ValueToData(self.serviceList_HPC1, 3, SECC_BIT_MASK_1)
        data[4] += SECC_ValueToData(self.rsvd04, 4, SECC_BIT_MASK_4)
        data[5] = SECC_ValueToData(self.freeService_EVCharging, 0, SECC_BIT_MASK_1)
        data[5] += SECC_ValueToData(self.freeService_Internet, 1, SECC_BIT_MASK_1)
        data[5] += SECC_ValueToData(self.freeService_ContractCert, 2, SECC_BIT_MASK_1)
        data[5] += SECC_ValueToData(self.freeService_OtherCustom, 3, SECC_BIT_MASK_1)
        data[5] += SECC_ValueToData(self.rsvd05, 4, SECC_BIT_MASK_4)
        data[6] = self.saScheduleManagement & 0xFF
        data[7] = SECC_ValueToData(self.cpMonitoringMode, 0, SECC_BIT_MASK_1)
        return bytearray(data)


# 50 ms
# typedef struct SECC_EVSE_STATUS
class SECC_EvseStatus:
    def __init__(self):
        self.evseHeartbeat = 0
        self.chargingControl = 0
        self.notificationMaxDelay = 0
        self.evseIsolationStatus = 0
        self.rsvd00 = 0
        self.evseProcessing_AuthEIM = 0
        self.evseProcessing_CPD = 0
        self.evseProcessing_CableCheck = 0
        self.isolationMonitoringActive = 0
        self.triggerReNegotiation = 0
        self.rsvd01 = 0
        self.triggerStateE = 0
        self.rsvd02 = 0
        self.evseCurrentLimitAchieved = 0
        self.evseVoltageLimitAchieved = 0
        self.evsePowerLimitAchieved = 0
        self.rsvd03 = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.evseHeartbeat & 0xFF
        data[1] = self.chargingControl & 0xFF
        data_array = SECC_IntToDataArray(self.notificationMaxDelay, byte_length=2, signed=False)
        SECC_Copy(data_array, data[2:], len(data_array))
        data[4] = self.evseIsolationStatus & 0xFF
        data[5] = self.rsvd00 & 0xFF
        data[6] = SECC_ValueToData(self.evseProcessing_AuthEIM, 0, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.evseProcessing_CPD, 1, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.evseProcessing_CableCheck, 2, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.isolationMonitoringActive, 3, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.triggerReNegotiation, 4, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.rsvd01, 5, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.triggerStateE, 6, SECC_BIT_MASK_1)
        data[6] += SECC_ValueToData(self.rsvd02, 7, SECC_BIT_MASK_1)
        data[7] = SECC_ValueToData(self.evseCurrentLimitAchieved, 0, SECC_BIT_MASK_1)
        data[7] += SECC_ValueToData(self.evseVoltageLimitAchieved, 1, SECC_BIT_MASK_1)
        data[7] += SECC_ValueToData(self.evsePowerLimitAchieved, 2, SECC_BIT_MASK_1)
        data[7] += SECC_ValueToData(self.rsvd03, 3, SECC_BIT_MASK_5)
        return bytearray(data)


# 200 ms
# typedef struct SECC_EVSE_CHARGE_PARAMETERS1
class SECC_EvseChgParam1:
    def __init__(self):
        self.f_evseMaximumCurrentLimit = float(0)
        self.u_evseMaximumPowerLimit = 0
        self.f_evseMaximumVoltageLimit = float(0)
        self.f_evsePeakCurrentRipple = float(0)

    def ByteArray(self):
        data = [0] * 8
        data_array = SECC_FloatToDataArray(self.f_evseMaximumCurrentLimit, multiple=10)
        SECC_Copy(data_array, data[0:], len(data_array))
        data_array = SECC_IntToDataArray(self.u_evseMaximumPowerLimit, multiple=0.1, signed=False)
        SECC_Copy(data_array, data[2:], len(data_array))
        data_array = SECC_FloatToDataArray(self.f_evseMaximumVoltageLimit, multiple=10)
        SECC_Copy(data_array, data[4:], len(data_array))
        data_array = SECC_FloatToDataArray(self.f_evsePeakCurrentRipple, multiple=10)
        SECC_Copy(data_array, data[6:], len(data_array))
        return bytearray(data)


# 200 ms
# typedef struct SECC_EVSE_CHARGE_PARAMETERS2
class SECC_EvseChgParam2:
    def __init__(self):
        self.f_evseMinimumCurrentLimit = float(0)
        self.f_evseMinimumVoltageLimit = float(0)
        self.f_evseCurrentRegulationTolerance = float(0)
        self.u_evseEnergyToBeDelivered = 0

    def ByteArray(self):
        data = [0] * 8
        data_array = SECC_FloatToDataArray(self.f_evseMinimumCurrentLimit, multiple=10)
        SECC_Copy(data_array, data[0:], len(data_array))
        data_array = SECC_FloatToDataArray(self.f_evseMinimumVoltageLimit, multiple=10)
        SECC_Copy(data_array, data[2:], len(data_array))
        data_array = SECC_FloatToDataArray(self.f_evseCurrentRegulationTolerance, multiple=10)
        SECC_Copy(data_array, data[4:], len(data_array))
        data_array = SECC_FloatToDataArray(self.u_evseEnergyToBeDelivered, multiple=0.1, signed=False)
        SECC_Copy(data_array, data[6:], len(data_array))
        return bytearray(data)


# 50 ms
# typedef struct SECC_EVSE_PRESENT_VOLT_CURR
class SECC_EvsePresVoltCurr:
    def __init__(self):
        self.f_evsePresentVoltage = float(0)
        self.f_evsePresentCurrent = float(0)

    def ByteArray(self):
        data = [0] * 8
        data_array = SECC_FloatToDataArray(self.f_evsePresentVoltage, multiple=10)
        SECC_Copy(data_array, data[0:], len(data_array))
        data_array = SECC_FloatToDataArray(self.f_evsePresentCurrent, multiple=10)
        SECC_Copy(data_array, data[2:], len(data_array))
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_DIN_ID_1
class SECC_EvseDinID1:
    def __init__(self):
        self.evseDinId1 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseDinId1, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_DIN_ID_2
class SECC_EvseDinID2:
    def __init__(self):
        self.evseDinId2 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseDinId2, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_DIN_ID_3
class SECC_EvseDinID3:
    def __init__(self):
        self.evseDinId3 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseDinId3, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_DIN_ID_4
class SECC_EvseDinID4:
    def __init__(self):
        self.evseDinId4 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseDinId4, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_ISO_ID_1
class SECC_EvseIsoID1:
    def __init__(self):
        self.evseIsoId1 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseIsoId1, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_ISO_ID_2
class SECC_EvseIsoID2:
    def __init__(self):
        self.evseIsoId2 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseIsoId2, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_ISO_ID_3
class SECC_EvseIsoID3:
    def __init__(self):
        self.evseIsoId3 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseIsoId3, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_ISO_ID_4
class SECC_EvseIsoID4:
    def __init__(self):
        self.evseIsoId4 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseIsoId4, byte_length=8, signed=False)
        return bytearray(data)


# 500 ms
# typedef struct SECC_EVSE_ISO_ID_5
class SECC_EvseIsoID5:
    def __init__(self):
        self.evseIsoId5 = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseIsoId5, byte_length=8, signed=False)
        return bytearray(data)


# EVENT
# typedef struct SECC_EVSE_TIMESTAMP
class SECC_EvseTimeStamp:
    def __init__(self):
        self.evseTimeStamp = 0

    def ByteArray(self):
        data = SECC_IntToDataArray(self.evseTimeStamp, byte_length=8, signed=False)
        return bytearray(data)


# EVENT
# typedef struct SECC_EVSE_SECC_REBOOT
class SECC_EvseSeccReboot:
    def __init__(self):
        self.rebootR = 0
        self.rebootE = 0
        self.rebootB = 0
        self.rebootO1 = 0
        self.rebootO2 = 0
        self.rebootT = 0
        self.rsvd00 = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.rebootR & 0xFF
        data[1] = self.rebootE & 0xFF
        data[2] = self.rebootB & 0xFF
        data[3] = self.rebootO1 & 0xFF
        data[4] = self.rebootO2 & 0xFF
        data[5] = self.rebootT & 0xFF
        return bytearray(data)


# typedef struct SECC_SECC_STATUS1
class SECC_SeccStatus1:
    def __init__(self):
        self.seccHeartbeat = 0
        self.seccStatus_legacy = 0
        self.evErrorCode = 0
        self.seccErrorCode = 0
        self.seccVersionMajor = 0
        self.seccVersionMinor = 0
        self.seccVersionPatch = 0
        self.pncReady = 0 # / < 00: None, 01: Not ready, 02: Ready

    def Parsing(self, data_array, byte_array):
        self.seccHeartbeat = data_array[0]
        self.seccStatus_legacy = data_array[1]
        self.evErrorCode = data_array[2]
        self.seccErrorCode = data_array[3]
        self.seccVersionMajor = data_array[4]
        self.seccVersionMinor = data_array[5]
        self.seccVersionPatch = data_array[6]
        self.pncReady = data_array[7]


# typedef struct SECC_SECC_STATUS2
class SECC_SeccStatus2:
    def __init__(self):
        self.cpOscillator = 0
        self.f_cpVoltage = float(0)
        self.hpgpLinkStatus = 0
        self.tlsErrorAlert = 0

    def Parsing(self, data_array, byte_array):
        self.cpOscillator = SECC_DataToValue(data_array[0], 0, SECC_BIT_MASK_1)
        self.f_cpVoltage = SECC_FloatFromByteArray(byte_array[1:2], multiple=0.1, signed=True)
        self.hpgpLinkStatus = SECC_DataToValue(data_array[3], 0, SECC_BIT_MASK_1)
        self.tlsErrorAlert = data_array[4]


# typedef struct SECC_SECC_EV_SERVICE_SELECTION
class SECC_SeccEvSvcSelect:
    def __init__(self):
        self.selectedChargingProtocol = 0
        self.selectedPaymentOption = 0
        self.selectedService_EVCharging = 0
        self.selectedService_Internet = 0
        self.selectedService_ContractCert = 0
        self.selectedService_OtherCustom = 0
        self.selectedService_HPC1 = 0
        self.selectedContractService_Installation = 0
        self.selectedContractService_Update = 0
        self.selectedEnergyTransferMode = 0
        self.selectedSAScheduleTupleID = 0

    def Parsing(self, data_array, byte_array):
        self.selectedChargingProtocol = data_array[0]
        self.selectedPaymentOption = data_array[1]
        self.selectedService_EVCharging = SECC_DataToValue(data_array[2], 0, SECC_BIT_MASK_1)
        self.selectedService_Internet = SECC_DataToValue(data_array[2], 1, SECC_BIT_MASK_1)
        self.selectedService_ContractCert = SECC_DataToValue(data_array[2], 2, SECC_BIT_MASK_1)
        self.selectedService_OtherCustom = SECC_DataToValue(data_array[2], 3, SECC_BIT_MASK_1)
        self.selectedService_HPC1 = SECC_DataToValue(data_array[2], 4, SECC_BIT_MASK_1)
        self.selectedContractService_Installation = SECC_DataToValue(data_array[2], 5, SECC_BIT_MASK_1)
        self.selectedContractService_Update = SECC_DataToValue(data_array[2], 6, SECC_BIT_MASK_1)
        self.selectedEnergyTransferMode = data_array[3]
        self.selectedSAScheduleTupleID = data_array[4]


# typedef struct SECC_SECC_SESSION_ID
class SECC_SeccSessionID:
    def __init__(self):
        self.sessionID = 0

    def Parsing(self, data_array, byte_array):
        self.sessionID = SECC_IntFromByteArray(byte_array, signed=False)


# typedef struct SECC_SECC_EVCC_INFO
class SECC_SeccEvccInfo:
    def __init__(self):
        self.evccMAC = 0
        self.evccAttn = 0

    def Parsing(self, data_array, byte_array):
        self.evccMAC = SECC_IntFromByteArray(byte_array[:6], signed=False)
        self.evccAttn = data_array[6]


# typedef struct SECC_SECC_EV_CHG_PARAM1
class SECC_SeccEVChgParam1:
    def __init__(self):
        self.maxEntriesSAScheduleTuple = 0
        self.departureTime = 0
        self.u_evMaximumPowerLimit = 0

    def Parsing(self, data_array, byte_array):
        self.maxEntriesSAScheduleTuple = SECC_IntFromByteArray(byte_array[0:2], signed=False)
        self.departureTime = SECC_IntFromByteArray(byte_array[2:6], signed=False)
        self.u_evMaximumPowerLimit = SECC_FloatFromByteArray(byte_array[6:8], multiple=10, signed=False)


# typedef struct SECC_SECC_EV_CHG_PARAM2
class SECC_SeccEVChgParam2:
    def __init__(self):
        self.f_evMaximumCurrentLimit = float(0)
        self.f_evMaximumVoltageLimit = float(0)
        self.u_evEnergyCapacity = 0
        self.u_evEnergyRequest = 0

    def Parsing(self, data_array, byte_array):
        self.f_evMaximumCurrentLimit = SECC_FloatFromByteArray(byte_array[0:2], multiple=0.1)
        self.f_evMaximumVoltageLimit = SECC_FloatFromByteArray(byte_array[2:4], multiple=0.1)
        self.u_evEnergyCapacity = SECC_IntFromByteArray(byte_array[4:6], multiple=10, signed=False)
        self.u_evEnergyRequest = SECC_IntFromByteArray(byte_array[6:8], multiple=10, signed=False)


# typedef struct SECC_SECC_EV_SOC_RELATED_PARAM
class SECC_SeccEvSOC:
    def __init__(self):
        self.chargingComplete = 0        # 0: Not complete, 1: Complete, 3: NONE(default)
        self.bulkChargingComplete = 0    # 0: Not complete, 1: Complete, 3: NONE(default)
        self.rsvd00 = 0
        self.evSOC = 0                   # State of charge of the EV's battery (RESS)
        self.fullSOC = 0
        self.bulkSOC = 0
        self.u_remainingTimeToFullSOC = 0
        self.u_remainingTimeToBulkSOC = 0

    def Parsing(self, data_array, byte_array):
        self.chargingComplete = SECC_DataToValue(data_array[0], 0, SECC_BIT_MASK_2)
        self.bulkChargingComplete = SECC_DataToValue(data_array[0], 2, SECC_BIT_MASK_2)
        self.evSOC = data_array[1]
        self.fullSOC = data_array[2]
        self.bulkSOC = data_array[3]
        self.u_remainingTimeToFullSOC = SECC_IntFromByteArray(byte_array[4:6], multiple=10)
        self.u_remainingTimeToBulkSOC = SECC_IntFromByteArray(byte_array[6:8], multiple=10)


#typedef struct SECC_SECC_EV_TGT_VOLTCURR
class SECC_SeccEvTgVoltCurr:
    def __init__(self):
        self.f_targetVoltage = float(0)
        self.f_targetCurrent = float(0)

    def Parsing(self, data_array, byte_array):
        self.f_targetVoltage = SECC_FloatFromByteArray(byte_array[0:2], multiple=0.1)
        self.f_targetCurrent = SECC_FloatFromByteArray(byte_array[2:4], multiple=0.1)


# typedef struct SECC_SECC_TIMESTAMP
class SECC_SeccTimestamp:
    def __init__(self):
        self.seccTimestamp = 0  # Unix Time Stamp format

    def Parsing(self, data_array, byte_array):
        self.seccTimestamp = SECC_IntFromByteArray(byte_array, multiple=1)


# typedef struct SECC_SECC_STATUS3_PNC
class SECC_SeccStatus3:
    def __init__(self):
        self.seccStatus = 0
        self.seccEstablishedInfo = 0  # 0: NONE, 1: Non-TLS, 2: Public TLS, 3: PE TLS

    def Parsing(self, data_array, byte_array):
        self.seccStatus = data_array[0]
        self.seccEstablishedInfo = data_array[7]


# typedef struct SECC_SECC_EMERGENCY_NOTI
class SECC_SeccEmgNoti:
    def __init__(self):
        self.notificationCount = 0

    def Parsing(self, data_array, byte_array):
        self.notificationCount = data_array[0]


# typedef struct SECC_EVSE_SA_AGENT_CONN_CONF
class SECC_SaAgentConnConf:
    def __init__(self):
        self.saAgentIpAddr1 = 0
        self.saAgentIpAddr2 = 0
        self.saAgentIpAddr3 = 0
        self.saAgentIpAddr4 = 0
        self.saAgentPort = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.saAgentIpAddr1
        data[1] = self.saAgentIpAddr2
        data[2] = self.saAgentIpAddr3
        data[3] = self.saAgentIpAddr4
        data[4:] = SECC_IntToDataArray(self.saAgentPort, multiple=1, byte_length=2, signed=False)
        return bytearray(data)


# typedef struct SECC_EVSE_SECC_PNC_CONF
class SECC_EvsePnCConf:
    def __init__(self):
        self.pkiEnvironmentSelection = 0
        self.certChainValidationOption = 0
        self.reKeyOption = 0

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.pkiEnvironmentSelection
        data[1] = self.certChainValidationOption
        data[2] = self.reKeyOption
        return bytearray(data)


# typedef struct SECC_EVSE_SA_AGENT_COMM_TIMEOUT
class SECC_EvseSaAgentCommTO:
    def __init__(self):
        self.saAgentHelloResponseTimeout = 0                    # default : 30s
        self.saAgentGetCertificateStatusResponseTimeout = 0     # default : 30s
        self.saAgentSignSECCertificateResponseTimeout = 0       # default : 30s
        self.saAgentCertInstallationPerformanceTimeout = 0      # default : 4.5s
        self.saAgentCertUpdatePerformanceTimeout = 0            # default : 4.5s
        self.saAgentAuthorizeRespnseTimeout = 0                 # default : 4.5s

    def ByteArray(self):
        data = [0] * 8
        data[0] = self.saAgentHelloResponseTimeout
        data[1] = self.saAgentGetCertificateStatusResponseTimeout
        data[2] = self.saAgentSignSECCertificateResponseTimeout
        data[3] = self.saAgentCertInstallationPerformanceTimeout
        data[4] = self.saAgentCertUpdatePerformanceTimeout
        data[5] = self.saAgentAuthorizeRespnseTimeout
        return bytearray(data)


# typedef struct SECC_SECC_SA_COMM_STATUS
class SECC_SeccSaCommStatus:
    def __init__(self):
        self.saAgentInitResult = 0
        self.saAgentInitDetails = 0
        self.saAgentCertInstallationDetails = 0
        self.saAgentCertUpdateDetails = 0
        self.saAgentAuthorizeResponseDetails = 0

    def Parsing(self, data_array, byte_array):
        self.saAgentInitResult = data_array[0]
        self.saAgentInitDetails = data_array[1]
        self.saAgentCertInstallationDetails = data_array[2]
        self.saAgentCertUpdateDetails = data_array[3]
        self.saAgentAuthorizeResponseDetails = data_array[4]


# typedef struct SECC_SECC_IP_STATUS
class SECC_SeccIpStatus:
    def __init__(self):
        self.seccIpAddr1 = 0  # default: 192
        self.seccIpAddr2 = 0  # default: 168
        self.seccIpAddr3 = 0  # default: 0
        self.seccIpAddr4 = 0  # default: 100

    def Parsing(self, data_array, byte_array):
        self.seccIpAddr1 = data_array[0]
        self.seccIpAddr2 = data_array[1]
        self.seccIpAddr3 = data_array[2]
        self.seccIpAddr4 = data_array[3]


# ######### SECC variables ############

# typedef struct SECC_VAR
class SECC_Var:
    def __init__(self):
        self.is_activated = 0
        self.prev_secc_heartbeat = 0
        self.secc_activated_check_count = 0
        self.rx_count = 0


# typedef struct SECC_PARAMETERS
class SECC_Parameters:
    def __init__(self):
        self.evse_config = SECC_EvseConfig()
        self.evse_status = SECC_EvseStatus()
        self.evse_chg_param1 = SECC_EvseChgParam1()
        self.evse_chg_param2 = SECC_EvseChgParam2()
        self.evse_volt_curr = SECC_EvsePresVoltCurr()
        self.evse_timestemp = SECC_EvseTimeStamp()
        self.evse_reboot = SECC_EvseSeccReboot()
        self.secc_status1 = SECC_SeccStatus1()
        self.secc_status2 = SECC_SeccStatus2()
        self.secc_sv_sel = SECC_SeccEvSvcSelect()
        self.secc_session_id = SECC_SeccSessionID()
        self.secc_evcc_info = SECC_SeccEvccInfo()
        self.secc_chg_param1 = SECC_SeccEVChgParam1()
        self.secc_chg_param2 = SECC_SeccEVChgParam2()
        self.secc_soc = SECC_SeccEvSOC()
        self.secc_tg = SECC_SeccEvTgVoltCurr()        # EV Target Voltage / Current
        self.secc_tstamp = SECC_SeccTimestamp()
        self.secc_status3 = SECC_SeccStatus3()
        self.secc_emg_noti = SECC_SeccEmgNoti()
        self.secc_saagent_conf = SECC_SaAgentConnConf()
        self.evse_evsepnc_conf = SECC_EvsePnCConf()
        self.evse_saagent_timeout = SECC_EvseSaAgentCommTO()
        self.secc_sa_comm_status = SECC_SeccSaCommStatus()
        self.secc_ip_status = SECC_SeccIpStatus()
        self.secc_var = SECC_Var()

