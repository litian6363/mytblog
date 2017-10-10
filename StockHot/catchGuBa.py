#!/urs/bin/env python3
# -*- coding: utf-8 -*-

'抓取 http://guba.eastmoney.com/ 数据'

__author__ = 'Li Tian'

from urllib import request
from compileGubaByBS import myde

#创建基础地址
headurl = 'http://guba.eastmoney.com/list,'
stocknum = '000001'
endurl = ',f.html'

#组合地址
realurl = headurl + stocknum + endurl

#获取连接
with request.urlopen(realurl) as f:
    data = f.read()

#解释数据
myde(data.decode('utf-8'))