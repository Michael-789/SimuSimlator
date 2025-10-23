from enum import Enum


class DetectionTypeClassification(Enum):
    UNKNOWN = 0
    FRIENDLY = 1
    CIVILIAN = 2
    OPPOSING = 3

class DetectorTypes(Enum):
    WC_D = 0
    NG_S_Msr = 1
    NG_S_Unk = 2
    NG_S_Calc = 3
    MRKR_Mrkr = 4
    MRKR_Unk = 5
    NG_Msr = 6
    NG_Unk = 7
    NG_Calc = 8
    USR_AT = 9
    USR_GE = 10
    DH = 11
