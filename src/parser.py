#!/usr/bin/python


class Parser(object):

    def __init__(self, fetchMode, keyword, htmlQueue, dataQueue, urlQueue):
        self.htmlQueue = htmlQueue
        self.dataQueue = dataQueue
        self.urlQueue = urlQueue
        self.keyword = keyword
        self.fetchMode = fetchMode

    def start(self):
        print 'parse html to data...'


