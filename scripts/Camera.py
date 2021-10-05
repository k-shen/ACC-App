from scripts.Zone import *
class Camera:
    def __init__(self, cam_id, name, zones) -> None:
        self.cam_id = cam_id
        self.name = name
        if len(zones) == 0 or isinstance(zones[0], Zone):
            self.zones = zones
        else:
            raise TypeError

        