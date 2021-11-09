import time
import os

import lib.youmiWebConfig as youmiWebConfig
import conf.log_dict_config as logging


def httpHeadCreate(httpVersion="HTTP/1.1", fileType=None, cookie=None, length=None, lastModofyTime=None):
    """
    根据指定参数生成http头部信息
    :param httpVersion:         Http的版本号
    :param fileType:            数据类型
    :param length:                 数据的长度，单位字节（byte）
    :param lastModofyTime:      数据的最后一次修改日期，没有可不写
    :return:
    """
    # 拼接第一行
    headData = ' '.join([httpVersion, '200', 'OK'])
    headData += "\r\n"

    # 拼接第二行日期信息
    timeNow = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime(time.time()))
    headData += timeNow
    headData += "\r\n"

    # 拼接第三行服务器信息
    headData += "Server: Youmi\r\n"

    # 拼接跨域允许
    if youmiWebConfig.accessControl:
        headData += "Access-Control-Allow-Origin: *\r\n"
        headData += "Access-Control-Allow-Methods: GET,POST,PUT,DELETE\r\n"
        headData += "Access-Control-Allow-Headers: " \
                    "X-Requested-With,userToken,Content-type,Accept,Version,Timestamp,Platform,Sign\r\n"

    # 拼接文件最后一次修改日期，如果有给的话
    if lastModofyTime != None:
        headData += time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                  time.localtime(lastModofyTime))
        headData += "\r\n"

    # 拼接文件的大小信息
    if length != None:
        headData += "Accept-Ranges: bytes\r\n"
        headData += f"Content-Length: {length}\r\n"

    # 拼接最大连接时长
    headData += "Cache-Control: max-age=86400\r\n"

    # 拼接cookie内容
    if cookie != None:
        headData += f"Set-Cookie: {cookie}\r\n"

    # 拼接持续连接字样
    headData += "Connection: Keep-Alive"

    # 拼接文件类型
    if fileType == None:
        fileType = "default"

    flag = False  # 用于如果找不到文件类型时设置
    for item in youmiWebConfig.contentType:
        if item[0] == fileType:
            fileType = item[1]
            flag = True
            break
    # 如果遍历结束后还是找不到这种类型，就让其等于默认类型
    if not flag:
        fileType = youmiWebConfig.contentType[0][1]

    # 拼接文件类型
    headData += f"Content-Type: {fileType}\r\n"

    # 拼接最后一个\r\n
    headData += "\r\n"

    return headData


def staticPageSend(clientSocket, urlPath, httpVersion="HTTP/1.1", cookie=None):
    """
    静态页面处理方法
    :param clientSocket:    与客户端链接的socket
    :param urlPath:         静态页面的url路径
    :param httpVersion:     http版本，不填默认 HTTP/1.1
    :return:
    """

    # 获取文件的类型信息
    try:
        fileType = urlPath.split('.')
        fileType = fileType[len(fileType) - 1]
        headData = httpHeadCreate(httpVersion=httpVersion,
                                  fileType=fileType,
                                  length=os.stat(urlPath).st_size,
                                  lastModofyTime=os.path.getmtime(urlPath),
                                  cookie=cookie)
        clientSocket.send(headData.encode("utf-8"))
    except FileNotFoundError:
        logging.logger.warning("file not find: %s" % urlPath)
        return None

    try:
        # 打开文件
        file = open(urlPath, mode="rb")
        length = 0
        while True:
            sendData = file.read(1024)
            length += len(sendData)
            if (len(sendData) == 0):
                break
            # 发送数据
            clientSocket.send(sendData)
        file.close()
    except:
        logging.logger.critical("UNKNOWN ERROR!!!")
    finally:
        file.close()


