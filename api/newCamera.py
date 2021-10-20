import sqlite3
import sys
import os
# sys.path.append(os.path.realpath(__file__).replace('/api/newCamera.py',''))

# should be able to change environment variable pretty easily
# PYTHONPATH- add various directories, and they will be a part of the import path
# .bashrc
# export PYTHONPATH="${PYTHONPATH}:/path/to/my/modules/"
# add to bash
#
'''
Ryan's stuff:
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/path/to/application/app/folder')

import file
'''
sys.path.insert(1, os.path.realpath(__file__).replace('/api/newCamera.py','/scripts'))
# print(sys.path)
from Video import Video
from Zone import Zone
from Camera import Camera
from Point import Point
import apiHelpers as help

'''Need to talk to Joey to figure out how to pass zones'''
def newCamera(name: str, zones: list, video_path: str, video_name: str) -> str:
    # try:
    cam_id = Camera.createId()

    # insert zones and initiate array of zones for camera class
    zone_objs = []
    for z in zones:
        # req_keys = {"tl_x","tl_y", "br_x","br_y","name",}
        # # not really sure how this will work..
        # if req_keys.difference(zones.keys())
        try:
            top_left = Point(z['tl_x'], z['tl_y'])
            bot_right = Point(z["br_x"], z["br_y"])
            zone = Zone(-1, z["name"], cam_id, top_left, bot_right)
            zone_objs.append(zone)
            zone.insert()
        except:
            raise TypeError("Make sure the zones have all required attributes")

    # insert camera
    camera = Camera(cam_id, name, zone_objs)
    camera.insert()

    # insert video
    video = Video(-1, video_name, cam_id, video_path)
    video.insert()

    return "Camera, video, and zones were all successfully inserted"
    # except:
    #     return "There was an error"

def check():
    sql = 'select * from Cameras c join Zones z on c.cam_id = z.cam_id ' + \
                                'join Videos v on c.cam_id = v.cam_id;'
    cursor = help.executeSQL(sql)
    for i in cursor:
        print(i)

zones = [{"tl_x":4,"tl_y":4,"br_x":10,"br_y":0,"name":"test_zone"}]
print(type(zones))
# print(zones.keys())

print(newCamera("test insert cam",zones,'test/path/vid0.mp4','vid0'))
check()
    