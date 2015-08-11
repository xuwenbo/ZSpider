#!/usr/bin/python
#coding:utf-8

import Queue
import lxml.html
import time
import threading

from mylogger import logger
from dataModel import UrlModel
from pageFilter import PageFilter
from urlFilter import UrlFilter
from helper import timestamp


class Parser(object):

    def __init__(self, depth, keyword, htmlQueue, dataQueue, urlQueue, exitFlag):
        self.htmlQueue = htmlQueue
        self.dataQueue = dataQueue
        self.urlQueue = urlQueue
        self.keyword = keyword
        self.depth = depth
	self.exitFlag = exitFlag
	self.thread = None

        #pageFilter用于页面过滤，用于判断此页面是否需要存储
        self.myPageFilter = PageFilter(keyword)
	#urlFilter用于url过滤，用于判断此url是否需要进行继续下载
        self.myUrlFilter = UrlFilter() 


    def parseThread(self):
        while True:
            if self.htmlQueue.qsize() > 0:
		#从html队列取出数据
                htmlNode = self.htmlQueue.get()

                linkList = []
                try:
		    #解析html页面中的所有链接，主要使用lxml模块
                    doc = lxml.html.document_fromstring(htmlNode.html)
                    doc.make_links_absolute(htmlNode.url)
                    links = doc.iterlinks()
                    for link in links:
                        linkList.append(link[2])
                except Exception, e:
		    logger.warning('parse page exception: %s', str(e))
		    continue
                
		if len(linkList) == 0:
		    logger.warning('parse page success, but link is null: %s', htmlNode.url)
                    continue

                #过滤url，包括去url重复和特定后缀
                linkList = self.myUrlFilter.urlfilter(linkList)

                #过滤页面，判断页面是否需要存储
                if self.myPageFilter.isGood(htmlNode.html):               
                    self.dataQueue.put(htmlNode)

                #爬取深度控制,如果爬取深度大于指定深度则不继续往url队列中添加
                if htmlNode.depth + 1 > self.depth:
                    continue

                #将符合条件的url重新添加回url队列
                for url in linkList:
                    urlNode = UrlModel(url, htmlNode.url, timestamp(), htmlNode.depth + 1 )
                    self.urlQueue.put(urlNode)
            else:
                time.sleep(1)
	
            if self.exitFlag.is_set():
		logger.info('parser thread quit...')
		return


    def start(self):
	#解析线程，用来从html队列中取出数据并解析，将符合条件的url重新添加到url队列进行再次下载，
	#对符合存储条件的页面，将其添加到data队列进行数据库存储
        self.thread = threading.Thread(target =  self.parseThread)
        self.thread.setDaemon(True)
        self.thread.start()
	logger.info('parse thread is started...')

