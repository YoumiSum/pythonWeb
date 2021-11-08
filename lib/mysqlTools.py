import pymysql

import lib.databaseConfig as databaseConfig

conn: pymysql.connect = None

def databaseInit():
    global conn
    conn = pymysql.connect(
        host=databaseConfig.database_host,
        port=databaseConfig.database_port,
        user=databaseConfig.database_user,
        password=databaseConfig.database_password,
        database=databaseConfig.database_basename,
        charset=databaseConfig.database_charset
    )


def databaseClose():
    global conn
    conn.close()


class Cursor(object):
    def __init__(self):
        global conn
        self.__cursor = conn.cursor()

    def __del__(self):
        self.__cursor.close()

    def commit(self):
        global conn
        conn.commit()

    def rollback(self):
        global conn
        conn.rollback()

    def execute(self, sql, *args):
        self.__cursor.execute(sql, args)
