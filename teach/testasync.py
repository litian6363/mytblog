#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""用异步的方式读取'www.sina.com.cn', 'www.sohu.com', 'www.163.com'的hearder"""

__author__ = 'LiTian'

import asyncio


@asyncio.coroutine
async def wedget(host):
    print('wedget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wedget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
