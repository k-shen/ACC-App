import sqlite3
import sys
import os
sys.path.append(os.path.realpath(__file__).replace('/api/newCamera.py',''))
print(sys.path)
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

from scripts.Video import Video
from scripts.Zone import *
from scripts.Camera import *

'''Need to talk to Joey to figure out how to pass zones'''
def newCamera(name: str, zones: list[dict], video_path: str, video_name: str) -> str:
    try:
        cam_id = Camera.createId()

        # insert zones and initiate array of zones for camera class
        zone_objs = []
        for z in zones:
            # req_keys = {"tl_x","tl_y", "br_x","br_y","name",}
            # # not really sure how this will work..
            # if req_keys.difference(zones.keys())
            try:
                top_left = Point(z["tl_x"], z["tl_y"])
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

        return "Camera, video, and zones were all successfully inserted"
    except:
        return "There was an error"
zones = {"tl_x":4,"tl_y":4,"br_x":10,"br_y":0,"name":"test_zone"}

print(newCamera("testvid",zones,'test/path/vid0.mp4','vid0'))

    