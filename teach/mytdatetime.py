#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timezone, timedelta

def to_timestamp(dt_str, tz_str):

    dt = datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
    tz1 = re.match(r'(UTC)(\+|\-)(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])', tz_str)
    H, M = int(tz1.group(3)), int(tz1.group(4)) 
    if tz1.group(2) == '-':
        H, M = -H, -M
    tz = timezone(timedelta(hours=H, minutes=M))
    dt = dt.replace(tzinfo=tz)
    return dt.timestamp()
        

t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('Pass')