# -*- coding: utf-8 -*-
# 2017/2/24
# author = JEFF

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
