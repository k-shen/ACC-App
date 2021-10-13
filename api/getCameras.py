import sqlite3
import apiHelpers as help

def getCameras():
    sql = "SELECT cam_name FROM Cameras;" 
    result = help.executeSQL(sql)
    # note- printing will move the cursor through the whole db and make it empty
    # for row in result:
    #     print(row)
    return list(result)

print(getCameras())