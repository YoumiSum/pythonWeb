import re

rootPath = ""       # 项目根目录

serverIP = ""       # 配置服务器的IP地址，不写为本机默认IP
serverPort = 9090   # 服务器的端口号设置
sevrverPool = 1024  # 一次性能接收的最大链接数量
accessControl = False        # 是否开启跨域请求（True | False）
logingFile = "../log.txt"       # 指定日志文件名
indexPage = ".../web/index.html"           # 配置首页，建议不添加"./"，这样可以方便staticPages的配置
nofindPage = "../web/404notFind.html"      # 配置404页面的路径，同indexPage，建议不加"./"

from .mysqlTools import *
initFun = databaseInit
delFun = databaseClose

"""
    动态模块
    所有导入了youmiWeb_dynamicTool模块进行动态处理python文件，都需要写在这里
    注意：写的时候不在.py后缀
    数据结构：不带.py后缀的文件名
        示例：youmiWebTools
"""
dynamicModule = [
    "webhandle.tinyYoumiTest"
]

"""
    能直接访问的静态页面
    即：放行的静态页面
    数据结构：
        从项目根目录开始算起的路径，注意：不要带 ./
        字符串格式
        示例：web/index.html
"""
staticPages = [
    "web/test.html",
    indexPage,
    nofindPage
]

staticPagesProg = re.compile(".*")


"""
    http头部contenType，写在这里方便未来的扩展
    数据结构：
        (文件类型, contentType)
"""
contentType = [
    # 默认的文件类型，必须放在列表的第一位
    ("default", "application/octet-stream"),    # 二进制数据流，常用于文件下载
    ("text", "text/plain"),
    ("html", "text/html"),
    ("js", "text/javascript"),
    ("css", "text/css"),
    ("json", "application/json"),
    ("png", "image/png"),
    ("img", "application/x-img"),
    ("jpg", "image/jpeg"),
    ("jif", "image/gif"),
    ("mp3", "audio/mp3"),
    ("mp4", "video/mpeg4"),
    ("xml", "text/xml"),
    ("htm", "text/html"),
]
