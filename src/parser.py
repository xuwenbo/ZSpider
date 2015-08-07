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

    def __init__(self, fetchMode, keyword, htmlQueue, dataQueue, urlQueue):
        self.htmlQueue = htmlQueue
        self.dataQueue = dataQueue
        self.urlQueue = urlQueue
        self.keyword = keyword
        self.fetchMode = fetchMode
	self.thread = None

        self.myPageFilter = PageFilter(keyword)
        self.myUrlFilter = UrlFilter() 


    def parseThread(self):
        while True:
            if self.htmlQueue.qsize() > 0:
                htmlNode = self.htmlQueue.get()
                linkList = []
                try:
                    doc = lxml.html.document_fromstring(htmlNode.html)
                    doc.make_links_absolute(htmlNode.url)
                    links = doc.iterlinks()
                    for link in links:
                        linkList.append(link[2])
                except Exception, e:
                    print str(e)
                
                linkList = self.myUrlFilter.urlfilter(linkList)

                if(self.myPageFilter.isGood(htmlNode.html)):               
                    self.dataQueue.put(htmlNode)

                for url in linkList:
                    urlNode = UrlModel(url, htmlNode.url, timestamp(), htmlNode.depth + 1 )
                    self.urlQueue.put(urlNode)
            else:
                time.sleep(1)
                


    def start(self):
        self.thread = threading.Thread(target =  self.parseThread)
        self.thread.start()
        print 'parse thread is started...'

