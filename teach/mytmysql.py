#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

conn = pymysql.connect(host = '127.0.0.1', port = 3306, 
user = 'root', passwd = 'root', db = 'testsc', charset = 'utf8')

cursor = conn.cursor()

cursor.execute('select * from test1')

print(cursor.fetchall())

conn.commit()
cursor.close()
conn.close()