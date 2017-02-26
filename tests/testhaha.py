# -*- coding: utf-8 -*-
# 2017/2/23
# author = JEFF
import re

filename = '20170226_data.txt'

with open(filename, 'r', encoding='utf-8') as f:
    cont = f.read()

counts = re.findall(r'{(.*?)]\n},', cont, re.S)
print(len(counts))
