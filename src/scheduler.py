#!/usr/bin/python
#coding:utf-8

import threading
import Queue
import time
import sys
import gc
import objgraph

from meliae import scanner
from meliae import loader

from mylogger import logger
from mylogger import setLoggerLevel
from dataModel import UrlModel 
from dataModel import HtmlModel
from downloader import Downloader
from parser import Parser
from storage import Storage
from helper import timestamp


class Scheduler(object):

    def __init__(self, dbName, threadNum, logLevel, startUrls, depth, keyword, downloadMode):
        self.threadNum = threadNum
        self.startUrls = startUrls
        self.depth = depth
        self.keyword = keyword
        self.downloadMode = downloadMode
	self.dbName = dbName
	self.logLevel = logLevel
	self.exitFlag = threading.Event() 
	self.exitFlag.clear()

        #url队列存储待下载的url节点
        self.urlQueue = Queue.Queue()
        #html队列存储已经下载完成等待解析的html节点
        self.htmlQueue = Queue.Queue()
        #data队列存储以已解析完成并符合存入数据库条件的html节点
        self.dataQueue = Queue.Queue()


    def initUrlQueue(self, urlList):
        #将url封装为内部数据格式
        for url in urlList:
            urlNode = UrlModel(url, '', timestamp(), 0) 
            self.urlQueue.put(urlNode)


    def start(self):
	#设置日志等级
        setLoggerLevel(self.logLevel)

        #初始化url列表和三个主要模块
        self.initUrlQueue(self.startUrls)
        downloader = Downloader(self.threadNum, self.downloadMode, self.urlQueue, self.htmlQueue, self.exitFlag)
        parser = Parser(self.depth, self.startUrls, self.keyword, self.htmlQueue, self.dataQueue, self.urlQueue, self.exitFlag) 
        storage = Storage(self.dbName, self.dataQueue, self.exitFlag)

        #开启下载、解析、存储模块
        downloader.start()
        parser.start()
        storage.start()

        #主线程输出日志信息
	while True:
            '''
	    memfile = 'test.file'
	    scanner.dump_all_objects(memfile)
	    manager = loader.load(memfile, using_json=None,
		    show_prog=False, collapse=True)
            summarize = manager.summarize()
	    print 'summarize:/n%s/n/n' %(summarize)
	    print '\n\n'
            '''
            logger.error('URL QUEUE SIZE : %d' , self.urlQueue.qsize())
            logger.error('HTML QUEUE SIZE : %d' , self.htmlQueue.qsize())
            logger.error('DATA QUEUE SIZE : %d' , self.dataQueue.qsize())
            logger.error('REPEAT SET SIZE : %d' , parser.getRepeatSetSize())

            #如果当前没有正在下载的任务，且url队列、html队列、data队列都为空则表示任务完成，退出程序 
	    if not downloader.isDownloading() and self.urlQueue.qsize() < 1 and self.htmlQueue.qsize() < 1 and self.dataQueue.qsize() < 1:
		self.exitFlag.set()
		return

	    time.sleep(10)


def test():
    urlList = ['http://www.qq.com']
    sc = Scheduler('test', 20, 4, urlList, 2, 'photo', 0) 
    sc.start()


if __name__ == "__main__":
    test()
