import logging

logfile_path = "../log.txt"  # 日志的输出文件

# 定义三种日志输出格式 开始
# format中的配置与含义，见上一篇
standard_format = '[%(asctime)s] [%(threadName)s:%(thread)d] [task_id:%(name)s][%(filename)s:%(lineno)d] ' \
                  '[%(levelname)s] [%(message)s]'

simple_format = '%(filename)s[line:%(lineno)d]: %(asctime)s - %(levelname)s: %(message)s'

id_simple_format = '[%(levelname)s] [%(asctime)s] %(message)s'

# log配置字典
LOGGING_DIC = {
    # 当前日志字典的版本，可以自己随便给
    'version': 1,

    # 是否禁用已经存在的logger实例
    'disable_existing_loggers': False,

    # 定义日志格式化的工具
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'id_simple': {
            'format': id_simple_format
        },
    },

    # 过滤
    'filters': {},

    # 日志的处理方法
    'handlers': {
        # 这里的key可以随便取名，例如我可以将shell改成emmmmmm
        # 但每个key里的内容名字不能瞎改

        # 打印到终端的日志
        'shell': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'file': {
            'level': 'DEBUG',
            # 'class': 'logging.FileHandle',    # 保存到文件
            # 日志轮转技术，关于日志轮转见下方说明
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件路径
            'maxBytes': 1024 * 1024 * 8,  # 轮转日志的大小 8M
            # 备份的数量，如果是公司要求的级别比较高，这个数字就要求大点
            'backupCount': 2048,
            'encoding': 'utf-8',  # 日志文件的编码，解决只能跟随系统下的编码格式问题
        }
    },

    # logger实例
    'loggers': {
        # 这里的key和handlers一样是可以瞎取的，但是同样key里的名字是固定的
        # 此外这里的key值还有一个很重要的属性，那就是在format里的 %(name)s 会将key输出
        # 所以在起key名时，可以根据这个是什么类型的日志进行命名，、如果是默认，那么 %(name)s = root

        # 默认的logger应用如下配置
        # getLogger('loggers_key') 会在这里查找对应的key名，如果没找到，就会使用空key
        # 也就是下面这个
        '': {
            # 日志输出的位置，我们这里即指定了shell也指定了file
            # 那么这样就会即输出到屏幕，也会输出到文件
            # handlers中放的内容来自handlers里的key名
            'handlers': ['shell', 'file'],
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递，即：可以输出更高级别的，但无法输出更低级别的
        }
    },
}


"""
    init log
"""
from logging import config


config.dictConfig(LOGGING_DIC)
logger = logging.getLogger()
