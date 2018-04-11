# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# 如需用到管道来储存数据，需要在此定义item

import scrapy


class WeatherHourItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    AQI = scrapy.Field()
    pm25 = scrapy.Field()
    assess = scrapy.Field()
    time = scrapy.Field()
