# -*- coding: utf-8 -*-
# 2017/2/22 0022
# JEFF

import pymongo
import os
from codes.spider_base import BaseClass


class Datahandler(object):
    def __init__(self, host, port, dbname):
        self.logger = BaseClass.getlogger()
        client = pymongo.MongoClient(host=host, port=port)
        db = client[dbname]
        self.coll = {
            'shehui': db['shehui_coll'],
            'guoji': db['guoji_coll'],
            'guonei': db['guonei_coll'],
            'sports': db['sports_coll'],
            'ent': db['ent_coll'],
            'money': db['money_coll'],
            'tech': db['tech_coll'],
            'lady': db['lady_coll'],
            'edu': db['edu_coll'],
        }

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            self.logger.error('data is empty')
        channelname = new.get('channelname')
        self.coll.get(channelname).insert(new)

    def test_handler_new(self, new):
        filename = self.init_testdir()
        if not new or not isinstance(new, str):
            self.logger.error('data is empty')
        with open(filename, 'a', encoding='gbk') as f:
            f.write(new)

    def init_testdir(self):
        program_path = os.path.split(os.path.abspath('.'))[0]
        logspath = os.path.join(program_path, 'tests')
        if not os.path.exists(logspath):
            os.mkdir(logspath)
        from codes.spider_logger import log_current_date
        return os.path.join(logspath, '{}test.txt'.format(log_current_date()))


if __name__ == '__main__':
    dh = Datahandler(host='localhost', port=27017, dbname='163news')
    lists = dh.coll['guonei'].find({'filter_remark': {'$exists': False}})
    for i in lists:
        print(i)
