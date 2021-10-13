import sqlite3
import apiHelpers as help

def redrawCamera(camera_name: str) -> str: # do we want this to be an image or the image path?
    select = "SELECT frame_num\n"
    frum = "FROM Frames f\n"
    join = "\tJOIN Cameras c ON f.cam_id = c.cam_id\n"
    where = "WHERE c.cam_name = {}\n".format(camera_name)
    limit = "LIMIT 1"

    sql = "".join([select, frum, join, where, limit])
    cursor = help.executeSQL(sql)
    example_frame = cursor.fetchone()

    # use example_frame to retrieve a frame or a file path and return it

    return example_frame # will need to be changed
