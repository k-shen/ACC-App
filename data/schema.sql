/*create table Cameras 
            (
                cam_id integer primary key,
                cam_name text not null    
            );

create table Zones 
            (
                zone_id integer primary key,
                zone_name text not null,
                cam_id integer,
                top_left_x integer not null,    
                top_left_y integer not null,
                bot_right_x integer not null,    
                bot_right_y integer not null
            );

create table Videos
            (
                video_id integer primary key,
                video_name text not null,
                cam_id integer not null, 
                video_path text not null
            );

create table Frames
            (
                frame_id integer primary key,
                frame_num integer not null,
                video_id integer not null,
                cam_id integer not null,
                zone_id integer not null,
                time_stamp timestamp not null,
                person text
            );

*/
CREATE TRIGGER IF NOT EXISTS autoDeleteCamera
    BEFORE DELETE ON Cameras
BEGIN
    DELETE FROM Zones
	WHERE Zones.cam_id = old.cam_id;
    DELETE FROM Videos
	WHERE Videos.cam_id = old.cam_id;
    DELETE FROM Frames
	WHERE Frames.cam_id = old.cam_id;
END;

CREATE TRIGGER IF NOT EXISTS autoDeleteVideo 
    BEFORE DELETE ON Videos
BEGIN
    DELETE FROM Frames
	WHERE Frames.video_id = old.video_id;
END;