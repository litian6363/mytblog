#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aiomysql, asyncio


# 日志函数
def log(sql):
    logging.info('SQL: %s' % sql)


# 创建数据库连接池
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    # 连接池由全局变量__pool存储，每个HTTP请求都可以从连接池中直接获取数据库连接，不必频繁地打开和关闭数据库连接。
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


# 执行SQL的select语句的函数
async def select(sql, args=None, size=None):
    log(sql)
    # 定义获取连接池
    # global __pool
    # 创建一个Connection（连接）实例conn
    async with __pool.get() as conn:
        # 创建connection的cursor(游标)实例cur，cursor用来执行mysql语句命令；aiomysql.DictCursor用来将结果变成字典来返回
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换
            await cur.execute(sql.replace('?', '%s'), args or ())
            # 如果有size则返回size大小的结果，不然则返回全部
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs


# 执行SQL的INSERT、UPDATE、DELETE等语句集合的函数
async def execute(sql, args=None, autocommit=True):
    log(sql)
    # 创建一个Connection（连接）实例conn
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            # 创建connection的cursor(游标)实例cur，cursor用来执行mysql语句命令；aiomysql.DictCursor用来将结果变成字典来返回
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换
                await cur.execute(sql.replace('?', '%s'), args or ())
                # 返回执行影响行数
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException:
            if not autocommit:
                await conn.rollback()
            raise
        return affected


def create_args_string(num):
    l = []
    for n in range(num):
        l.append('?')
    return ', '.join(l)


class Field(object):
    # 4个参数为：1名字；2数据类型、范围；3是否主键；4默认值
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


# 创建元类
class ModelMetaclass(type):
    # __new__自定义创建类
    # __new__需要的的4个参数为：1当前准备创建的类对象；2创建后类的名字；3类继承的父类集合；4类的方法集合
    def __new__(cls, name, bases, attrs):
        # 排除Model类本身：
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称：
        table_name = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, table_name))
        # 获取所有的Field和主键名
        mappings = dict()  # 存放映射关系
        fields = []  # 存放主键外的属性
        primarykey = None  # 存放主键
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键
                    if primarykey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primarykey = k
                else:
                    fields.append(k)
        if not primarykey:
            raise RuntimeError('Primary key not found')
        # 从类属性中删除Field属性,否则，容易造成运行时错误（实例的属性会遮盖类的同名属性)
        for k in mappings.keys():
            attrs.pop(k)
        escaped_field = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primarykey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键属性名
        # 构造默认的select,insert,update和delete语句：
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primarykey, ', '.join(escaped_field), table_name)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            table_name, ', '.join(escaped_field), primarykey, create_args_string(len(escaped_field) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s` = ?' % (
            table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primarykey)
        attrs['__delete__'] = 'delete from `%s` where `%s` = ?' % (table_name, primarykey)
        return type.__new__(cls, name, bases, attrs)


# 创建模板基类,父类为dict,具备所有dict功能
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    # 自定义属性获取，例子：（对象.属性）
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % item)

    # 自定义设置对象属性，例子：（对象.属性 = ?）
    def __setattr__(self, key, value):
        self[key] = value

    def getvalue(self, key):
        # 返回self的key，若不存在，返回None
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    # @classmethod代表这是一个类方法，可以直接（类.方法名）调用，不需要创造实例
    @classmethod
    async def find_all(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        # 默认值不能为[],因为会出错
        if args is None:
            args = []
        order_by = kw.get('order_by', None)
        if order_by:
            sql.append('order by')
            sql.append(order_by)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def find_number(cls, select_field, where=None, args=None):
        sql = ['select %s _num_ from `%s`' % (select_field, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.get_value_or_default, self.__fields__))
        args.append(self.get_value_or_default(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            log('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getvalue, self.__fields__))
        args.append(self.getvalue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            log('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getvalue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            log('failed to remove by primary key: affected rows: %s' % rows)
