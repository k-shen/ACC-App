from sqlite3.dbapi2 import Cursor


from scripts.Point import *
import api.apiHelpers as help

class Video:
    def __init__(self, vid_id, name, cam_id, path) -> None:
        self.vid_id = vid_id if vid_id != -1 else self.createId()
        self.name = name
        self.cam_id = cam_id
        self.path = path
    def createId() -> int:
        sql = "select video_id from Videos order by video_id desc limit 1"
        cursor = help.executeSQL(sql)
        return cursor.fetchone() + 1
    def insert() -> None:
        values = "({},'{}',{},'{}')".format(self.vid_id, self.name, self.cam_id, self.video_path)
        sql = "insert into Videos values {};".format(values)
        help.insertSQL(sql)
        