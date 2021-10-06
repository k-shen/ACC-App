import sqlite3 as sqlite
import flask
from flask.helpers import url_for
from scripts.Camera import *
from scripts.Video import Video
from flask import request
import os


app = flask.Flask(__name__, static_folder='')
UPLOAD_FOLDER = './data/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return flask.redirect('/home')

@app.route('/home', methods=['GET'])
def show():
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    all = (c.execute("select * from Cameras").fetchall())
    conn.commit()
    conn.close()

    cam_list = []
    for cam in all:
        cam_list.append(loadTempCamera(cam))

    return flask.render_template('home.html', cam_list=cam_list)

def loadTempCamera(data):
    print(data)
    cam = Camera(data[0], data[1], [])
    
    return cam


def loadCameraObj(id):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    data = (c.execute("select * from Cameras where cam_id=?",(id,)).fetchone())
    zones = (c.execute("select * from Zones where cam_id=?",(id,)).fetchall())
    conn.commit()
    conn.close()
    zone_list = []
    for zone in zones:
        zone_list.append(loadZoneObj(zone))
    cam = Camera(data[0], data[1], zone_list)
    return cam

def loadZoneObj(data):
    z = Zone(data[0], data[1], data[2], Point(data[3], data[4]), Point(data[5], data[6]))
    return z

@app.route('/cam/<cid>/delete', methods=['POST'])
def deleteCam(cid):
    #connect to data base
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    idToDelete = request.form['cid']
    c.execute("delete from Cameras where cam_id=?",(idToDelete,))
    conn.commit()
    conn.close()

    print("deleted camera id " + str(cid))
    return flask.redirect('/home')

@app.route('/vid/<vid>/delete', methods=['POST'])
def deleteVid(vid):
    #connect to data base
    
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    idToDelete = request.form['vid']
    c.execute("delete from Videos where video_id=?",(idToDelete,))
    conn.commit()
    conn.close()

    print("deleted video id " + str(vid))
    cid = request.form['cid']
    return flask.redirect('/cam/{}'.format(cid))

@app.route('/cam/<cid>', methods=['GET', 'POST'])
def viewCam(cid):
    #connect to data base
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam = loadCameraObj(cid)
    details = (c.execute("select * from Videos where cam_id=?",(cid,)).fetchall())
    conn.commit()
    conn.close()

    videos = []
    for v in details:
        videos.append(loadVideoObj(v))

    return flask.render_template('camera.html', cam=cam, data=videos)

def loadVideoObj(data):
    return Video(data[0], data[1], data[2], data[3])

@app.route("/cam/<cid>/addVideo", methods=['GET', "POST"])
def addVideo(cid):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam_info = (c.execute("select * from Cameras where cam_id=?",(cid,)).fetchone())
    conn.commit()
    conn.close()
    cam = loadTempCamera(cam_info)
    
    return flask.render_template("addVideo.html", cam=cam)


@app.route("/cam/<cid>/addVideo/success", methods=["POST"])
def addVideoSuccess(cid):
    #connect to data base
    video = flask.request.files['videofile']
    vname = flask.request.form['vname']
    vpath = os.path.join(app.config['UPLOAD_FOLDER'], vname)
    #video.save(os.path.join(app.config['UPLOAD_FOLDER'], vname))

    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Videos (video_name, cam_id, video_path) VALUES (?, ?, ?);", \
        (vname, cid, vpath))
    conn.commit()
    conn.close()

    print("added video" + vname + " of camera id " + str(cid))
    return flask.redirect('/cam/{}'.format(cid))

@app.route("/addCamera", methods=['GET', "POST"])
def addCamera():
    return flask.render_template("addCamera.html")

@app.route("/drawbox", methods=['GET', "POST"])
def drawBox():
    return flask.render_template('drawbox.html')

@app.route("/frames", methods=['GET', 'POST'])
def queryInit():
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    zones = (c.execute("select * from Zones").fetchall())
    conn.commit()
    conn.close()
    return flask.render_template('query.html', zones=zones, frames=[])

@app.route("/frames/query", methods=['GET', 'POST'])
def query():
    zones = request.form.getlist('zones')
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    z_str = "({});".format(",".join(zones))
    frames = c.execute("select frame_num, video_id, f.cam_id, f.zone_id, time_stamp from Frames f left join Zones z on f.zone_id = z.zone_id where z.zone_id in {}".format(z_str)).fetchall()
    zones = (c.execute("select * from Zones").fetchall())
    conn.commit()
    conn.close()
    return flask.render_template('query.html', zones=zones, frames=frames)

@app.route("/cam/<cid>/draw", methods=['GET', "POST"])
def redrawBox(cid):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    # what does this (cid,) mean ? cid is the variable passed in
    cam_info = (c.execute("select * from Cameras where cam_id=?",(cid,)).fetchone())
    conn.commit()
    conn.close()
    cam = loadTempCamera(cam_info)

    return flask.render_template('redraw.html', cam=cam)

# does this look right?
# cid is what i used for camera id and idt we will need it here right now
# can you motify the /frames/query function? yupp
# i need to first test if i can get the forms info like that hence the print statements lol


# @app.route("/frames/<cid>", methods=['GET'])
# def getFrames(cid):
#     conn = sqlite.connect('./data/database.db')
#     c = conn.cursor()
#     frame_tups = list(c.execute("select * from Frames f join Zones z on f.zone_id = z.zone_id where z.zone_name =?",(cid)).fetchall())
#     conn.close()
#     return frame_tups

if __name__ == '__main__':
    app.run(port=8001, host='127.0.0.1',debug=True, use_evalex=False,use_reloader=True)