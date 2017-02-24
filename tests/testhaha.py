# -*- coding: utf-8 -*-
# 2017/2/23
# author = JEFF


def get_hello():
    return {
        'a': 1,
        'b': 2
    }


hello = get_hello()

hello['c'] = 3

hello['d'] = 4
print(hello)
