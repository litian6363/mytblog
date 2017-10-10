#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration
"""

import config_default


class Dict(dict):
    """
    Simple ict but support access as x.y style.
    重写获取方法
    例如：configs.db.host
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        # zip函数将参数数据分组返回[(arg1[0],arg2[0],arg3[0]...),(arg1[1],arg2[1],arg3[1]...),,,]
        # 以参数中元素数量最少的集合长度为返回列表长度
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % item)

    def __setattr__(self, key, value):
        self[key] = value


# 以override的为准，结合default
def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


# 将一个dict变成Dict
def to_dict(d):
    di = dict()
    for k, v in d.items():
        di[k] = to_dict(v) if isinstance(v, dict) else v
    return di

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError as e:
    pass

configs = to_dict(configs)
