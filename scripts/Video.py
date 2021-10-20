from sqlite3.dbapi2 import Cursor


from Point import *
import sys
import os
sys.path.insert(1, os.path.realpath(__file__).replace('/scripts/Video.py','/api'))
import apiHelpers as help

class Video:
    def __init__(self, vid_id, name, cam_id, path) -> None:
        self.vid_id = vid_id if vid_id != -1 else Video.createId()
        self.name = name
        self.cam_id = cam_id
        self.path = path
    def createId() -> int:
        sql = "select video_id from Videos order by video_id desc limit 1"
        cursor = help.executeSQL(sql)
        return cursor.fetchone()[0] + 1
    def insert(self) -> None:
        values = "({},'{}',{},'{}')".format(self.vid_id, self.name, self.cam_id, self.path)
        sql = "insert into Videos values {};".format(values)
        help.insertSQL(sql)
        