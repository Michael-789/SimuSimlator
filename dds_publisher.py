import random
import struct
import sys
import uuid

from rticonnector.utils import str_to_char_sequence

import enum_p
from time import sleep

from rticonnector.idl_types.Detection import P_Tactical_Sensor_PSM_C_Detection

from rticonnector.publisher import Publisher
from rticonnector.topic_data import TopicEnum

from convertor import uuid2int


class DDSPublisher():

    def __init__(self):
        self.publisher = Publisher(TopicEnum.DETECTION)

    def publish_created_data(self):
        for i in range(10):
            try:
                detection = self.create_data(i)
                self.publish(detection)
            except Exception as e:
                print(f'process of detection failed: {e}')
            sleep(1)


    def publish(self, detection):
        self.publisher.publish(detection)
        print(f"published {detection.__dict__}")

    def create_data(self, i):
        detection = P_Tactical_Sensor_PSM_C_Detection()
        detection.A_sourceID.A_platformId = 1
        detection.A_sourceID.A_systemId = 14
        detection.A_sourceID.A_moduleId = 3
        msb, lsb = uuid2int(uuid.uuid4())
        detection.A_detectionUniqueID.A_msb = int(msb)
        detection.A_detectionUniqueID.A_lsb = int(lsb)
        detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_altitude = 410
        detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_longitude = 34.124657 + i * 0.001
        detection.A_spatialInfo.A_physicalInfo.A_absoluteLocation.A_latitude = 32.8746121 + i * 0.001

        detection.A_detectionClassification = str_to_char_sequence(enum_p.DetectionTypeClassification((random.randint(0, 3))).name)

        return detection

    def random_number(self, uid):
        msb, lsb = self.uuid2int(uid)
        return msb, lsb

    def uuid2int(self, ID):
        """
        translate uuid to int
        :param ID:uuid object
        :return: 2 int_64 which represents input uuid (msb, lsb)
        """
        b_uuid = ID.int.to_bytes(16, byteorder=sys.byteorder, signed=False)
        return struct.unpack('2q', b_uuid)

