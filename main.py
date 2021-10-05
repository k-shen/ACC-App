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
    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    all = (c.execute("select * from Cameras").fetchall())
    conn.commit()
    conn.close()

    cam_list = []
    for cam in all:
        cam_list.append(loadTempCamera(cam))
    '''
    cam1 = Camera(1, "first cam", [])
    cam2 = Camera(2, "second cam", [])
    camera_list = [cam1, cam2]
    return flask.render_template('home.html', cam_list=camera_list)

def loadTempCamera(data):
    '''
    cam = Camera(data["cam_id"], data["cam_name"], [])
    return cam
    '''
    pass


def loadCameraObj(id):
    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    data = (c.execute("select * from Cameras where cam_id=?",(id,)).fetchone())
    zones = (c.execute("select * from Zones where cam_id=?",(id,)).fetchall())
    conn.commit()
    conn.close()
    zone_list = []
    for zone in zones:
        zone_list.append(loadZoneObj(zone))
    cam = Camera(data["cam_id"], data["cam_name"], zone_list)
    return cam
    '''
    pass

def loadZoneObj(data):
    z = Zone(data["zone_name"], Point(data["top_left_x"], data["top_left_y"]), Point(data["bot_right_x"], data["bot_right_y"]))
    return z

@app.route('/cam/<cid>/delete', methods=['POST'])
def deleteCam(cid):
    #connect to data base
    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    idToDelete = request.form['cid']
    c.execute("delete from Cameras where cam_id=?",(idToDelete,))
    conn.commit()
    conn.close()
    '''
    print("deleted camera id " + str(cid))
    return flask.redirect('/home')

@app.route('/vid/<vid>/delete', methods=['POST'])
def deleteVid(vid):
    #connect to data base
    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    idToDelete = request.form['vid']
    c.execute("delete from Videos where video_id=?",(idToDelete,))
    conn.commit()
    conn.close()
    '''
    print("deleted video id " + str(vid))
    cid = request.form['cid']
    return flask.redirect('/cam/{}'.format(cid))

@app.route('/cam/<cid>', methods=['GET', 'POST'])
def viewCam(cid):
    #connect to data base
    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam = loadCameraObj(cid)
    details = (c.execute("select from Videos where cam_id=?",(cid,)).fetchall())
    conn.commit()
    conn.close()
    '''
    print("viewing camera id " + str(cid))
    
    details = [Video(1, "SW EE206", 1), Video(2, "NW EE206", 1)]
    cam = Camera(1, "fake name", [])
    return flask.render_template('camera.html', cam=cam, data=details)

@app.route("/cam/<cid>/addVideo", methods=['GET', "POST"])
def addVideo(cid):
    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam_info = (c.execute("select from Cameras where cam_id=?",(idToDelete,)).fetchone())
    conn.commit()
    conn.close()
    cam = loadTempCamera(cam_info)
    '''
    print("here")
    cam = Camera(1, "fake name", [])
    return flask.render_template("addVideo.html", cam=cam)


@app.route("/cam/<cid>/addVideo/success", methods=["POST"])
def addVideoSuccess(cid):
    #connect to data base
    video = flask.request.files['videofile']
    vname = flask.request.form['vname']
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], vname))
    videoObj = Video(1, vname, cid)

    '''
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cur.execute("INSERT INTO Video VALUES (?, ?, ?);", \
        (videoObj.vid_id, videoObj.name, videoObj.cam_id))
    conn.commit()
    conn.close()
    '''
    print("added video" + vname + " of camera id " + str(cid))
    return flask.redirect('/cam/{}'.format(cid))


if __name__ == '__main__':
    app.run(port=8001, host='127.0.0.1',debug=True, use_evalex=False,use_reloader=True)