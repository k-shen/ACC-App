from scripts.Point import *
class Zone:
    def __init__(self, name, top_left, bot_right) -> None:
        self.name = name
        if not isinstance(top_left, Point) or not isinstance(bot_right, Point):
            raise TypeError("Need the points to create a zone")
        self.top_left = top_left
        self.bot_right = bot_right