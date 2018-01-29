#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

__author__ = 'LiTian'

import scrapy
import datetime
from pymongo import MongoClient


class WeatherOfHour(scrapy.Spider):
    name = 'hour2'
    start_urls = [
        'http://www.86pm25.com/paiming.htm'
    ]
    client = MongoClient('localhost', 27017)
    db = client.weather_data
    weather_of_hour = db.weather_of_hour
    insert_data = []

    def parse(self, response):
        # 获取更新时间
        times = response.xpath('//div[@style=" margin:auto;'
                              ' width:960px; '
                              'text-align:center;'
                              'font-size:12px; '
                              'margin:10px; '
                              'margin-top:10px;"]/text()').extract_first()

        for tr in response.xpath('//table[@id="goodtable"]/tr'):
            self.insert_data.append({
                'city': tr.xpath('td/a/text()').extract_first(),
                'province': tr.xpath('td/text()').extract()[0],
                'AQI': tr.xpath('td/text()').extract()[1],
                'pm25': tr.xpath('td/text()').extract()[2],
                'assess': tr.xpath('td/div/font/text()').extract_first(),
                'time': datetime.datetime.strptime(times, '更新：%Y-%m-%d %H:%M'),  # 将字符串转换成datatime格式
                # 注意mongodb保存的时间格式是UTC，比中国本地时间快8小时
            })

        try:
            self.weather_of_hour.insert_many(self.insert_data)
        except Exception as e:
            print('>>>>>>>>>>>>>>>>ERROR:', e)


