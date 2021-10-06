import sqlite3
from datetime import date, datetime
from datetime import timedelta

def insertFrames():
    conn = sqlite3.connect('database.db')
    desired_columns = "(frame_id,frame_num, video_id, cam_id,zone_id, time_stamp)"
    dt = datetime.strptime("2021-02-22:01:00:00.00", "%Y-%m-%d:%H:%M:%S.%f")
    for i in range(200,300):
        frame_id = str(i)
        frame_number = str(i//2)
        video_id = 1
        zone_id = i % 2 +1
        cam_id = 2
        # zone = ["printer", "copier"][zone_id]
        dt += timedelta(microseconds=40000) #datetime.strptime("3","%f")
        time_stamp = datetime.strftime(dt, "%Y-%m-%d:%H:%M:%S.%f")
        filepath = "frames/" + frame_id
        values = "({0},{1},{2},{3},{4},'{5}')".format(frame_id,frame_number, video_id,cam_id,zone_id, time_stamp)
        sql = "INSERT INTO Frames {0} VALUES {1}".format(desired_columns, values)
        conn.execute(sql)
        conn.commit()

insertFrames()
print("should have inserted")