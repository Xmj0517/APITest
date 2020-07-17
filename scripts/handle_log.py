import logging
import os

from scripts.handle_yaml import do_yaml
# 导入日志文件的存放目录
from scripts.handle_path import LOGS_DIR

class HandleLogger(object):

    @classmethod
    def create_logger(cls):
        my_log = logging.getLogger(do_yaml.read_yaml('log', 'log_name'))
        my_log.setLevel(do_yaml.read_yaml('log', 'logger_level'))

        # 创建输出格式
        formatter = logging.Formatter(do_yaml.read_yaml('log', 'log_formatter'))

        # 创建到控制台的输出渠道
        stream = logging.StreamHandler()
        stream.setLevel(do_yaml.read_yaml('log', 'stream_levle'))
        stream.setFormatter(formatter)

        my_log.addHandler(stream)

        # 创建到文件的输出渠道，文件目录和配置文件中的文件名进行拼接
        filer = logging.FileHandler(filename=os.path.join(LOGS_DIR, do_yaml.read_yaml('log', 'logfile_name')),
                                    encoding='utf8')
        filer.setLevel(do_yaml.read_yaml('log', 'logfile_level'))
        filer.setFormatter(formatter)

        my_log.addHandler(filer)

        return my_log


do_log = HandleLogger.create_logger()

