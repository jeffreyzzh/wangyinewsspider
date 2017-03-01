# -*- coding: utf-8 -*-
# 2017/2/22 0022
# JEFF

import pymongo
import os
import json
from codes.spider_base import BaseClass
from settings.base_setting import MONGODB


class Datahandler(object):
    def __init__(self, host, port):
        self.logger = BaseClass.getlogger()
        self.client = pymongo.MongoClient(host=host, port=port)
        db = self.client[MONGODB]
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

    def channel_news_count(self, channel):
        return self.coll.get(channel).count()

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            self.logger.error('data is empty')
        channelname = new.get('channelname')
        self.coll.get(channelname).insert(new)
        self.logger.info('coll [{}] insert >> {}'.format(channelname, new))

    def filter_list_by_channel(self, channel):
        remarks = self.coll.get(channel).find({'filter_remark': {'$exists': True}}, {'_id': 1, 'filter_remark': 1})
        # remarks = self.coll.get(channel).find({}, {'filter_remark': 1, '_id': 0})
        filters = list()
        for each in remarks:
            filters.append(each['filter_remark'])
        return filters

    def test_handler_new(self, new):
        filename = self.init_testdir()
        if not new or not isinstance(new, dict):
            self.logger.error('data is empty')
        jsonstr = json.dumps(new, ensure_ascii=False, indent=4)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(jsonstr)
            f.write(',\n')

    def init_testdir(self):
        program_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        logspath = os.path.join(program_path, 'tests')
        if not os.path.exists(logspath):
            os.mkdir(logspath)
        from codes.spider_logger import log_current_date
        return os.path.join(logspath, '{}_data.txt'.format(log_current_date()))


if __name__ == '__main__':
    dh = Datahandler(host='localhost', port=27017)
    # lists = dh.filter_list_by_channel('shehui')
    # print(len(lists))
    print(dh.channel_news_count('tech'))
