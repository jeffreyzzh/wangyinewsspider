# -*- coding: utf-8 -*-
# 2017/2/21 0021
# JEFF

from codes.spider_base import BaseClass
from codes.spider_urlmanager import URLmanager
from codes.spider_downloader import URLdowner
from codes.spider_parser import URLparser
from settings import base_setting


class SpiderMain(object):
    def __init__(self, thread_num, hotcomment_num=40, newcomment_num=20, crawl_channels=base_setting.CRAWL_LIST):
        self.logger = BaseClass.getlogger()
        self.manager = URLmanager(hot_num=hotcomment_num, new_num=newcomment_num)
        self.downloader = URLdowner()
        self.parse = URLparser()


if __name__ == '__main__':
    m = SpiderMain(thread_num=4)
    # a = m.manager.ajaxdict_by_crawl_channels(channels=base_setting.CRAWL_LIST)
    # for k, v in a.items():
    #     print(k)
    #     print(v)
    #     print()
    # print(len(a))
