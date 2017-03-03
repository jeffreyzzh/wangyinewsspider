# -*- coding: utf-8 -*-
# 2017/2/21 0021
# JEFF

import time
import re
import sys
import threading
import traceback
import json
from codes.spider_base import BaseClass
from codes.spider_urlmanager import URLmanager
from codes.spider_downloader import URLdowner
from codes.spider_parser import URLparser
from codes.spider_datahandler import Datahandler
from multiprocessing.dummy import Pool

lock = threading.Lock()


class SpiderMain(object):
    regex_dict = {
        'channel_name': re.compile(r'//(.*?).163.com', re.S)
    }

    def __init__(self,
                 thread_num,
                 crawl_delay,
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
        self.crawl_delay = crawl_delay
        self.hotcomment_num = hotcomment_num
        self.newcomment_num = newcomment_num
        self.channel_count = dict()
        self.current_spider_channel = ''

    def domain(self):
        channel_dict = self.manager.ajaxdict_by_crawl_channels(self.crawl_channels)
        for k, v in channel_dict.items():
            try:
                self.do_by_channel(k, v)
            except Exception as e:
                self.logger.error(e)
                self.logger.error(traceback.format_exc())
        self.print_all_spider_info()

    def do_by_channel(self, channel, urls):
        time.sleep(self.crawl_delay)
        start_time = time.time()
        print('开始抓取频道{}'.format(channel))
        self.current_spider_channel = channel
        self.channel_count[channel] = 0
        old_num = self.datahandler.channel_news_count(channel)
        p = Pool(self.thread_num)
        p.map(self.do_by_ajaxurl, urls)
        print()
        print('频道{}抓取完成'.format(channel))
        new_num = self.datahandler.channel_news_count(channel)
        self.channel_count[channel] = {
            '频道': channel,
            '原有新闻数': old_num,
            '现有新闻数': new_num,
            '抓取新闻数': new_num - old_num,
            '用时': '{0:.6f}'.format(time.time() - start_time)
        }

    def do_by_ajaxurl(self, url):
        dochannel = re.findall(self.regex_dict['channel_name'], url)
        cont = self.downloader.ajax_fetch(url)
        new_cont = self.parser.parse_ajax_channel(cont, dochannel[0])
        if not new_cont:
            self.logger.info('url {} parse data is none')
            return
        current_collobject = self.datahandler.coll[self.current_spider_channel]
        filter_list = self.manager.commenturl_filterlist_by_channel(current_collobject)
        for new in new_cont:
            # if not new.get('filter_remark'):
            #     continue
            if new.get('filter_remark') in filter_list:
                continue
            # 线程加锁
            lock.acquire()
            count = self.channel_count[self.current_spider_channel]
            self.test_print_count(count)
            self.channel_count[self.current_spider_channel] = count + 1
            # 线程释放锁
            lock.release()
            # 处理评论
            if not new.get('commenturl'):
                # 无评论插入数据库
                self.datahandler.handler_ajax_new(new)
                continue
            hotc, newc = self.handler_comment(new)
            new['hotcomment'] = hotc
            new['newcomment'] = newc
            # 插入数据库
            self.datahandler.handler_ajax_new(new)

    def test_print_count(self, count):
        print("\r抓取新闻数:", count + 1, end="")
        sys.stdout.flush()

    def handler_comment(self, new):
        remark = new.get('filter_remark')
        if not remark:
            return None, None
        # 处理评论
        return self.handler_hot(remark), self.handler_new(remark)

    def handler_hot(self, remark):
        """
        处理热评
        :param remark: 唯一标识
        :return: 热门评论内容
        """
        if self.hotcomment_num <= 0:
            return None
        url = self.manager.hotcomment_ajax_by_filter_remark(remark)
        cont = self.downloader.page_fetch(url)
        comment_info = self.parser.parser_hotcomment(cont, url)
        return comment_info

    def handler_new(self, remark):
        """
        处理新评
        :param remark:唯一标识
        :return: 新评论内容
        """
        if self.newcomment_num <= 0:
            return None
        url = self.manager.newcomment_ajax_by_filter_remark(remark)
        cont = self.downloader.page_fetch(url)
        comment_info = self.parser.parser_hotcomment(cont, url)
        return comment_info

    def print_all_spider_info(self):
        for each in self.channel_count:
            self.logger.info(self.channel_count[each])
        print('程序10秒后退出')
        time.sleep(10)


if __name__ == '__main__':
    starttime = time.time()
    # lists = base_setting.CRAWL_LIST
    lists = ['tech']
    m = SpiderMain(thread_num=4, crawl_delay=1, hotcomment_num=10, newcomment_num=10, crawl_channels=lists,
                   host='localhost', port=27017)
    m.domain()
    print('{0:.6f}'.format(time.time() - starttime))
