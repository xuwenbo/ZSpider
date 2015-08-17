#!/usr/bin/python
# coding:utf-8

import lxml.html
import time
import threading

from mylogger import logger
from dataModel import UrlModel
from dataModel import  HtmlModel
from pageFilter import PageFilter
from urlFilter import UrlFilter
from helper import timestamp


class Parser(object):

    def __init__(self, depth, startUrls, keyword, htmlQueue, dataQueue, urlQueue, exitFlag):
        self.htmlQueue = htmlQueue
        self.dataQueue = dataQueue
        self.urlQueue = urlQueue
        self.keyword = keyword
        self.depth = depth
        self.startUrls = startUrls
        self.exitFlag = exitFlag
        self.thread = None

        #pageFilter用于页面过滤，用于判断此页面是否需要存储
        self.myPageFilter = PageFilter(keyword)
        #urlFilter用于url过滤，用于判断此url是否需要进行继续下载
        self.myUrlFilter = UrlFilter(self.startUrls)


    def getRepeatSetSize(self):
        return self.myUrlFilter.getRepeatSetSize()


    def parsePage(self):
        #从html队列取出数据
        htmlNode = self.htmlQueue.get()

        #过滤页面，判断页面是否需要存储
        if self.myPageFilter.isGood(htmlNode.html):
            dataNode = HtmlModel(htmlNode.url, '', htmlNode.time, htmlNode.depth)
            self.dataQueue.put(dataNode)

        #爬取深度控制,如果爬取深度达到指定深度则不继续解析页面中的链接
        #如果继续解析，则用于去除重复的repeatSet集合的大小将呈指数增长
        if htmlNode.depth >= self.depth:
            return

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
            return

        if len(linkList) == 0:
            logger.warning('parse page success, but link is null: %s', htmlNode.url)
            return

        #过滤url，包括去url重复、特定后缀以及站外链接
        linkList = self.myUrlFilter.urlfilter(linkList)

        #将符合条件的url重新添加回url队列
        for url in linkList:
            urlNode = UrlModel(url, htmlNode.url, timestamp(), htmlNode.depth + 1)
            self.urlQueue.put(urlNode)


    def auxiliaryParseThread(self):
	#辅助解析线程，在html队列超过一定数量范围后启动，用于加快解析速度
        while True:
            if self.htmlQueue.qsize() > 100:
                self.parsePage()
                if self.exitFlag.is_set():
                    logger.info('auxiliary parser thread quit.')
                    return
            else:
                print 'auxiliary parser thread is stoped...'
                return


    def mainParseThread(self):
	#主解析线程，如果主解析线程解析速度跟不上下载模块下载速度则开启辅助线程加快解析
        baseNum = 100
        while True:
            if self.htmlQueue.qsize() > baseNum:
		#根据基数开启新的辅助解析线程
                print 'html queue Num: %d, baseNum is : %d, new thead num is : %d' % (self.htmlQueue.qsize(),
			baseNum, self.htmlQueue.qsize() / baseNum)
                for i in range(self.htmlQueue.qsize() / baseNum):
                    print 'new auxiliary parser thread is start...'
                    t = threading.Thread(target=self.auxiliaryParseThread)
                    t.setDaemon(True)
                    t.start()
                baseNum += 100

            if self.htmlQueue.qsize() > 0:
                self.parsePage()
            else:
                time.sleep(1)

            #基数重置
            if self.htmlQueue.qsize < 100:
                baseNum = 100

            if self.exitFlag.is_set():
                logger.info('main parser thread quit...')
                return


    def start(self):
        #解析线程，用来从html队列中取出数据并解析，将符合条件的url重新添加到url队列进行再次下载，
        #对符合存储条件的页面，将其添加到data队列进行数据库存储
        self.thread = threading.Thread(target=self.mainParseThread)
        self.thread.setDaemon(True)
        self.thread.start()
        logger.info('parse thread is started...')

