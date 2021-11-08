import json
from lib.youmiWeb_dynamicTool import route      # 需要导入这个模块

"""
使用说明：
    @route({'path': "abc", 'method': "ALL", 'dataType': "json"}) 数据格式说明
        path: 该方法的路径
        method：POST | GET | ALL，不给默认为ALL，例如下面的返回json示例中就使用了缺省的ALL
        dataType：返回的数据格式，例如json, html，如果不确定，可以不写
                此时如果是普通字符串，将以json数据处理，如果是.html结尾的字符串，将以html处理
                或者返回的路径是包含在你写过的path中的，那么将同样当做路径处理
        注：如果图方便，可以不写method和path，就如同下面所示的最简约写法
        
    方法的说明：
        参数：
            argv = {'parameter': postdata, 'cookie': cookie}
            parameter：用户传递的参数
            cookie：cookie信息
        返回值：
            如果返回的数据不是以.html结尾，那么将直接将数据返回到浏览器
            如果返回的数据以.html结尾，那么表示返回的是一个页面的地址，注意：该地址是从root开始计算的
    
    模块添加：
        每添加一个处理页面，都需要在conf/youmiWebConfig.py中的dynamicModule列表中进行添加
        注意：不能带.py后缀
    
"""

# 注：这种使用方式是不对的，正确的方式是区数据库中查询，因为这个myCookie是全局的，这样其他人也能访问到
# 这里仅仅为了演示示例
myCookie = "123"

# 返回json数据示例
@route(path="abc", dataType="json")
def abcAjax(httpRequest):
    return json.dumps("Hello", ensure_ascii=False)


# 返回一个页面示例
@route(path="abcd", method="POST", dataType="html")
def abcAjax(httpRequest):
    print(httpRequest.name)     # username=youmi&passwd=123

    global myCookie
    httpRequest.cookie = str(myCookie)       # 设置cookie

    return "../web/success.html"

@route(path="getCookie", dataType="json")
def getCookie(httpRequest):

    global myCookie
    # 如果cookie失效，则返回错误页面
    if httpRequest.cookie == None or httpRequest.cookie != myCookie:
        return "web/cookieFail.html"

    return httpRequest.cookie


"""
最简约写法
"""
# 1. 返回一个页面
@route("index")
def getIndex(httpRequest):
    return "/web/index.html"

# 2. 返回json数据
@route("test")
def getHello(httpRequest):
    return "Hello"

# 3. 返回path动态路径
@route("index2")
def getIndex2(httpRequest):
    return "index"

@route("index3/<abc>/<bcd>/abc")
def test3(httpRequest):
    print(httpRequest.abc)
    print(httpRequest.bcd)

    return "index"

