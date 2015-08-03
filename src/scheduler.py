#!/usr/bin/python

import threading
import Queue

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

    def start(self):
        print 'server is started'

        downloader = Downloader(self.threadNum, self.downloadMode, self.urlQueue, self.htmlQueue)
        parser = Parser(self.fetchMode, self.keyword, self.htmlQueue, self.dataQueue, self.urlQueue) 
        storage = Storage(self.dataQueue)        

        downloader.start()
        parser.start()
        storage.start()




def test():
    sc = Scheduler(10,'http://www.douban.com', 2, 'photo', 0, 0) 
    sc.start()


if __name__ == "__main__":
    test()
