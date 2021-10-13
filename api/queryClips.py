import sqlite3
import os
import apiHelpers as help

def queryClips(camera: str, clip: str, start: str, end: str, zones: list) -> str:
    # build sql string
    select = "SELECT * \n"
    frum = "FROM Frames f \n"
    join1 = "\tJOIN Cameras c ON f.cam_id = c.cam_id \n"
    join2 = "\tJOIN Videos v ON f.video_id = v.video_id \n"
    join3 = "\tJOIN Zones z ON f.zone_id = z.zone_id \n"
    where = "WHERE c.cam_name = '{}' \n".format(camera) + \
                "\tAND v.video_name = '{}' \n".format(clip) + \
                "\tAND f.time_stamp BETWEEN '{}' AND '{}' \n".format(start, end) + \
                "\tAND z.zone_name IN ('{}')".format("','".join(zones))
    sql = "".join([select,frum,join1,join2,join3,where,";"])
    # sql = "".join([select,frum,join1,join2,join3,";"])
    
    cursor = help.executeSQL(sql)
    for row in cursor:
        print(row)
    # combine frames into clips
    dir = help.changeDir('clips')
    # save each clip to clips directory
    return "Clips saved in {}".format(dir)

print(queryClips("Test Cam 1","SW view","2021-02-22:01:00:00.00", "2022-03-05:07:10:00.13",["printer", "station"]))


# WHERE Camera = 'camera 5'
# /*could add clip name*/
# AND Timestamp BETWEEN '2005-01-01' AND '2022-01-01' 
# /*startime and end time parameters to be added in*/
# AND Zone IN ('copier', 'printer');"