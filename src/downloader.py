#!/usr/bin/python 

import threading


class Downloader(object):

    def __init__(self, threadNum, downloadMode, urlQueue, htmlQueue):
        self.urlQueue = urlQueue 
        self.htmlQueue = htmlQueue
        self.threadNum = threadNum
        self.downloadMode = downloadMode
        self.threadList = []

    def workThead(self, htmlQueue):
        pass

    def start(self):
        for i in range(self.threadNum):
            t = threading.Thread(target = self.workThead, args = (self.htmlQueue,))
            self.threadList.append(t)

	print 'start download...'
