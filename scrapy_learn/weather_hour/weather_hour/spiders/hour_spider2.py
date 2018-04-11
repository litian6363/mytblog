#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爬取http://www.86pm25.com/paiming.htm页面的每小时天气数据
"""

__author__ = 'LiTian'

import scrapy
import datetime


class WeatherOfHour(scrapy.Spider):
    name = 'hour2'
    start_urls = [
        'http://www.86pm25.com/paiming.htm'
    ]

    def parse(self, response):
        # 获取更新时间
        times = response.xpath('//div[@style=" margin:auto;'
                              ' width:960px; '
                              'text-align:center;'
                              'font-size:12px; '
                              'margin:10px; '
                              'margin-top:10px;"]/text()').extract_first()

        for tr in response.xpath('//table[@id="goodtable"]/tr'):
            yield {
                'city': tr.xpath('td/a/text()').extract_first(),
                'province': tr.xpath('td/text()').extract()[0],
                'AQI': tr.xpath('td/text()').extract()[1],
                'pm25': tr.xpath('td/text()').extract()[2],
                'assess': tr.xpath('td/div/font/text()').extract_first(),
                'time': datetime.datetime.strptime(times, '更新：%Y-%m-%d %H:%M'),  # 将字符串转换成datatime格式
                # 注意mongodb保存的时间格式是UTC，看起来比中国本地时间快8小时,其实没错
            }
