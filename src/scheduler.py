#!/usr/bin/python
#coding:utf-8

import threading
import Queue
import time

from mylogger import logger
from dataModel import UrlModel 
from dataModel import HtmlModel
from downloader import Downloader
from parser import Parser
from storage import Storage
from helper import timestamp


class Scheduler(object):

    def __init__(self, dbName, threadNum, startUrls, depth, keyword, downloadMode, fetchMode):
        self.threadNum = threadNum
        self.startUrls = startUrls
        self.depth = depth
        self.keyword = keyword
        self.downloadMode = downloadMode
        self.fetchMode = fetchMode
	self.dbName = dbName

        self.urlQueue = Queue.Queue()
        self.htmlQueue = Queue.Queue()
        self.dataQueue = Queue.Queue()


    def initUrlQueue(self, urlList):
        for url in urlList:
            urlNode = UrlModel(url, '', timestamp(), 0) 
            self.urlQueue.put(urlNode)


    def start(self):
        self.initUrlQueue(self.startUrls)
        downloader = Downloader(self.threadNum, self.downloadMode, self.urlQueue, self.htmlQueue)
        parser = Parser(self.fetchMode, self.keyword, self.htmlQueue, self.dataQueue, self.urlQueue) 
        storage = Storage(self.dbName, self.dataQueue)        

        downloader.start()
        parser.start()
        storage.start()

	while True:
            logger.error('error')
	    logger.warning('warning')
	    logger.info('info')
	    logger.debug('debug')
	    print 'URL QUEUE SIZE: %d' % self.urlQueue.qsize()
	    print 'HTML QUEUE SIZE: %d' % self.htmlQueue.qsize()
	    print 'DATA QUEUE SIZE: %d' % self.dataQueue.qsize()
	    time.sleep(2)



def test():
    #urlList = ['http://www.douban.com','http://www.sina.com.cn','http://www.qq.com']
    urlList = ['http://www.qq.com']
    sc = Scheduler('test', 1, urlList, 2, 'photo', 0, 0) 
    sc.start()


if __name__ == "__main__":
    test()
