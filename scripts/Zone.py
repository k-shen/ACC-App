import sqlite3
from Point import *
import sys
import os
sys.path.insert(1, os.path.realpath(__file__).replace('/scripts/Zone.py','/api'))
import apiHelpers as help

class Zone:
    def __init__(self, id, name, cid, top_left, bot_right) -> None:
        self.zone_id = id if id != -1 else Zone.createId()
        self.name = name
        self.cam_id = cid
        if not isinstance(top_left, Point) or not isinstance(bot_right, Point):
            raise TypeError("Need the points to create a zone")
        self.top_left = top_left
        self.bot_right = bot_right
    # get max id and then add oen
    def createId() -> int:
        sql = "select zone_id from Zones order by zone_id desc limit 1"
        cursor = help.executeSQL(sql)
        return cursor.fetchone()[0]+1
    def insert(self):
        ids = "({},'{}',{},".format(self.zone_id, self.name, self.cam_id)
        points = "{},{},{},{})".format(self.top_left.x, self.top_left.y, self.bot_right.x, self.bot_right.y)
        values = ids + points
        sql = "insert into Zones values {};".format(values)
        help.insertSQL(sql)