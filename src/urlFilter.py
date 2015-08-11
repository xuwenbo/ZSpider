#!/usr/bin/python
#coding:utf-8

import urlparse

from config import SUFFIX_LIST 
from mylogger import logger


class UrlFilter(object):
    
    def __init__(self):
        self.repeatSet = set()
        
    
    def ignoreSuffix(self, linkList):
	#过滤url后缀，如rar，zip，jpg等文件,主要用到urlparse模块
        tmpList = []
        for url in linkList:
            path = urlparse.urlparse(url)[2]
            suffix = path.split('.')[-1]
            suffix = suffix.lower()
            if suffix not in SUFFIX_LIST:
		tmpList.append(url)
	return tmpList


    def deleteRepeatUrl(self, linkList):
	#过滤已经下载过的url，已下载过的url不应被重复下载，否则会导致性能问题
        cleanList = []
        for url in linkList:
	    if url not in self.repeatSet:
		self.repeatSet.add(url)
		cleanList.append(url)
	return cleanList

    

    def urlfilter(self, linkList):
	#去除当前页面重复url
        linkList = list(set(linkList))
	#过滤url后缀
	tmpList = self.ignoreSuffix(linkList)
	#去除所有已下载的url
	return  self.deleteRepeatUrl(tmpList)

