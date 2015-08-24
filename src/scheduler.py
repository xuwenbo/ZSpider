#!/usr/bin/python
# coding:utf-8

'''爬虫启动模块:
       1.负责所有模块的启动和调度
       2.为下载模块的各个下载队列分配url
       3.输出调试信息
       4.检测程序是否运行完成
'''

import time
import Queue
import threading

from mylogger import logger
from dataModel import UrlModel
from downloader import Downloader
from pageParser import Parser
from storage import Storage
from threadPool import ThreadPool
from helper import timestamp
from config import PRINT_TIME_INTERVAL


class Scheduler(object):
    '''初始化并开启爬虫程序所有模块,并为下载模块分配url'''
    def __init__(self, dbName, threadNum, logLevel, startUrls, depth, keyword, downloadMode):
        self.__threadNum = threadNum
        self.__startUrls = startUrls
        self.__depth = depth
        self.__keyword = keyword
        self.__downloadMode = downloadMode
        self.__dbName = dbName
        self.__logLevel = logLevel
        
        self.__exitEvent = threading.Event()
        # url队列存储待下载的url节点
        self.__urlQueue = Queue.Queue()
        # html队列存储已经下载完成等待解析的html节点
        self.__htmlQueue = Queue.Queue()
        # data队列存储已解析完成并符合存入数据库条件的html节点
        self.__dataQueue = Queue.Queue()
        # 存储为各个下载模块分配的下载队列
        self.__downloadQueueList = []
	# 创建线程池
        self.__threadPool = ThreadPool(threadNum + 2)
        self.__downloadingFlag = 0


    def __initUrlQueue(self, urlList):
        '''将url封装为内部数据格式'''
        for url in urlList:
            urlNode = UrlModel(url, '', timestamp(), 0)
            self.__urlQueue.put(urlNode)


    def start(self):
	'''创建并启动各个模块'''
        logger.debug('Init start urls...')
        self.__initUrlQueue(self.__startUrls)
        
	# 启动threadNum个下载器并为它们分配下载队列 
        logger.debug('Put downloader to thread pool...')
        for i in range(self.__threadNum):
            dlQueue = Queue.Queue()
            self.__downloadQueueList.append(dlQueue)
            downloadReq = Downloader(dlQueue, self.__downloadMode, self.__htmlQueue, self.__exitEvent, self.__downloadingFlag)
            self.__threadPool.putRequest(downloadReq)

	# 创建解析模块并添加到线程池运行
        logger.debug('Put parser to thread pool...')
        parserReq = Parser(self.__depth, self.__startUrls, self.__keyword, self.__htmlQueue, self.__dataQueue, self.__urlQueue, self.__exitEvent)
        self.__threadPool.putRequest(parserReq)

	# 创建存储模块并添加到线程池运行
        logger.debug('Put storage to thread pool...')
        storageReq = Storage(self.__dbName, self.__dataQueue, self.__exitEvent)
        self.__threadPool.putRequest(storageReq)

	# 主循环用于为各个下载队列分配url以及输出日志信息
        logger.debug('start main loop...')
        lastTime = time.time()
        while True:
            for dlQueue in self.__downloadQueueList:
                if self.__urlQueue.qsize() > 0 and dlQueue.qsize() < 1:
                    node = self.__urlQueue.get()
                    dlQueue.put(node)

            now = time.time()
            if now - lastTime > PRINT_TIME_INTERVAL:
                logger.info('URL QUEUE SIZE : %d', self.__urlQueue.qsize())
                logger.info('HTML QUEUE SIZE : %d', self.__htmlQueue.qsize())
                logger.info('DATA QUEUE SIZE : %d', self.__dataQueue.qsize())
                logger.info('REPEAT SET SIZE : %d', parserReq.getRepeatSetSize())
                # 延迟检测退出事件，防止程序启动时即退出 
                if now - lastTime > 30:
                    if self.__urlQueue.qsize() < 1 and self.__htmlQueue.qsize() < 1 and \
	                          self.__dataQueue.qsize() < 1 and self.__downloadingFlag < 1:
                        self.__exitEvent.set()
                        self.__threadPool.close(True)
                        return
                lastTime = now



