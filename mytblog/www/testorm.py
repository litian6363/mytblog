#!usr/bin/env python3
# -*- coding: utf-8 -*-


import orm
import asyncio
from models import User, Blog, Comment

async def test(loop):
    await orm.create_pool(loop, user='bm_ttt', password='root', db='mytblog')
    u = User(name='Test2', email='ttt@163.com', password='123456', image='about:blank')
    await u.save()
    re = await u.find_all()
    print(re)


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.run_forever()
