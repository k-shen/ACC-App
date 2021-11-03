import sqlite3 as sqlite
import flask
from flask.helpers import url_for
from scripts.Camera import *
from scripts.Video import Video
from flask import request
import os
from scripts.get_frame import *


app = flask.Flask(__name__, static_folder='')
UPLOAD_FOLDER = './data/videos'
SS_FOLDER = './data/cam_screen'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SS_FOLDER'] = SS_FOLDER

@app.route('/')
def home():
    return flask.redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
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
    cam = Camera(data[0], data[1], [])
    
    return cam

def getImgFromCam(cam):
    cname = cam.name.replace(' ', '')
    img_src = '/' + app.config['SS_FOLDER'] + '/' + cname + '_img.jpg'
    print(img_src)
    print(os.path.exists(img_src[1:]))
    return img_src

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
    massDeleteVideo(idToDelete)
    cname = c.execute("select cam_name from Cameras where cam_id=?",(idToDelete,)).fetchone()[0]
    ci_name = cname.replace(' ', '') + "_img.jpg"
    ci_path = os.path.join(app.config['SS_FOLDER'], ci_name)
    try: 
        os.remove(ci_path)
    except:
        FileNotFoundError()
    c.execute("delete from Cameras where cam_id=?",(idToDelete,))
    conn.commit()
    conn.close()

    print("deleted camera id " + str(cid))
    return flask.redirect(url_for('home'))

def massDeleteVideo(cid):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    videos = (c.execute("select video_id from Videos where cam_id=?",(cid,)).fetchall())
    print(videos)
    for i in videos:
        vname = c.execute("select video_name from Videos where video_id=?",(i[0],)).fetchone()[0]
        
        ci_name = vname.replace(' ', '')
        ci_path = os.path.join(app.config['UPLOAD_FOLDER'], ci_name)
        try: 
            os.remove(ci_path)
        except:
            FileNotFoundError()

@app.route('/vid/<vid>/delete', methods=['POST'])
def deleteVid(vid):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    idToDelete = request.form['vid']
    vname = c.execute("select video_name from Videos where video_id=?",(idToDelete,)).fetchone()[0]
    ci_name = vname.replace(' ', '')
    ci_path = os.path.join(app.config['UPLOAD_FOLDER'], ci_name)
    try: 
        os.remove(ci_path)
    except:
        FileNotFoundError()
    c.execute("delete from Videos where video_id=?",(idToDelete,))
    conn.commit()
    conn.close()

    print("deleted video id " + str(vid))
    cid = request.form['cid']
    return flask.redirect('/cam/{}'.format(cid))

@app.route('/zone/<zid>/delete', methods=['POST'])
def deleteZone(zid):
    #connect to data base
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    idToDelete = request.form['zid']
    c.execute("delete from Zones where zone_id=?",(idToDelete,))
    conn.commit()
    conn.close()

    print("deleted zone id " + str(zid))
    cid = request.form['cid']
    return flask.redirect('/cam/{}'.format(cid))

@app.route('/cam/<cid>', methods=['GET', 'POST'])
def viewCam(cid):
    #connect to data base
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam = loadCameraObj(cid)
    v_details = (c.execute("select * from Videos where cam_id=?",(cid,)).fetchall())
    z_details = (c.execute("select * from Zones where cam_id=?",(cid,)).fetchall())
    conn.commit()
    conn.close()

    videos = []
    zones = []
    for v in v_details:
        videos.append(loadVideoObj(v))
    for z in z_details:
        zones.append(loadZoneObj(z))

    return flask.render_template('camera.html', cam=cam, vdata=videos, zdata=zones)

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
    vname = flask.request.form['vname'].replace(' ', '')
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

@app.route("/addCamera/drawbox", methods=['GET', "POST"])
def addVideoDrawbox():
    video = flask.request.files['videofile']
    vname = flask.request.form['vname']
    cname = flask.request.form['cname']
    vname_format = vname.replace(' ', '')
    cname_format = cname.replace(' ', '')
    vpath = os.path.join(app.config['UPLOAD_FOLDER'], vname_format)
    ci_name = cname_format.replace(' ', '') + "_img.jpg"
    ci_path = os.path.join(app.config['SS_FOLDER'], ci_name)
    video.save(vpath)
    get_image(vpath, ci_path)
    print(vpath, ci_path)
    
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    c.execute('insert into Cameras (cam_name) values (?);', (cname,))
    cid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
    print(cid, vname, vpath)
    c.execute("INSERT INTO Videos (video_name, cam_id, video_path) VALUES (?, ?, ?);", \
        (vname, cid, vpath))
    c.execute('insert into Zones (zone_name, cam_id, top_left_x, top_left_y, bot_right_x, bot_right_y) values (?, ?, ?, ?, ?, ?);', \
    ('Entire', cid, 0, 0, 0, 0 ))
    c.execute('insert into Zones (zone_name, cam_id, top_left_x, top_left_y, bot_right_x, bot_right_y) values (?, ?, ?, ?, ?, ?);', \
        ('Enter Zone Name', cid, 0, 0, 0, 0 ))
    zid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.commit()
    conn.close()

    return flask.redirect(url_for('drawZone', cid=cid, zid=zid, zname='Enter Zone Name', img_src='None'))

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

@app.route("/cam/<cid>/addZone", methods=['GET', "POST"])
def addZone(cid):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam_info = (c.execute("select * from Cameras where cam_id=?",(cid,)).fetchone())
    c.execute('insert into Zones (zone_name, cam_id, top_left_x, top_left_y, bot_right_x, bot_right_y) values (?, ?, ?, ?, ?, ?);', \
        ('Enter Zone Name', cid, 0, 0, 0, 0))
    zid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
    print(zid)
    conn.commit()
    conn.close()
    return flask.redirect(url_for('drawZone', cid=cid, zid=zid, zname='Enter Zone Name', img_src='None'))

@app.route("/cam/<cid>/<zid>/redraw/<img_src>", methods=['GET', "POST"])
def drawZone(cid, zid, img_src):
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    cam_info = (c.execute("select * from Cameras where cam_id=?",(cid,)).fetchone())
    cam = loadTempCamera(cam_info)
    if (img_src == 'None'):
        img_src = getImgFromCam(cam)
        print(img_src)
    zname = (c.execute("select zone_name from Zones where zone_id=?", (zid,)).fetchone())
    print(zname)
    conn.commit()
    conn.close()
    return flask.render_template('image.html', cam=cam, zid=zid, zname=zname[0], img_src=img_src)

@app.route("/cam/<cid>/<zid>/redraw/success", methods=['GET', "POST"])
def drawZoneSuccess(cid, zid):
    top_left_x = flask.request.form['tlx']
    top_left_y = flask.request.form['tly']
    bot_right_x = flask.request.form['brx']
    bot_right_y = flask.request.form['bry']
    zname = flask.request.form['zname']
    print(top_left_x, top_left_y, bot_right_x, bot_right_y)
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    c.execute("update Zones set zone_name = ?, top_left_x = ?, top_left_y = ?, bot_right_x = ?, bot_right_y = ? where zone_id =?",(zname, top_left_x, top_left_y, bot_right_x, bot_right_y, zid,))
    conn.commit()
    conn.close()
    return flask.redirect('/cam/{}'.format(cid))


@app.route("/cam/<cid>/draw_success", methods=['GET', "POST"])
def redrawSuccess(cid):
    zname = flask.request.form['zname']
    top_left_x = flask.request.form['top_left_x']
    top_left_y = flask.request.form['top_left_y']
    bot_right_x = flask.request.form['bot_right_x']
    bot_right_y = flask.request.form['bot_right_y']
    conn = sqlite.connect('./data/database.db')
    c = conn.cursor()
    c.execute('insert into Zones (zone_name, cam_id, top_left_x, top_left_y, bot_right_x, bot_right_y) values (?, ?, ?, ?, ?, ?);', \
        (zname, cid, top_left_x, top_left_y, bot_right_x, bot_right_y))
    conn.commit()
    conn.close()

    return flask.redirect('/cam/{}'.format(cid))

if __name__ == '__main__':
    app.run(port=8001, host='127.0.0.1',debug=True, use_evalex=False,use_reloader=True)