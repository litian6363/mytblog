#!/urs/bin/env python3
# -*- coding: utf-8 -*-

'Decode Guba data'

__author__ = 'Li Tian'

from bs4 import BeautifulSoup

def myde(data):
    #创建BeautifulSoup对象
    soup = BeautifulSoup(data, 'lxml')
   
    #抓取div标签里，所有class等于articleh的数据
    sArticleh = soup.select('div.articleh')
   
    for t in sArticleh:
        if t.get_text('|').count('|') >= 8 :
            print('a')
        else :
            print('b')
