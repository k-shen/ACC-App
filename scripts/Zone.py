from scripts.Point import *
class Zone:
    def __init__(self, id, name, cid, top_left, bot_right) -> None:
        self.zone_id = id
        self.name = name
        self.cam_id = cid
        if not isinstance(top_left, Point) or not isinstance(bot_right, Point):
            raise TypeError("Need the points to create a zone")
        self.top_left = top_left
        self.bot_right = bot_right