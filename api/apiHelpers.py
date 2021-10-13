import os
import sqlite3

def executeSQL(sql: str) -> sqlite3.Connection:
    print(sql)
    
    # changes the current directory to data
    dir = changeDir('data')
    os.chdir(dir)
    
    # connect to database
    conn = sqlite3.connect('database.db')
    cursor = conn.execute(sql)
    # for row in cursor:
    #     print(row)
    return cursor

'''Allows database to be accessed by sister directories'''
def changeDir(sibling: str) -> str:
    # use sister directory to access data- might just want to move this else where
    path = os.path.realpath(__file__)
    # gives the directory where file exists
    dir = os.path.dirname(path)
    dir = dir.replace('api', sibling)
    return dir

def insertSQL(sql: str) -> None:
    # changes the current directory to data
    dir = changeDir('data')
    os.chdir(dir)

    # connect to database
    conn = sqlite3.connect('database.db')
    conn.execute(sql)
    conn.commit()
