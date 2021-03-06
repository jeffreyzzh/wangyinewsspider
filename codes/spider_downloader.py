# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

import requests
import traceback
from codes.spider_base import BaseClass
from tools.common_tools import getrandomua

spiderheaders = {
    'User-Agent': getrandomua()
}


# URL下载器
class URLdowner(object):
    CRAWL_COUNT = 5
    CRAWL_TIMEOUTS = 3

    def __init__(self):
        self.logger = BaseClass.getlogger()

    def ajax_fetch(self, url):
        return self.fetch(url, 'gbk')

    def page_fetch(self, url):
        return self.fetch(url, 'utf-8')

    def fetch(self, url, encoding, count=1):
        self.logger.debug('fetch url >> {}'.format(url))
        if count >= self.CRAWL_COUNT + 1:
            self.logger.error('url: {} to much error'.format(url))
            return None
        try:
            r = requests.get(url, timeout=self.CRAWL_TIMEOUTS, headers=spiderheaders)
            r.encoding = encoding
            if not r.status_code == 404:
                return r.text
            else:
                self.logger.error('url: {} 404 Not Found'.format(url))
        except Exception as e:
            self.logger.error(e)
            if count == 5:
                self.logger.error('\r\n' + traceback.format_exc())
            return self.fetch(url, encoding, count=count + 1)


if __name__ == '__main__':
    # u = URLdowner()
    # cont = u.page_fetch('http://www.wawa.com')
    # print(cont)
    import time

    s = time.time()
    print(headers)
    print(time.time() - s)
