# -*- coding: utf-8 -*-
# 2017/2/21 0021
# JEFF

import time
import re
from codes.spider_base import BaseClass
from codes.spider_urlmanager import URLmanager
from codes.spider_downloader import URLdowner
from codes.spider_parser import URLparser
from settings import base_setting
from multiprocessing.dummy import Pool


class SpiderMain(object):
    regex_dict = {
        'channel_name': re.compile(r'//(.*?).163.com', re.S)
    }

    def __init__(self,
                 thread_num,
                 hotcomment_num,
                 newcomment_num,
                 crawl_channels):
        self.logger = BaseClass.getlogger()
        self.manager = URLmanager(hot_num=hotcomment_num, new_num=newcomment_num)
        self.downloader = URLdowner()
        self.parser = URLparser()
        self.crawl_channels = crawl_channels
        self.thread_num = thread_num

    def domain(self):
        channel_dict = m.manager.ajaxdict_by_crawl_channels(self.crawl_channels)
        for k, v in channel_dict.items():
            self.do_by_channel(k, v)

    def do_by_channel(self, channel, urls):
        print('正在爬取频道{}'.format(channel))
        p = Pool(self.thread_num)
        p.map(self.do_by_ajaxurl, urls)

    def do_by_ajaxurl(self, url):
        dochannel = re.findall(self.regex_dict['channel_name'], url)
        cont = self.downloader.ajax_fetch(url)
        new_cont = self.parser.parse_ajax_channel(cont, dochannel[0])
        print(new_cont)


if __name__ == '__main__':
    starttime = time.time()
    # lists = base_setting.CRAWL_LIST
    lists = ['tech']
    m = SpiderMain(thread_num=4, hotcomment_num=40, newcomment_num=20, crawl_channels=lists)
    m.domain()
    print('{0:.6f}'.format(time.time() - starttime))
