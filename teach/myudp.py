#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

#建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#绑定端口
s.bind(('127.0.0.1',9999))

print('Bind UDP on 9999')
while True:
    #接受数据
    data, addr = s.recvfrom(1024)
    print('Recdived from %s:%s' % addr)
    s.sendto(b'Hello, %s!' % data, addr)