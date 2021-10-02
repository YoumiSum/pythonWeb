文件说明：
    youmiWebTools.py                youmiWeb的工具箱
    youmiWeb_dynamicTool.py         youmiWeb对动态路径处理的核心模块
    youmiWeb.py                     youmiWeb的启动类就在这里面，功能：处理普通的静态页面并将动态路径交给youmiWeb_dynamicTool.py进行处理
    youmiWebConfig.py               重要配置文件，对youmiWeb的所有配置都可以在这里进行处理
    linkstart.py                    youmiWeb启动文件
    log.txt                         日志文件，可以在youmiWebConfig.py进行配置

使用说明：
    1. 使用时需要导入youmiWebTools.py、youmiWeb_dynamicTool.py、youmiWeb.py、youmiWebConfig.py、linkstart.py
       这5个文件
    2. 使用示例：
        参考 webhandle/tinyYoumiTest.py

实现功能：微web框架
Python最低版本：3.6
版本：1.0
补丁：暂无
作者：Youmi
联系方式：
    QQ: 1281124008
