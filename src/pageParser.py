#!/usr/bin/python
# coding:utf-8

'''解析模块，用于从html队列中取出html页面进行解析，将解析后符合条件
   的页面放入data队列，将符合条件的url放入url队列

   解析模块中用到了pageFilter模块和urlFilter模块，它们分别用来过滤
   html页面和url链接
   '''

import time

import lxml.html

from mylogger import logger
from dataModel import UrlModel,HtmlModel
from pageFilter import PageFilter
from urlFilter import UrlFilter
from threadPool import WorkRequest
from helper import timestamp


class Parser(WorkRequest):
    '''继承自线程池中的WorkRequest类，并实现线程执行函数
       功能: 过滤html页面，判断其是否符合存储条件并将符合条件的页面放入data队列
             解析html页面，过滤出符合条件的url并将其放入url队列
    '''
    def __init__(self, depth, startUrls, keyword, htmlQueue, dataQueue, urlQueue, exitEvent):
        self.__htmlQueue = htmlQueue
        self.__dataQueue = dataQueue
        self.__urlQueue = urlQueue
        self.__keyword = keyword
        self.__depth = depth
        self.__startUrls = startUrls
        self.__exitEvent = exitEvent
        # pageFilter用于页面过滤，判断此页面是否需要存储
        self.__myPageFilter = PageFilter(keyword)
        # urlFilter用于url过滤，判断url是否需要继续下载
        self.__myUrlFilter = UrlFilter(self.__startUrls)


    def getRepeatSetSize(self):
        return self.__myUrlFilter.getRepeatSetSize()


    def __parsePage(self):
	'''解析函数，完成解析模块的核心功能'''
        htmlNode = self.__htmlQueue.get()

        # 过滤页面，判断页面是否需要存储
        if self.__myPageFilter.isGood(htmlNode.html):
            dataNode = HtmlModel(htmlNode.url, '', htmlNode.time, htmlNode.depth)
            self.__dataQueue.put(dataNode)

        # 爬取深度控制,如果爬取深度达到指定深度则不继续解析页面中的链接
        if htmlNode.depth >= self.__depth:
            return

        linkList = []
        try:
            # 解析html页面中的所有链接，使用lxml模块
            doc = lxml.html.document_fromstring(htmlNode.html)
            doc.make_links_absolute(htmlNode.url)
            links = doc.iterlinks()
            for link in links:
                linkList.append(link[2])
        except Exception, e:
            logger.warning('Parse page exception: %s', str(e))
            return

        if len(linkList) == 0:
            logger.warning('Parse page success, but link is null: %s', htmlNode.url)
            return

        # 过滤url，包括去url重复、特定后缀以及站外链接
        linkList = self.__myUrlFilter.urlfilter(linkList)

        # 将符合条件的url重新添加回url队列
        for url in linkList:
            urlNode = UrlModel(url, htmlNode.url, timestamp(), htmlNode.depth + 1)
            self.__urlQueue.put(urlNode)


    def doWork(self):
        '''重写WorkRequest类的线程执行函数，此函数将在线程池中执行'''
        logger.debug('Start parser`s doWork...')
        while True:
            if self.__htmlQueue.qsize() > 0:
                self.__parsePage()
            else:
                time.sleep(1)
            #检测退出事件
            if self.__exitEvent.is_set():
                logger.info('Parser model quit...')
                return


