import os
import logging


class Logger_Config(object):
    """ 初始化生成文件目录 """
    log_dir = os.path.join(os.path.abspath("."), "system_logs", )
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger('alter_epidemic_log')  # 创建logging类对象
    logger.setLevel(logging.DEBUG)  # 配置logging对象的默认级别
    """ 创建日志输出格式 可读时间、文件名、打印信息 """
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(funcName)s | 行号：%(lineno)d -> %(message)s')
    file_handler = logging.FileHandler(os.path.join(log_dir, "epidemic_system.log"), encoding='gbk')  # 创建一个写入日志的 epidemic.log 文件
    file_handler.setFormatter(formatter)  # handler对象添加日志输出格式
    file_handler.setLevel(logging.DEBUG)
    terminal_handle = logging.StreamHandler()
    logger.addHandler(file_handler)  # 将logger添加handler对象里面

    def get_logger(self):
        return self.logger  # 将配置好的 logging 对象返回


logger = Logger_Config().get_logger()  # 定义该类的对象，方便直接引用
