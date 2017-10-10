#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

def chackbmp (path):
    with open(path ,'rb') as f:
        y = f.read()[:30]
        v = (struct.unpack('<ccIIIIIIHH' ,y))
        if v[0] == b'B' and v[1]==b'M':
            print('该文件是位图文件')
            print('图片大小为：%s X %s  颜色数为：%s' % (v[6],v[7],v[9]))
            
    
    
if __name__ == '__main__' :

    p = input('请输入相对路径')
    chackbmp(p)