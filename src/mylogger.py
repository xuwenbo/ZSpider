#!/usr/bin/python
#coding:utf-8

import logging
import os
from helper import timestamp


class MyLogger(object):

    def __init__(self):
	self.logDir = os.getcwd() + '/log/'


    def createLogDir(self):
        #创建日志目录
        if not os.path.exists(self.logDir):
	    os.makedirs(self.logDir)


    def createLogger(self):
	self.createLogDir()

        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        #创建文本日志处理器
        fh = logging.FileHandler(self.logDir + timestamp() +'_zspider.log')
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
	return logger


def setLoggerLevel(level):
    if level == 1:
	logger.setLevel(logging.CRITICAL)
    elif level == 2:
	logger.setLevel(logging.ERROR)
    elif level == 3:
	logger.setLevel(logging.WARNING)
    elif level == 4:
	logger.setLevel(logging.INFO)
    elif level == 5:
	logger.setLevel(logging.DEBUG)


myLogger = MyLogger()
logger = myLogger.createLogger()


