#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, time, threading

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

# 创建一个socket
s = socket.socket()

# 监听端口:
s.bind(('0.0.0.0', 9999))

# 紧接着，调用listen()方法开始监听端口，传入的参数指定等待连接的最大数量：
s.listen(0)
print('Waiting for connection...')


while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    print(sock)
    print(addr)
    # 创建新线程来处理TCP连接:
    p = threading.Thread(target=tcplink, args=(sock, addr))
    p.start()

    
