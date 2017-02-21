# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

import os
import time
import logging


def log_current_date():
    return time.strftime('%Y%m%d')


class MyLogger(object):
    def __init__(self, log='[163news]'):
        self.logger = logging.getLogger(log)
        self.logger.setLevel(logging.DEBUG)
        self.logname = self.init_logsdir()

        fh = logging.FileHandler(self.logname)
        fh.setLevel(logging.ERROR)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def init_logsdir(self):
        program_path = os.path.split(os.path.abspath('.'))[0]
        logspath = os.path.join(program_path, 'logs')
        if not os.path.exists(logspath):
            os.mkdir(logspath)
        return os.path.join(logspath, '{}.log'.format(log_current_date()))


if __name__ == '__main__':
    l = MyLogger()
    l.get_logger().error('xxx123')
    l.get_logger().info('456789')
