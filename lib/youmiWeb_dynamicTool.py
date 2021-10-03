import logging
import sys

from .youmiWebTools import *

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
def route(data):
    # 装饰器
    def decorator(func):
        try:
            data['path']
        except:
            print(f"path是必须的，位于方法：{func}")
            sys.exit(1)

        # 当执行装饰器的时候就需要把路由添加到路由列表里面,
        # 当装饰函数的时候只添加一次路由即可
        try:
            data['method']
        except:
            data['method'] = "ALL"

        try:
            data['dataType']
        except:
            data['dataType'] = "json"


        route_list.append((data['path'], data['method'], data['dataType'], func))

        def inner():
            result = func()
            return result

        return inner

    # 返回一个装饰器
    return decorator

def handleSub(item, httpVersion, clientSocket, postdata, cookie):
    argv = {'parameter': postdata, 'cookie': cookie}
    retData = item[3](argv)  # 调用fun，获取要返回的数据

    # 如果返回的数据是以.html结尾，说明希望返回的是一个页面
    if retData.endswith(".html"):
        staticPageSend(clientSocket, retData, httpVersion, argv['cookie'])
        return None

    # 如果返回的路径是在路由列表里的，那么也代表返回一个页面
    for it in route_list:
        if retData == it[0]:
            handleSub(it, httpVersion, clientSocket, postdata, argv['cookie'])
            return None

    # 否则按照其指定的数据处理
    headData = httpHeadCreate(httpVersion=httpVersion,
                                            fileType=item[2],
                                            length=len(retData),
                                            cookie=argv['cookie'])
    clientSocket.send(headData.encode("utf-8"))
    clientSocket.send(retData.encode("utf-8"))

    return None


def dynamicHandle(method, urlPath, httpVersion, clientSocket, postdata, cookie):
    flag = False  # 利用flag来处理不存在的页面，以及method不匹配的页面

    for item in route_list:
        if urlPath == item[0]:
            if method == item[1] or item[1] == "ALL":
                handleSub(item, httpVersion, clientSocket, postdata, cookie)
                return None
            else:
                # 利用日志打印method不匹配
                logging.info(f"{urlPath}的method与指定的不匹配")
                flag = False

    if not flag:  # 返回404页面
        staticPageSend(clientSocket, youmiWebConfig.nofindPage, httpVersion)
