import logging
import sys
import re

import lib.youmiWebConfig as youmiWebConfig

from .youmiWebTools import *
from .httpRequest import HttpRequest
from .youmiError import SameParamsError

"""
    路由列表：
    数据结构：
        (path, method, dataType, function)
    示例：("index.html", "POST, "html",  myFun)
    注：如果没有指定method，那么默认为ALL，ALL表示即可以是POST也可以是GET
    注：POST 和 GET 都需要大写
"""
route_list = []


# 定义带有参数的装饰器
# data参数为字典类型，有如下数据：
#   {'path'="该方法的路径", method="POST | GET | ALL",
#     dataType="返回的数据类型，可以参考youmiWebConfig.py"}
def route(path=None, method="ALL", dataType="json"):
    # 装饰器
    def decorator(func):
        nonlocal path, method, dataType

        if path is None:
            print(func, ": need to config path")
            sys.exit(1)

        if path.startswith("/"):
            path = path[1:len(path)]

        if path.endswith("/"):
            path = path[0:len(path)-1]

        route_list.append((path, method, dataType, func))

        def inner():
            result = func()
            return result

        return inner

    # 返回一个装饰器
    return decorator


def urlEqual(httpRequest,  urlPath, item):
    path = item[0]

    if urlPath.endswith("/"):
        urlPath = urlPath[0:len(urlPath)-1]

    urlPath = urlPath.split("/")
    path = path.split("/")

    flag = True

    if len(urlPath) == len(path):
        prog = re.compile("<.*?>")
        for index in range(len(path)):
            item = prog.match(path[index])
            if item is not None:
                item = item.group()
                item = item[1:len(item) - 1]
                if hasattr(httpRequest, item):
                    raise SameParamsError()

                setattr(httpRequest, item, urlPath[index])

                continue

            if path[index] != urlPath[index]:
                flag = False
                break
    else:
        flag = False

    return flag


def handleSub(item, httpVersion, clientSocket, httpRequest):
    retData = item[3](httpRequest)  # 调用fun，获取要返回的数据

    # 如果返回的数据是以.html结尾，说明希望返回的是一个页面
    if retData.endswith(".html"):
        if retData.startswith("/"):
            retData = os.path.join(youmiWebConfig.rootPath, retData[1:len(retData)])
            if sys.platform == "win32":
                retData = retData.replace("\\", "/")
        staticPageSend(clientSocket, retData, httpVersion, httpRequest.cookie)
        return None

    # 如果返回的路径是在路由列表里的，那么也代表返回一个页面
    for it in route_list:
        if urlEqual(httpRequest, retData, it):
            handleSub(it, httpVersion, clientSocket, httpRequest)
            return None

    # 否则按照其指定的数据处理
    headData = httpHeadCreate(httpVersion=httpVersion,
                                            fileType=item[2],
                                            length=len(retData),
                                            cookie=httpRequest.cookie)
    clientSocket.send(headData.encode("utf-8"))
    clientSocket.send(retData.encode("utf-8"))

    return None


def paramsInit(httpRequest: HttpRequest, requestdata: str):
    if (requestdata is None) or requestdata == "":
        return httpRequest

    rdata = requestdata.split("&")

    for item in rdata:
        item = item.split("=")
        if hasattr(httpRequest, item[0]):
            raise SameParamsError()
        setattr(httpRequest, item[0], item[1])

    return httpRequest


def dynamicHandle(method, urlPath, httpVersion, clientSocket, requestdata, cookie):

    httpRequest = HttpRequest()
    httpRequest = paramsInit(httpRequest, requestdata)
    httpRequest.cookie = cookie

    for item in route_list:
        if urlEqual(httpRequest, urlPath, item):
            if method == item[1] or item[1] == "ALL":
                handleSub(item, httpVersion, clientSocket, httpRequest)
                return False
            else:
                # 利用日志打印method不匹配
                logging.info(f"{urlPath}: not match method")

    return True
