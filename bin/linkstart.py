import os
import re
import configparser
import sys

import lib.mysqlTools
import lib.youmiWebConfig as youmiWebConfig
import lib.databaseConfig as databaseConfig
import conf.log_dict_config as logging

from lib.youmiWeb import YoumiHttpServer

databaseList = [{"name": "None",
                 "func": None,
                 },
                {"name": "mysql",
                "func": lib.mysqlTools.Database(),
                 }
                ]


def init():
    # config web server base
    youmiWebConfig.rootPath = os.path.abspath("..")
    if sys.platform == "win32":
        youmiWebConfig.rootPath = youmiWebConfig.rootPath.replace("\\", "/")
    youmiwebConfigPath = os.path.join(youmiWebConfig.rootPath, "conf", "youmiweb_config.ini")
    if sys.platform == "win32":
        youmiwebConfigPath = youmiwebConfigPath.replace("\\", "/")
    config = configparser.ConfigParser()
    config.read(youmiwebConfigPath)

    youmiWebConfig.serverIP = config.get("webserver-base", "host")
    youmiWebConfig.serverPort = config.getint("webserver-base", "port")
    youmiWebConfig.accessControl = config.getboolean("webserver-base", "accessControl")

    indexPage = config.get("webserver-base", "indexPage")
    if indexPage == "None":
        youmiWebConfig.indexPage = None
    else:
        indexPage = indexPage.split("/")
        if not len(indexPage[0]):
            indexPage[0] = youmiWebConfig.rootPath
        for index in range(len(indexPage)):
            if index != 0:
                indexPage[0] = os.path.join(indexPage[0], indexPage[index])
        youmiWebConfig.indexPage = indexPage[0]
        if sys.platform == "win32":
            youmiWebConfig.indexPage = youmiWebConfig.indexPage.replace("\\", "/")

    nofindPage = config.get("webserver-base", "404Page")
    if nofindPage == "None":
        youmiWebConfig.nofindPage = None
    else:
        nofindPage = nofindPage.split("/")
        if not len(nofindPage[0]):
            nofindPage[0] = youmiWebConfig.rootPath
        for index in range(len(nofindPage)):
            if index != 0:
                nofindPage[0] = os.path.join(nofindPage[0], nofindPage[index])
        youmiWebConfig.nofindPage = nofindPage[0]
        if sys.platform == "win32":
            youmiWebConfig.nofindPage = youmiWebConfig.nofindPage.replace("\\", "/")


    # config web server extern
    def subTool(partenList):
        temp = ""
        prog = re.compile("<.*?>")
        for item in partenList:
            item = item.strip()
            item = item.replace(".", "\\.")
            item = item.replace("*", "\\*")
            patterns = prog.finditer(item)
            item = list(item)
            for pattern in patterns:
                it = pattern.group()
                it = it[1:len(it)-1]
                it = it.replace("\\.", ".")
                it = it.replace("\\*", "*")
                item[pattern.span()[0]] = it
                index = pattern.span()[0] + 1
                while index < pattern.span()[1]:
                    item[index] = ''
                    index += 1
            item = ''.join(item)
            item = "^" + item + "$"
            temp += "|"
            temp += item
        return re.compile(temp[1:len(temp)])

    # config static pages
    partenList = config.get("webserver-extern", "staticPages")
    partenList = partenList[1:len(partenList) - 1]
    partenList = partenList.split("\n")
    partenList = ''.join(partenList)
    partenList = partenList.split(',')
    for index in range(len(partenList)):
        if partenList[index].startswith("/"):
            partenList[index] = partenList[index][1:len(partenList[index])]
    youmiWebConfig.staticPagesProg = subTool(partenList)

    # config dynamicModule
    partenList = config.get("webserver-extern", "dynamicPages")
    partenList = partenList[1:len(partenList) - 1]
    partenList = partenList.split("\n")
    partenList = ''.join(partenList)
    partenList = partenList.split(',')
    basePath = youmiWebConfig.rootPath.replace("\\", "\\\\")
    for index in range(len(partenList)):
        if partenList[index].startswith("/"):
            partenList[index] = partenList[index][1:len(partenList[index])]
            partenList[index] = '/'.join([youmiWebConfig.rootPath, partenList[index]])
    dynamicModuleProg = subTool(partenList)
    dynamicModules = []

    for lst in os.walk(youmiWebConfig.rootPath):
        for file in lst[2]:
            path = os.path.join(lst[0], file)
            if sys.platform == "win32":
                path = path.replace("\\", "/")
            if dynamicModuleProg.match(path) is not None:
                dynamicModules.append(path[len(youmiWebConfig.rootPath):len(path)])

    for index in range(len(dynamicModules)):
        if dynamicModules[index].startswith("/"):
            dynamicModules[index] = dynamicModules[index][1:len(dynamicModules[index])]

        if dynamicModules[index].endswith(".py"):
            dynamicModules[index] = dynamicModules[index][0:len(dynamicModules[index])-3]

        dynamicModules[index] = dynamicModules[index].replace("/", ".")

    youmiWebConfig.dynamicModule = dynamicModules


    # config database
    def initSub_database(section):
        try:
            databaseConfig.database_host = config.get(section, "host")
            databaseConfig.database_port = config.getint(section, "port")
            databaseConfig.database_user = config.get(section, "user")
            databaseConfig.database_password = config.get(section, "password")
            databaseConfig.database_basename = config.get(section, "basename")
            databaseConfig.database_charset = config.get(section, "charset")
        except:
            logging.logger.warning("don't have database")

        database = config.get(section, "database")
        global databaseList
        for item in databaseList:
            if item["name"] == database:
                youmiWebConfig.functions.append(item["func"])
                if youmiWebConfig.functions[-1] is not None:
                    youmiWebConfig.functions[-1].databaseInit()
                break


    databases = re.compile("^\[database.*\]$")
    sections = []
    with open(youmiwebConfigPath, "r") as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            line = line.strip()
            section = databases.match(line)
            if section is not None:
                sections.append(section.group()[1:len(section.group())-1])

    for section in sections:
        initSub_database(section)




if __name__ == '__main__':
    init()
    YoumiHttpServer().start()


