# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

from settings import base_setting
from codes.spider_logger import MyLogger


class BaseClass(object):
    def __init__(self):
        pass

    logger = MyLogger(base_setting.FILELOGLEVEL, base_setting.STREAMLOGLEVEL)

    @staticmethod
    def getlogger():
        return BaseClass.logger.get_logger()


if __name__ == '__main__':
    l = BaseClass.getlogger()
    l.error(';;;;')
