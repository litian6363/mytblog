#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

__author__ = 'LiTian'

import scrapy


class WeatherOfHour(scrapy.Spider):
    name = 'hour'
    start_urls = [
        'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462261004631'
    ]

    def parse(self, response):
        for one in eval(response.xpath('//input[@name="gisDataJson"]/@value').extract_first()):
            yield one

        for a in response.xpath('//div[@class="report_page"]/a[text()="下一页"]'):
             yield response.follow(a, callback=self.parse)
