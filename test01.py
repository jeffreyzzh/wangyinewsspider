# -*- coding: utf-8 -*-
# 2017/2/18 0018
# JEFF

import sys
import time


def test_print():
    for i in range(1, 100):
        print("\rHello,Gay!", i, end="")
        sys.stdout.flush()
        time.sleep(0.1)


if __name__ == '__main__':
    test_print()
    print('ok')
    print('yes')
