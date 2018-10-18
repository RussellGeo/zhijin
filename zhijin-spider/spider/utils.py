# -*- coding: utf-8 -*-

import time
import hashlib

def now_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def create_id(data):
    return hashlib.md5(str(data)).hexdigest()
