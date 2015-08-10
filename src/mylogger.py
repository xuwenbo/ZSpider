#!/usr/bin/python
#coding:utf-8

import logging
import os
from helper import timestamp

#创建日志目录
logDir = os.getcwd() + '/log/'
if not os.path.exists(logDir):
    os.makedirs(logDir)


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

#创建文本日志处理器
fh = logging.FileHandler(logDir + timestamp() +'_zspider.log')
#创建控制台日志处理器
ch = logging.StreamHandler()

#控制两种日志输出方式的级别
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)

#日志输出格式
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
