#!usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

data = 'i am LiTian123'
sha1data = hashlib.sha1(data.encode('utf-8')).hexdigest()
print(sha1data)
print(data.encode('utf-8'))