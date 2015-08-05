#!/usr/bin/python

import threading
import Queue
import time

from dataModel import UrlModel 
from dataModel import HtmlModel
from downloader import Downloader
from parser import Parser
from storage import Storage


class Scheduler(object):

    def __init__(self, threadNum, startUrls, depth, keyword, downloadMode, fetchMode):
        self.threadNum = threadNum
        self.startUrls = startUrls
        self.depth = depth
        self.keyword = keyword
        self.downloadMode = downloadMode
        self.fetchMode = fetchMode

        self.urlQueue = Queue.Queue()
        self.htmlQueue = Queue.Queue()
        self.dataQueue = Queue.Queue()

    def timestamp(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    def initUrlQueue(self, urlList):
        for url in urlList:
            urlNode = UrlModel(url, '', self.timestamp(), 0) 
            self.urlQueue.put(urlNode)


    def start(self):
        print 'server is started'
        self.initUrlQueue(self.startUrls)

        downloader = Downloader(self.threadNum, self.downloadMode, self.urlQueue, self.htmlQueue)
        parser = Parser(self.fetchMode, self.keyword, self.htmlQueue, self.dataQueue, self.urlQueue) 
        storage = Storage(self.dataQueue)        

        downloader.start()
        parser.start()
        storage.start()



def test():
    #urlList = ['http://www.douban.com','http://www.sina.com.cn','http://www.qq.com']
    urlList = ['http://www.douban.com']
    sc = Scheduler(1, urlList, 2, 'photo', 0, 0) 
    sc.start()


if __name__ == "__main__":
    test()
