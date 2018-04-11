# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# 不要忘了在settings.py上解除ITEM_PIPELINES的注释，pipelines才会生效
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class WeatherHourPipeline(object):

    collection_name = 'weather_of_hour'

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongodb_host = mongo_host
        self.mongodb_port = mongo_port
        self.mongodb_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """获取settings.py里的mongodb配置"""
        return cls(
            mongo_host=crawler.settings.get('MONGODB_HOST'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGODB_DBNAME')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongodb_host, self.mongodb_port)  # 创建mongodb链接
        self.db = self.client[self.mongodb_db]  # 指定数据库

    def close_spider(self, spider):
        self.client.close()  # 关闭链接

    def process_item(self, item, spider):
        """具体操作数据的地方"""
        self.db[self.collection_name].insert_one(dict(item))  # 插入一条数据进collection_name对应的表
        return item

