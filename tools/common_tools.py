# -*- coding: utf-8 -*-
# 2017/2/24
# author = JEFF

import random
import time


class TimeTool(object):
    @staticmethod
    def current_time(spec_full=None, spec_simple=None):
        return TimeTool.format_time(spec_full=spec_full, spec_simple=spec_simple)

    @staticmethod
    def format_time(timex=None, format_spec='%Y-%m-%d %H:%M:%S', spec_full=None, spec_simple=None):
        if spec_full:
            return time.strftime('%Y-%m-%d %H:%M:%S')
        if spec_simple:
            return time.strftime('%Y-%m-%d')
        return time.strftime(format_spec, time.localtime(timex))


ua_list = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
    'Opera/9.80 (Windows NT 6.1; Opera Mobi/49; U; en) Presto/2.4.18 Version/10.00',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
]


def getrandomua():
    return random.choice(ua_list)


if __name__ == '__main__':
    print(getrandomua())
