#!/usr/bin/python 

import threading
import time
import Queue
import requests
from splinter import Browser


class Downloader(object):

    def __init__(self, threadNum, downloadMode, urlQueue, htmlQueue):
        self.urlQueue = urlQueue 
        self.htmlQueue = htmlQueue
        self.threadNum = threadNum
        self.downloadMode = downloadMode
	print 'download mode is %d' % downloadMode

        self.threadList = []
	self.ctrlThread = None;
	self.queueList = []

    def staticDownload(self, url):
        user_agent = r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36' 
        headers = {'User-Agent': user_agent}
        try:
            response = requests.get(url, timeout = 10, headers = headers)
            if response.status_code == 200:
                return response.content
            else:
                return ""
        except Exception,e:
            print 'staticDownload exception.'
            return ""
    
    def dynamicDownload(self, url):
        try:
            print 'visit url is : %s' % url
            browser = Browser()
            browser.visit(url)
            html = browser.html
            browser.quit()
            return html
        except Exception,e:
            print 'dynamicDownload exeception.'
            print str(e) 
            return ""

    def downloadPage(self, url):
        if self.downloadMode == 0:
            return self.staticDownload(url)
        elif self.downloadMode == 1:
            return self.dynamicDownload(url)

    def downloadThead(self, dlQueue):
	print 'download thread is running...'
        while True:
            print 'dlQueue size in downloadThead is %d' % dlQueue.qsize()
            if dlQueue.qsize() > 0:
                print 'i got a url..'
                url = dlQueue.get().url
                page = self.downloadPage(url)
                print 'download one page ...'
#                print page
            time.sleep(5)

    def controlThread(self):
        for i in xrange(self.threadNum):
            dlQueue = Queue.Queue()
            self.queueList.append(dlQueue)
            t = threading.Thread(target = self.downloadThead, args = (dlQueue,))
            self.threadList.append(t)

	while True:
            if self.urlQueue.qsize() < 1:
		time.sleep(1)
            else:
                for thread in self.threadList:
	            thread.start()
		print 'all download thread is running...'
                break
       
        while True:
	    for dlQueue in self.queueList:
                if self.urlQueue.qsize() > 0 and dlQueue.qsize() < 1:
	            node = self.urlQueue.get()
		    dlQueue.put(node)
                    print 'urlQueue size in ctrlThread is %d ' % self.urlQueue.qsize()
                    print 'dlQueue size in ctrlThread is %d ' % dlQueue.qsize()
                time.sleep(1)

    def start(self):
	self.ctrlThread = threading.Thread(target =  self.controlThread)
	self.ctrlThread.start()
        print 'control thread is started...'


