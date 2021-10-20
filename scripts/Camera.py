from Zone import *
class Camera:
    def __init__(self, cam_id, name, zones) -> None:
        self.cam_id = cam_id
        self.name = name
        if len(zones) == 0 or isinstance(zones[0], Zone):
            self.zones = zones
        else:
            raise TypeError
    def createId() -> int:
        sql = "select cam_id from Cameras order by cam_id desc limit 1"
        cursor = help.executeSQL(sql)
        print(cursor)
        return cursor.fetchone()[0] + 1
    def insert(self) -> None:
        values = "({},'{}')".format(self.cam_id, self.name)
        sql = "insert into Cameras values {}".format(values)
        help.insertSQL(sql)

        