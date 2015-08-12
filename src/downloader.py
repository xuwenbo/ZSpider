#!/usr/bin/python 
#coding:utf-8

import threading
import time
import Queue
import requests
import sys
import random
from splinter import Browser

from mylogger import logger
from dataModel import HtmlModel
from helper import timestamp
from config import * 

reload(sys)
sys.setdefaultencoding("utf-8") 


class Downloader(object):

    def __init__(self, threadNum, downloadMode, urlQueue, htmlQueue, exitFlag):
        self.urlQueue = urlQueue 
        self.htmlQueue = htmlQueue
        self.threadNum = threadNum
        self.downloadMode = downloadMode
	self.exitFlag = exitFlag
        self.downloadingFlag = 0

        self.threadList = []
	self.ctrlThread = None;
	self.queueList = []


    def staticDownload(self, url):
	#静态下载函数，主要使用requests模块
        user_agent = random.choice(USER_AGENTS)
        headers = {'User-Agent': user_agent}
        try:
	    logger.debug('downloading url : %s', url)
            response = requests.get(url, timeout = CONNECT_TIME_OUT, headers = headers)
            if response.status_code == 200:
                return response.text
            else:
		logger.warning('download failed. status code : %d', response.status_code)
                return ""
        except Exception,e:
	    logger.warning('download exception (static): %s', str(e))
            return ""
    

    def dynamicDownload(self, url):
	#动态下载模块，主要使用splinter模块、phantomjs模块(需单独安装)
        try:
	    logger.debug('downloading url : %s', url)
            browser = Browser('phantomjs')
            browser.visit(url)
            html = browser.html
            browser.quit()
            return html
        except Exception,e:
	    logger.warning('download exception (dynamic): %s', str(e))
            return ""


    def downloadPage(self, url):
	#判断下载模式:静态下载/动态下载
        if self.downloadMode == 0:
            return self.staticDownload(url)
        elif self.downloadMode == 1:
            return self.dynamicDownload(url)


    def downloadThead(self, dlQueue):
	#下载线程，从为自己分配的任务队列中取出任务进行下载
        while True:
            if dlQueue.qsize() > 0:
                urlNode = dlQueue.get()
		#下载标志加一，表示当前有下载任务正在进行
                self.downloadingFlag += 1
                page = self.downloadPage(urlNode.url)
                if len(page) == 0:
		    logger.debug('download return null: %s', urlNode.url)
                    continue
		logger.debug('download page success, url: %s', urlNode.url)
		#将下载的html页面封装为内部数据格式并添加到html队列供解析模块解析
                htmlNode = HtmlModel(urlNode.url, page, timestamp(), urlNode.depth) 
                self.htmlQueue.put(htmlNode)
                self.downloadingFlag -= 1

            if self.exitFlag.is_set():
                logger.info('download work thread quit...')
                return

#            time.sleep(FETCH_TIME_INTERVAL)


    def controlThread(self):
	#创建下载线程
        for i in xrange(self.threadNum):
            dlQueue = Queue.Queue()
            self.queueList.append(dlQueue)
            t = threading.Thread(target = self.downloadThead, args = (dlQueue,))
	    t.setDaemon(True)
            self.threadList.append(t)

        #等待url队列有数据再开启下载线程
	while True:
            if self.urlQueue.qsize() < 1:
		time.sleep(1)
            else:
                for thread in self.threadList:
	            thread.start()
                break
       
        logger.info('download thread all started...')
        #主循环，为每个线程分配下载任务
        while True:
	    for dlQueue in self.queueList:
                if self.urlQueue.qsize() > 0 and dlQueue.qsize() < 1:
	            node = self.urlQueue.get()
		    dlQueue.put(node)

            if self.exitFlag.is_set():
                logger.info('download control thread quit...')
                return 
    
    def isDownloading(self):
	#此函数用于判断当前是否还有下载任务正在进行
        if self.downloadingFlag > 0:
            return True
        for dlQueue in self.queueList:
            if dlQueue.qsize() > 0:
                return True
            return False


    def start(self):
	#开启下载控制线程，在此线程中将开启诸多下载工作线程，控制线程负责为工作线程分配任务
	self.ctrlThread = threading.Thread(target =  self.controlThread)
        self.ctrlThread.setDaemon(True)
	self.ctrlThread.start()
	logger.info('download control thread is started...')


