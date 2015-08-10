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

    def __init__(self, dbName, threadNum, startUrls, depth, keyword, downloadMode):
        self.threadNum = threadNum
        self.startUrls = startUrls
        self.depth = depth
        self.keyword = keyword
        self.downloadMode = downloadMode
	self.dbName = dbName

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
        #初始化url列表和三个主要模块
        self.initUrlQueue(self.startUrls)
        downloader = Downloader(self.threadNum, self.downloadMode, self.urlQueue, self.htmlQueue)
        parser = Parser(self.keyword, self.htmlQueue, self.dataQueue, self.urlQueue) 
        storage = Storage(self.dbName, self.dataQueue)        

        #开启下载、解析、存储模块
        downloader.start()
        parser.start()
        storage.start()

        #主线程输出日志信息
	while True:
            logger.info('URL QUEUE SIZE : %d' , self.urlQueue.qsize())
            logger.info('HTML QUEUE SIZE : %d' , self.htmlQueue.qsize())
            logger.info('DATA QUEUE SIZE : %d' , self.dataQueue.qsize())
	    time.sleep(3)



def test():
    #urlList = ['http://www.douban.com','http://www.sina.com.cn','http://www.qq.com']
    urlList = ['http://www.qq.com']
    sc = Scheduler('test', 1, urlList, 2, 'photo', 1) 
    sc.start()


if __name__ == "__main__":
    test()
