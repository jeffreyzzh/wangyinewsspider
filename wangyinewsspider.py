# -*- coding: utf-8 -*-
# 2017/2/24
# author = JEFF

import argparse
from settings.base_setting import CRAWL_LIST
from codes.spider_main import SpiderMain

description = """\
您好，欢迎使用。\r\n
如果有任何的建议，可以给我邮件\r\n
124303687@qq.com\r\n
如果喜欢本项目，please fork or star! thx!
"""


def parse_args():
    parses = argparse.ArgumentParser(description=description)

    parses.add_argument('-n', dest='threadnum', help='抓取的线程数', default=4, type=int)

    parses.add_argument('-list', dest='crawllist', help='抓取的频道', default=CRAWL_LIST, type=list)

    parses.add_argument('-hots', dest='hotnum', help='抓取热门评论数', default=40, type=int)

    parses.add_argument('-news', dest='newnum', help='抓取最新评论数', default=20, type=int)

    parses.add_argument('-host', dest='host', help='mongodb的主机地址', default='localhost', type=str)

    parses.add_argument('-port', dest='port', help='mongodb的连接端口', default=27012, type=int)

    return parses.parse_args()


if __name__ == '__main__':
    arg = parse_args()
    print('抓取的线程数', arg.threadnum)
    print('抓取的频道', arg.crawllist)
    print('抓取热门评论数', arg.hotnum)
    print('抓取最新评论数', arg.newnum)
    print('mongodb的主机地址', arg.host)
    print('mongodb的连接端口', arg.port)
    # SpiderMain(arg.threadnum, arg.hotnum, arg.newnum, arg.crawllist, arg.host, arg.port)
