#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, time

try:
    #建立连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for data in [b'Michael', b'Tracy', b'Sarah']:
        #发送数据
        s.sendto(data, ('127.0.0.1', 9999))
        #接受数据
        print(s.recv(1024).decode('utf-8'))
        
        time.sleep(0.5)

finally:
    s.close()