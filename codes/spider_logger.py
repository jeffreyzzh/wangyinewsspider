# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

import os
import time
import logging


def log_current_date():
    return time.strftime('%Y%m%d')


class MyLogger(object):
    def __init__(self, fileloglevel, streamloglevel, log='[163news]'):
        self.logger = logging.getLogger(log)
        self.logger.setLevel(logging.DEBUG)
        self.logname = self.init_logsdir()
        self.loger_level = {
            5: logging.CRITICAL,
            4: logging.ERROR,
            3: logging.WARNING,
            2: logging.INFO,
            1: logging.DEBUG,
            0: logging.NOTSET
        }
        if fileloglevel in [0, 1, 2, 3, 4, 5]:
            self.filelogleavel = fileloglevel
        else:
            self.filelogleavel = 2

        if streamloglevel in [0, 1, 2, 3, 4, 5]:
            self.streamloglevel = streamloglevel
        else:
            self.streamloglevel = 4

        fh = logging.FileHandler(self.logname)
        fh.setLevel(self.loger_level[self.filelogleavel])

        ch = logging.StreamHandler()
        ch.setLevel(self.loger_level[self.streamloglevel])

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def init_logsdir(self):
        """
        初始化日志文件夹
        :return: None
        """
        program_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        logspath = os.path.join(program_path, 'logs')
        if not os.path.exists(logspath):
            os.mkdir(logspath)
        return os.path.join(logspath, '{}.log'.format(log_current_date()))

    def clean_logs(self):
        """
        清理日志文件夹文件
        :return: None
        """
        pass


if __name__ == '__main__':
    l = MyLogger(2, 4)
    l.get_logger().error('logger.test.error')
    l.get_logger().info('logger.test.info')
