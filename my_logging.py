import os
import  time
import logging.config
#函数上面部分要根据你程序进行修改
# 定义三种日志输出格式 开始
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getLogger()指定的名字；lineno为调用日志输出函数的语句所在的代码行
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
basic_format = '[%(levelname)s][%(asctime)s] %(message)s'
# 定义日志输出格式 结束

logfile_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # log文件的目录，需要自定义文件路径 # atm
# logfile_dir = os.path.join(logfile_dir, 'log')  # C:\Users\oldboy\Desktop\atm\log
logfile_dir = r"J:\PlayGround\CVP"
logfile_name = 'log.log'  # log文件名，需要自定义路径名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):  # C:\Users\oldboy\Desktop\atm\log
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)  # C:\Users\oldboy\Desktop\atm\log\log.log
# 定义日志路径 结束

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'basic': {
            'format': basic_format
        },
    },
    'filters': {},  # filter可以不定义
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M  (*****)
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置。如果''设置为固定值logger1，则下次导入必须设置成logging.getLogger('logger1')
        '': {
            # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False,  # 向上（更高level的logger）传递
        },
    },
}
LOGGING_DIC_DEV = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'basic': {
            'format': basic_format
        },
    },
    'filters': {},  # filter可以不定义
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'basic'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M  (*****)
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置。如果''设置为固定值logger1，则下次导入必须设置成logging.getLogger('logger1')
        '': {
            # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False,  # 向上（更高level的logger）传递
        },
    },
}
DO_NOT_DEBUG= {#屏蔽当前文件
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'basic': {
            'format': basic_format
        },
    },
    'filters': {},  # filter可以不定义
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'basic'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M  (*****)
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置。如果''设置为固定值logger1，则下次导入必须设置成logging.getLogger('logger1')
        '': {
            # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False,  # 向上（更高level的logger）传递
        },
    },
}

#函数部分记录的东西可以修改一下
def load_my_logging_cfg(model):
    if model is None:
        #model可选LOGGING_DIC与LOGGING_DIC_DEV与DO_NOT_DEBUG
        logging.config.dictConfig(LOGGING_DIC_DEV)  # 导入上面定义的logging配置
        logger = logging.getLogger(__name__)  # 生成一个log实例
        logger.info('---------MODEL: DEBUG-----------')  # 记录该文件的运行状态可以自己修改
    else :
        #model可选LOGGING_DIC与LOGGING_DIC_DEV与DO_NOT_DEBUG
        logging.config.dictConfig(DO_NOT_DEBUG)  # 导入上面定义的logging配置
        # logger = logging.getLogger(__name__)  # 生成一个log实例
        # logger.info('---------MODEL: DO_NOT_DEBUG-----------')  # 记录该文件的运行状态可以自己修改


if __name__ == '__main__':
    logger = logging.getLogger(__name__)  # 生成logger实例
    # my_logging.load_my_logging_cfg()  # 在你程序文件的入口加载自定义logging配置

    def demo():
        logger.debug("start range... time:{}".format(time.time()))
        logger.info("中文测试开始。。。")
        for i in range(10):
            logger.debug("i:{}".format(i))
            time.sleep(0.2)
        else:
            logger.debug("over range... time:{}".format(time.time()))
        logger.info("中文测试结束。。。")
    # my_logging.load_my_logging_cfg()  # 在你程序文件的入口加载自定义logging配置

    load_my_logging_cfg()
    demo()
