#!/usr/bin/python

import Queue
import lxml.html
import time
import threading
import urlparse

from dataModel import UrlModel


class Parser(object):

    def __init__(self, fetchMode, keyword, htmlQueue, dataQueue, urlQueue):
        self.htmlQueue = htmlQueue
        self.dataQueue = dataQueue
        self.urlQueue = urlQueue
        self.keyword = keyword
        self.fetchMode = fetchMode
	self.thread = None

    def timestamp(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    def ignoreSuffix(self, linkList):
        tmpList = []
        for i in linkList:
            path = urlparse.urlparse(i)[2]
            suffix = path.split('.')[-1]
            suffix = suffix.lower()
            if(suffix not in ['rar','zip','gif','jpg','js','css','png']):
                tmpList.append(i)
        return tmpList

        

    def parseThread(self):
        while True:
            if self.htmlQueue.qsize() > 0:
                htmlNode = self.htmlQueue.get()
                print 'htmlNode info:', htmlNode.url ,htmlNode.depth
                linkList = []
                try:
                    doc = lxml.html.document_fromstring(htmlNode.html.decode('utf-8'))
                    doc.make_links_absolute(htmlNode.url)
                    links = doc.iterlinks()
                    for link in links:
                        linkList.append(link[2])

                    print 'fifter before num : %d ' % len(linkList)
                    linkList = list(set(linkList))
                    print 'fifter after num : %d ' % len(linkList)
                except Exception, e:
                    print str(e)
                    print 'parse html page error.'

                print 'ignore suffix before num : %d ' % len(linkList)
                linkList = self.ignoreSuffix(linkList)
                print 'ignore suffix after  num : %d' % len(linkList)

                for url in linkList:
                    urlNode = UrlModel(url, htmlNode.url, self.timestamp(), htmlNode.depth + 1 )
                    self.urlQueue.put(urlNode)

                for i in range(5):
                    print linkList[i] 
            else:
                time.sleep(1)
                


    def start(self):
        self.thread = threading.Thread(target =  self.parseThread)
        self.thread.start()
        print 'parse thread is started...'

