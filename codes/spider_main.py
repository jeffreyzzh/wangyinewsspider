# -*- coding: utf-8 -*-
# 2017/2/21 0021
# JEFF

import time
import re
from codes.spider_base import BaseClass
from codes.spider_urlmanager import URLmanager
from codes.spider_downloader import URLdowner
from codes.spider_parser import URLparser
from codes.spider_datahandler import Datahandler
from multiprocessing.dummy import Pool


class SpiderMain(object):
    regex_dict = {
        'channel_name': re.compile(r'//(.*?).163.com', re.S)
    }

    def __init__(self,
                 thread_num,
                 hotcomment_num,
                 newcomment_num,
                 crawl_channels,
                 host,
                 port):
        self.logger = BaseClass.getlogger()
        self.manager = URLmanager(hot_num=hotcomment_num, new_num=newcomment_num)
        self.downloader = URLdowner()
        self.parser = URLparser()
        self.datahandler = Datahandler(host=host, port=port)
        self.crawl_channels = crawl_channels
        self.thread_num = thread_num
        self.hotcomment_num = hotcomment_num
        self.newcomment_num = newcomment_num

    def domain(self):
        channel_dict = self.manager.ajaxdict_by_crawl_channels(self.crawl_channels)
        for k, v in channel_dict.items():
            self.do_by_channel(k, v)

    def do_by_channel(self, channel, urls):
        print('正在抓取频道{}'.format(channel))
        p = Pool(self.thread_num)
        p.map(self.do_by_ajaxurl, urls)
        print('频道抓取完成{}'.format(channel))

    def do_by_ajaxurl(self, url):
        dochannel = re.findall(self.regex_dict['channel_name'], url)
        cont = self.downloader.ajax_fetch(url)
        new_cont = self.parser.parse_ajax_channel(cont, dochannel[0])
        for new in new_cont:
            # 处理评论
            if not new.get('commenturl'):
                self.datahandler.test_handler_new(new)
                continue
            hotc, newc = self.handler_comment(new)
            new['hotcomment'] = hotc
            new['newcomment'] = newc
            # 插入数据库
            self.datahandler.test_handler_new(new)

    def handler_comment(self, new):
        remark = new.get('filter_remark')
        if not remark:
            return None, None
        # 处理热评
        # 处理新评
        return self.handler_hot(remark), self.handler_new(remark)

    def handler_hot(self, remark):
        if self.hotcomment_num <= 0:
            return None
        url = self.manager.hotcomment_ajax_by_filter_remark(remark)
        cont = self.downloader.page_fetch(url)
        comment_info = self.parser.parser_hotcomment(cont, url)
        return comment_info

    def handler_new(self, remark):
        if self.newcomment_num <= 0:
            return None
        url = self.manager.newcomment_ajax_by_filter_remark(remark)
        cont = self.downloader.page_fetch(url)
        comment_info = self.parser.parser_hotcomment(cont, url)
        return comment_info


if __name__ == '__main__':
    starttime = time.time()
    # lists = base_setting.CRAWL_LIST
    lists = ['tech']
    m = SpiderMain(thread_num=4, hotcomment_num=10, newcomment_num=10, crawl_channels=lists, host='localhost',
                   port=27017)
    m.domain()
    print('{0:.6f}'.format(time.time() - starttime))
