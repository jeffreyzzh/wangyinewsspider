# -*- coding: utf-8 -*-
# 2017/2/21
# author = JEFF

import json
import re
import traceback
from tools.common_tools import TimeTool
from codes.spider_base import BaseClass
from codes.spider_downloader import URLdowner


class URLparser(object):
    regex_dict = {
        'cont': re.compile('(\[.*\])', re.S),
        'titles': re.compile('"title":"(.*?)"', re.S),
        'docurls': re.compile('"docurl":"(.*?)"', re.S),
        'commenturls': re.compile('"commenturl":"(.*?)"', re.S),
        'timeums': re.compile('"tienum":(.*?),', re.S),
        'tlinks': re.compile('"tlink":"(.*?)"', re.S),
        'labels': re.compile('"label":"(.*?)"', re.S),
        'o_keywords': re.compile('"keywords":\[\s*(.*?)\s*\],', re.S),
        'times': re.compile('"time":"(.*?)"', re.S),
        'newstypes': re.compile('"newstype":"(.*?)"', re.S),
        'channelnames': re.compile('"channelname":"(.*?)"', re.S),
        'filter_remark': re.compile('bbs/(.*?)\.html')
    }

    def __init__(self):
        self.logger = BaseClass.getlogger()

    def parse_ajax_channel(self, cont, dochannel):
        """
        解析ajax url请求内容
        :param cont: list,每一个元素是一个新闻dict
        :param dochannel: 爬取的频道
        :return:
        """
        if not cont:
            return None
        cont = re.search('(\[.*\])', cont.strip(), re.S).group()
        titles = re.findall(self.regex_dict['titles'], cont)
        docurls = re.findall(self.regex_dict['docurls'], cont)
        commenturls = re.findall(self.regex_dict['commenturls'], cont)
        timeums = re.findall(self.regex_dict['timeums'], cont)
        tlinks = re.findall(self.regex_dict['tlinks'], cont)
        labels = re.findall(self.regex_dict['labels'], cont)
        o_keywords = re.findall(self.regex_dict['o_keywords'], cont)
        times = re.findall(self.regex_dict['times'], cont)
        newstypes = re.findall(self.regex_dict['newstypes'], cont)
        channelnames = re.findall(self.regex_dict['channelnames'], cont)
        keywords = list()
        for key in o_keywords:
            key = key.replace(' ', '')
            if not key:
                continue
            k_infos = key.split('\n,')
            n_infos = []
            for each in k_infos:
                each = each.replace('${type}', 'news.163.com')
                each_dict = json.loads(each)
                n_infos.append(each_dict)
            keywords.append(n_infos)

        if len(channelnames) == 0:
            for i in range(len(titles)):
                channelnames.append(dochannel)

        news = []
        for title, docurl, commenturl, timeum, tlink, label, keyword, time, newstype, channelname in zip(
                titles, docurls, commenturls, timeums, tlinks, labels, keywords, times, newstypes, channelnames
        ):
            dict_info = {
                'title': title,
                'docurl': docurl,
                'commenturl': commenturl,
                'timeum': timeum,
                'tlink': tlink,
                'label': label,
                'keyword': keyword,
                'time': time,
                'newstype': newstype,
                'channelname': channelname
            }
            filter_remark = re.search(self.regex_dict['filter_remark'], commenturl)
            if filter_remark:
                dict_info['filter_remark'] = filter_remark.group(1)
            dict_info['spider_time'] = TimeTool.current_time()
            news.append(dict_info)
        return news

    def parser_hotcomment(self, cont, url):
        if not cont:
            return None
        try:
            dict_json = json.loads(cont)
            result_info = dict()
            comment_list = list()
            if dict_json.get('code') == '40106':
                return None
            if dict_json.get('message') == 'Thread is closed':
                return None
            if not dict_json.get('comments'):
                return None
            for k, v in dict_json['comments'].items():
                comment_info = dict()
                comment_info['content'] = v['content']
                comment_info['ip'] = v['ip']
                comment_info['vote'] = v['vote']
                comment_info['against'] = v['against']
                comment_info['commentId'] = v['commentId']
                comment_info['location'] = v['user']['location']
                comment_info['createTime'] = v['createTime']
                comment_info['nickname'] = v.get('user').get('nickname')
                comment_list.append(comment_info)
            result_info['comments'] = comment_list
            result_info['newListSize'] = dict_json.get('newListSize') if dict_json.get('newListSize') else len(
                comment_list)
            result_info['commentSize'] = len(comment_list)
            return result_info
        except Exception as e:
            self.logger.log(e)
            self.logger.error('url: {} has a problem'.format(url))
            return None


if __name__ == '__main__':
    spider_url = 'http://temp.163.com/special/00804KVA/cm_shehui.js'
    p = URLparser()
    d = URLdowner()
    cont = d.ajax_fetch(spider_url)
    x = p.parse_ajax_channel(cont)
    for each in x:
        print(each)
        print(type(each))
        break
