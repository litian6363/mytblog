#!usr/bin/env python3
# -*- coding: utf-8 -*-

# 查看版本
import sqlalchemy
print(sqlalchemy.__version__)

# 建立与数据库的连接(mysql)
from sqlalchemy import create_engine
engine = create_engine('mysql://root:root@localhost:3306/testsc')

# 创建基类
from sqlalchemy.ext.declarative import declarative_base
base = declarative_base()

# 建立模板，声明映射
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
class User(base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'),primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

# 建立数据表
print(User.__table__)
base.metadata.create_all(engine)

# 测试
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user.name)
print(ed_user.password)
print(str(ed_user.id))

