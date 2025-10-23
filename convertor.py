import json
import struct
import uuid

from rticonnector.idl_types.Detection import P_Tactical_Sensor_PSM_C_Detection, CharSequence
from rticonnector.utils import char_sequence_to_str, str_to_char_sequence

from SimObj import SimObj
from enum_p import DetectorTypes


def convert_from_idl(detection):
    obj = SimObj()
    obj.message_id = str(int2uuid(detection.A_detectionUniqueID.A_msb,detection.A_detectionUniqueID.A_lsb))
    obj.location_altitude = detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_altitude
    obj.location_longitude = detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_longitude
    obj.location_latitude = detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_latitude
    obj.classification = char_sequence_to_str(detection.A_detectionClassification)
    obj.priority = detection.A_priority
    sensor_name = char_sequence_to_str(detection.A_spatialInfo.A_descriptiveInfo.A_recognizingDetectorTypes[0].value)
    obj.sensor_id = DetectorTypes[sensor_name].value
    for _method in detection.A_detectionMethods:
       msb =  int(char_sequence_to_str(_method.A_detectorType))
       lsb = int(char_sequence_to_str(_method.A_algorithm))
       id = int2uuid(msb,lsb)
       obj.fused_tracks.append(str(id))

    return obj


def convert_to_idl(obj : SimObj):
    detection = P_Tactical_Sensor_PSM_C_Detection()
    detection.A_sourceID.A_platformId = 1
    detection.A_sourceID.A_systemId = 14
    detection.A_sourceID.A_moduleId = 3
    id = uuid.UUID(obj.message_id)
    msb, lsb = uuid2int(id)
    detection.A_detectionUniqueID.A_msb = int(msb)
    detection.A_detectionUniqueID.A_lsb = int(lsb)
    detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_altitude = obj.location_altitude
    detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_longitude = obj.location_longitude
    detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_latitude = obj.location_latitude
    detection.A_detectionClassification = str_to_char_sequence(obj.classification)
    # det_type = CharSequence(value=str_to_char_sequence('AT'))
    # # det_type = CharSequence(value=list('AT'))
    #
    # detection.A_spatialInfo.A_descriptiveInfo.A_recognizingDetectorTypes = [det_type]
    # detection.A_spatialInfo.A_descriptiveInfo.A_recognizingDetectorTypes.append(list(det_type))

    return detection

# def str_to_char_sequence2(str_input: str) -> CharSequence:
#     return CharSequence(value=list(str_input)) if str_input is not None else CharSequence()

# def str_to_char_sequence(str_input: str) -> list[int]:
#     return [ord(ch) for ch in str_input] if str_input is not None else []

def int2uuid(msb,lsb):
    return uuid.UUID(int=(int(msb) << 64) | int(lsb))
    # return uuid.UUID(int=(int(msb) << 64) + int(lsb))

def uuid2int(uuid):
    msb, lsb = struct.unpack(">QQ", uuid.bytes)  # Unsigned 64-bit
    # msb,lsb = struct.unpack(">qq", uuid.bytes)
    return msb, lsb

