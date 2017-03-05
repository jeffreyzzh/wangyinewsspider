# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

import sys
import time
import datetime


# 测试刷新打印
def test_print():
    for i in range(1, 100):
        print("\rHello,Gay!", i, end="")
        sys.stdout.flush()
        time.sleep(0.1)


# 测试控制日期
def test_ctrl_data():
    pass


if __name__ == '__main__':
    print(time.time())
