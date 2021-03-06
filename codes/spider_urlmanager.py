# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

import re


class URLmanager(object):
    def __init__(self, hot_num, new_num):
        self.hotcomment_num = hot_num
        self.newcomment_num = new_num

    regex_dict = {
        'filter_remark': re.compile('bbs/(.*?)\.html')
    }

    CRAWL_URLS = {
        'shehui': {
            'channels': ['shehui'],
            'ajax_url': 'http://temp.163.com/special/00804KVA/cm_{}.js',
            'ajax_urls': 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js',
            'max': 8,
            'description': '普通频道，3个子频道：社会，国际，国内'
        },
        'guoji': {
            'channels': ['guoji'],
            'ajax_url': 'http://temp.163.com/special/00804KVA/cm_{}.js',
            'ajax_urls': 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js',
            'max': 8,
            'description': '普通频道，3个子频道：社会，国际，国内'
        },
        'guonei': {
            'channels': ['guonei'],
            'ajax_url': 'http://temp.163.com/special/00804KVA/cm_{}.js',
            'ajax_urls': 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js',
            'max': 8,
            'description': '普通频道，3个子频道：社会，国际，国内'
        },
        'sports': {
            'channels': ['index', 'allsports', 'cba', 'nba', 'china', 'world'],
            'ajax_url': 'http://sports.163.com/special/000587PR/newsdata_n_{}.js',
            'ajax_urls': 'http://sports.163.com/special/000587PR/newsdata_n_{}_0{}.js',
            'extra_urls': ['http://sports.163.com/special/000587PR/newsdata_n_index_10.js'],
            'max': 5,
            'description': '体育频道，6个子频道：首页，热点，CBA，NBA，国足，世界足球'
        },
        'ent': {
            'channels': ['index', 'star', 'movie', 'tv', 'show', 'music'],
            'ajax_url': 'http://ent.163.com/special/000380VU/newsdata_{}.js',
            'ajax_urls': 'http://ent.163.com/special/000380VU/newsdata_{}_0{}.js',
            'max': 8,
            'description': '娱乐频道，6个子频道：首页，明星，电影，电视剧，综艺，音乐'
        },
        'money': {
            'channels': ['index', 'stock', 'chanjing', 'finance', 'fund', 'licai', 'biz'],
            'ajax_url': 'http://money.163.com/special/002557S5/newsdata_idx_{}.js',
            'ajax_urls': 'http://money.163.com/special/002557S5/newsdata_idx_{}_0{}.js',
            'max': 8,
            'description': '财经频道，7个子频道：首页，股票，产经，金融，基金，理财，商业'
        },
        'tech': {
            'channels': ['datalist'],
            'ajax_url': 'http://tech.163.com/special/00097UHL/tech_{}.js',
            'ajax_urls': 'http://tech.163.com/special/00097UHL/tech_{}_0{}.js',
            'max': 3,
            'description': '科技频道'
        },
        'lady': {
            'channels': ['fashion', 'sense', 'travel', 'art', 'edu', 'baby'],
            'ajax_url': 'http://lady.163.com/special/00264OOD/data_nd_{}.js',
            'ajax_urls': 'http://lady.163.com/special/00264OOD/data_nd_{}_0{}.js',
            'max': 5,
            'description': '女性频道，6个子频道：时尚，情爱，旅游，艺术，教育，亲子'
        },
        'edu': {
            'channels': ['hot', 'liuxue', 'yimin', 'en', 'daxue', 'gaokao'],
            'ajax_url': 'http://edu.163.com/special/002987KB/newsdata_edu_{}.js',
            'ajax_urls': 'http://edu.163.com/special/002987KB/newsdata_edu_{}_0{}.js',
            'max': 3,
            'description': '教育频道，6个子频道：热点，留学，移民，外语，校园，高考'
        },

    }

    URL = 'http://news.163.com/shehui/'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit={}'
    NEW_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/newList?limit={}'

    def ajaxdict_by_crawl_channels(self, channels):
        """
        对普通新闻做特殊处理，每个子频道是一个独立的存储dict，
        其他的大频道对应一个存储dict
        :param channels: 频道列表
        :return: ajax_list_dict
        """
        result = dict()
        if not channels:
            return result
        for channel in channels:
            return_list = list()
            channelinfo = self.CRAWL_URLS.get(channel)
            if not channelinfo:
                continue
            child_channels = channelinfo.get('channels')
            maxtimes = channelinfo.get('max')
            ajax_url = channelinfo.get('ajax_url')
            ajax_urls = channelinfo.get('ajax_urls')
            for x in child_channels:
                return_list.append(ajax_url.format(x))
                for y in range(2, maxtimes + 1):
                    return_list.append(ajax_urls.format(x, y))
            result[channel] = return_list
        return result

    def hotcomment_ajax_by_commenturl(self, commenturl):
        # new_num = re.search(self.regex_dict['filter_remark'], commenturl)
        # return self.HOT_COMMENT_URL.format(new_num.group(1), self.hotcomment_num)
        return self.HOT_COMMENT_URL.format(self.commenturl_filter_remark(commenturl), self.hotcomment_num)

    def newcomment_ajax_by_commenturl(self, commenturl):
        # new_num = re.search(self.regex_dict['filter_remark'], commenturl)
        # return self.NEW_COMMENT_URL.format(new_num.group(1), self.newcomment_num)
        return self.NEW_COMMENT_URL.format(self.commenturl_filter_remark(commenturl), self.newcomment_num)

    def hotcomment_ajax_by_filter_remark(self, remark):
        return self.HOT_COMMENT_URL.format(remark, self.hotcomment_num)

    def newcomment_ajax_by_filter_remark(self, remark):
        return self.NEW_COMMENT_URL.format(remark, self.newcomment_num)

    def commenturl_filter_remark(self, commenturl):
        """
        根据评论URL拿到唯一标识
        :param commenturl: 评论URL
        :return: 唯一标识
        """
        new_num = re.search(self.regex_dict['filter_remark'], commenturl)
        return new_num.group(1)

    def commenturl_filterlist_by_channel(self, channel_coll):
        """
        过滤列表
        :param channel_coll: 查询的mongo集合
        :return: 该集合的所有唯一标识
        """
        remarks = channel_coll.find({}, {'filter_remark': 1, '_id': 0})
        result_list = list()
        for each in remarks:
            filter_mark = each.get('filter_remark')
            if filter_mark:
                result_list.append(filter_mark)
        return result_list


if __name__ == '__main__':
    um = URLmanager(hot_num=40, new_num=20)
    channels = ['shehui', 'guoji', 'guonei', 'lady']
    for k, v in um.ajaxdict_by_crawl_channels(channels).items():
        print(k)
        print(v)
        print('- ' * 60)
