create table Cameras 
            (
                cam_id integer primary key,
                cam_name text not null,    
            );

create table Zones 
            (
                zone_id integer primary key,
                zone_name text not null,
                cam_id integer,
                top_left_x integer not null,    
                top_left_y integer not null,
                bot_right_x integer not null,    
                bot_right_y integer not null,
            )

create table Videos
            (
                video_id integer primary key,
                video_name text not null,
                cam_id integer not null, 
                video_path text not null,
            )

CREATE TRIGGER IF NOT EXISTS autoDelete 
    BEFORE DELETE ON Cameras
BEGIN
    DELETE FROM Zones
	WHERE Zones.cam_id = Cameras.cam_id;
    DELETE FROM Videos
	WHERE Videos.cam_id = Cameras.cam_id;
END;