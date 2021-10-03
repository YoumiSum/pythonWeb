import platform
import socket
import threading
import sys
import os
import signal
import logging

import _youmiWebConfig
import youmiWebTools
import youmiWeb_dynamicTool

# 设置日志等级和输出日志格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename=_youmiWebConfig.logingFile,
                    filemode="a")


class YoumiHttpServer(object):

    def sigINT_handel(self, signum, frame):
        """
        INT信号（ctrl+c）处理函数
        :param signum:
        :param frame:
        :return:
        """
        # 1. 关闭tcp链接
        self.tcpServer.close()

        # 2. 执行用户关闭函数
        if _youmiWebConfig.delFun != None:
            _youmiWebConfig.delFun()

        # 3. 打印结束信息并退出
        logging.info("YoumiWebServer关闭")
        print("\n晚安，主人(*^▽^*)")
        sys.exit(0)

    def __init__(self):
        # 0. 其它初始化操作
        # 0.1 初始化信号量处理程序
        signal.signal(signal.SIGINT, self.sigINT_handel)
        signal.signal(signal.SIGTERM, self.sigINT_handel)

        # 0.2 动态导入dynamicModule
        for item in _youmiWebConfig.dynamicModule:
            __import__(item, fromlist=True)

        if _youmiWebConfig.initFun != None:
            _youmiWebConfig.initFun()

        # 1. 创建套接字文件
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. 设置端口复用
        # setsockopt(level, optname, value)
        # level：选项所在的协议层。
        #       SOL_SOCKET      socket层面
        #       IPPROTO_TCP     TCP层面
        # optname：需要访问的选项名。
        #       SO_REUSEADDR：允许套接口和一个已在使用中的地址捆绑
        #       更多见本文件的底部--附录--
        # value：设置的值
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        # 3. 端口绑定
        self.tcpServer.bind((_youmiWebConfig.serverIP, _youmiWebConfig.serverPort))

        # 4. 监听等待
        self.tcpServer.listen(_youmiWebConfig.sevrverPool)  # 设置一次性能开启的socket数量为1024

    def handle(self, clientSocket, IPPort):
        """
        客户端服务请求处理方法
        :param clientSocket:    客户端链接socket
        :param IPPort:          客户端的IP和端口信息
        :return:
        """
        # 1. 获取客户端请求信息
        try:
            recvData = clientSocket.recv(4096).decode("utf-8")
            if recvData.strip() == "":
                clientSocket.close()
                return None
        except:
            clientSocket.close()
            return None

        recvData = recvData.split("\r\n")

        # 2. 获取客户端请求信息的第一行和最后一行
        # 2.1 注：get方法只需要第一行
        # 2.2 post方法还需要最后一行传递进来的数据
        firstLine = recvData[0]
        firstLine = firstLine.split(" ")  # 示例数据：['GET', '/web/test.html', 'HTTP/1.1']
        lastLine = recvData[len(recvData) - 1]  # 示例数据：username=0313021803501&passwd=123456
        method, urlPath, httpVersion = firstLine  # 解包
        # 获取cookie信息，如果有的话
        cookie = None
        for item in recvData:
            if item.startswith("Cookie"):
                cookie = item.split(" ")[1]
                break

        # 2.1 去除urlPath的第一个斜杠
        urlPath = list(urlPath)
        urlPath.pop(0)
        urlPath = ''.join(urlPath)
        # 2.1 去除get中带?请求数据
        urlPath = urlPath.split('?')
        # 2.2 拼接get方式的数据
        if len(urlPath) >= 2:
            if lastLine == "":
                lastLine += urlPath[1]
            else:
                lastLine = lastLine + "&" + urlPath[1]
        # 2.3 只留下url
        urlPath = urlPath[0]


        if urlPath in [item[0] for item in youmiWeb_dynamicTool.route_list]:
            """ 动态页面处理 """
            youmiWeb_dynamicTool.handle(method, urlPath, httpVersion, clientSocket, lastLine, cookie)
        else:
            """ 静态页面处理 """
            # 配置首页
            if urlPath == "":
                urlPath = _youmiWebConfig.indexPage

            # 如果是html，则判断该资源是否能被放行
            if urlPath.endswith(".html"):
                if urlPath not in _youmiWebConfig.staticPages:
                    urlPath = _youmiWebConfig.nofindPage

            # 判断文件是否存在
            if not os.path.exists(urlPath):
                urlPath = _youmiWebConfig.nofindPage

            # 调用静态页面处理函数处理
            youmiWebTools.staticPageSend(clientSocket, urlPath, httpVersion)

        # 关闭客户端socket链接
        clientSocket.close()

    def start(self):
        """
        程序入口
        :return:
        """
        print("起床很累的o(╥﹏╥)o")
        logging.info("YoumiWebServer启动")
        while True:
            # 1. 接收等待客户端的链接
            clientSocket, IPPort = self.tcpServer.accept()

            # 2. 创建一个线程来专门处理客户端请求
            t = threading.Thread(target=self.handle, args=(clientSocket, IPPort))
            t.setDaemon(True)  # 设置为守护线程，让操作系统自行管理
            t.start()  # 客户端请求处理线程启动
