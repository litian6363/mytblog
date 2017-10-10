#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image

im = Image.open('abc\picture.jpg')

weight,high = im.size
print(weight,high)

im.thumbnail((weight//2,high//2))
im.save('abc\tp1.jpg','jpeg')