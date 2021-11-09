import pymysql

import lib.databaseConfig as databaseConfig
import conf.log_dict_config as logging

from .databaseMeta import DatabaseMeta


class Database(metaclass=DatabaseMeta):
    conn: pymysql.connect = None

    # you must have databaseInit
    def databaseInit(self):
        self.basename = databaseConfig.database_basename
        logging.logger.info("mysql %s start" % self.basename)
        try:
            self.conn = pymysql.connect(
                host=databaseConfig.database_host,
                port=databaseConfig.database_port,
                user=databaseConfig.database_user,
                password=databaseConfig.database_password,
                database=databaseConfig.database_basename,
                charset=databaseConfig.database_charset
            )
        except:
            self.conn = None
            logging.logger.warning("can't connect to database")
            return None

    # you must have databaseClose
    def databaseClose(self):
        logging.logger.info("mysql %s close" % self.basename)
        if self.conn != None:
            try:
                self.conn.close()
            except:
                logging.logger.error("can't close database")
                return None


    def getConn(self):
        return self.conn


class Cursor(object):
    def __init__(self):
        self.__cursor = Database().getConn().cursor()

    def __del__(self):
        self.__cursor.close()

    def commit(self):
        Database().getConn().commit()

    def rollback(self):
        Database().getConn().rollback()

    def execute(self, sql, *args):
        self.__cursor.execute(sql, args)
