import json


class SimObj:
    def __init__(self, **kwargs):
        self.message_id: str = ''
        self.trail_id: str = ''
        self.source: str = ''
        self.start_time: int = 0
        self.last_update_time: int = 0
        self.location_altitude: float = 0.0
        self.location_latitude: float = 0.0
        self.location_longitude: float = 0.0
        self.sensor_id: int = 0
        self.priority: int = 0
        self.classification: str = ''
        self.type: str = ''
        self.location_yaw: float = 0.0
        self.speed: float = 0.0
        self.vertical_speed: float = 0.0
        self.fused_tracks: [] = []
        self.__dict__.update(kwargs)

    def serialize_to_string(self):
        return json.dumps(self, default=lambda o: o.__dict__)
