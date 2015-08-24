#!/usr/bin/python
#coding:utf-8

'''日志模块，封装了logging模块,提供控制台输出、文件输出
   可分别设置不同的输出等级
   '''

import os
import logging
from helper import timestamp


LOGLEVEL = { 1 : logging.CRITICAL,
             2 : logging.ERROR,
             3 : logging.WARNING,
             4 : logging.INFO,
             5 : logging.DEBUG } 


class MyLogger(object):
    def __init__(self):
	self.logDir = os.getcwd() + '/log/'


    def __createLogDir(self):
        '''创建日志目录'''
        if not os.path.exists(self.logDir):
	    os.makedirs(self.logDir)


    def createLogger(self):
	'''创建并配置logger'''
	self.__createLogDir()

        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        # 创建文件日志处理器
        fh = logging.FileHandler(self.logDir + timestamp() +'_zspider.log')
        # 创建控制台日志处理器
        ch = logging.StreamHandler()

        # 控制两种日志输出方式的级别
        fh.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

        # 日志输出格式
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
	return logger


def setLoggerLevel(level):
    '''设置日志输出等级，数字越大日志信息越详细'''
    if int(level) > 0 and int(level) < 6:
        logger.setLevel(LOGLEVEL[level])


__myLogger = MyLogger()
logger = __myLogger.createLogger()


