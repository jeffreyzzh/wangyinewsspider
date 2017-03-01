# -*- coding: utf-8 -*-
# 2017/2/24
# author = JEFF

import argparse
import pymongo
import sys
from settings.base_setting import CRAWL_LIST
from codes.spider_main import SpiderMain

description = """\
hello world ! :)
"""


def parse_args():
    parses = argparse.ArgumentParser(description=description)

    arg_help = '抓取的频道,可选频道：' \
               'shehui(社会),guonei(国内),guoji(国际),sports(体育),ent(娱乐),' \
               'money(财经),tech(科技),lady(女性),edu(教育) 全频道抓取可输入all'

    parses.add_argument('-l', dest='crawllist', help=arg_help, default='money', type=str)

    parses.add_argument('-n', dest='threadnum', help='抓取的线程数', default=4, type=int)

    parses.add_argument('-d', dest='delay', help='抓取的延迟时间（秒）', default=1.5, type=int)

    parses.add_argument('-hots', dest='hotnum', help='抓取热门评论数', default=40, type=int)

    parses.add_argument('-news', dest='newnum', help='抓取最新评论数', default=20, type=int)

    parses.add_argument('-host', dest='host', help='mongodb的主机地址', default='localhost', type=str)

    parses.add_argument('-port', dest='port', help='mongodb的连接端口', default=27017, type=int)

    return parses.parse_args()


def test_mongo(host, port):
    client = pymongo.MongoClient(host=host, port=port)
    db = client['163news']
    coll = db['test']
    coll.find().count()


if __name__ == '__main__':
    arg = parse_args()
    try:
        test_mongo(host=arg.host, port=arg.port)
    except Exception as e:
        print(e)
        print('未能连接主机：{},端口：{}的数据库，请检查MongoDB相关设置'.format(arg.host, arg.port))
        sys.exit()

    print('抓取的频道', arg.crawllist)
    print('抓取的线程数', arg.threadnum)
    print('抓取的延迟时间', arg.delay)
    print('抓取热门评论数', arg.hotnum)
    print('抓取最新评论数', arg.newnum)
    print('mongodb的主机地址', arg.host)
    print('mongodb的连接端口', arg.port)

    if arg.crawllist != 'all':
        crawls = arg.crawllist.split(',')
        for each in crawls:
            if each not in CRAWL_LIST:
                crawls.remove(each)
    else:
        crawls = CRAWL_LIST
    print('处理列表:', crawls, 'size:', len(crawls))
    spider = SpiderMain(thread_num=arg.threadnum, crawl_delay=arg.delay, hotcomment_num=arg.hotnum,
                        newcomment_num=arg.newnum, crawl_channels=crawls,
                        host=arg.host, port=arg.port)
    spider.domain()
