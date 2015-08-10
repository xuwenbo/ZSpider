#!/usr/bin/python
#coding:utf-8

import urlparse


class UrlFilter(object):
    
    def __init__(self):
        self.repeatSet = set()
	self.suffixList = ['rar','zip','gif','jpg','js','css','png']
        
    
    def ignoreSuffix(self, linkList):
	#过滤url后缀，如rar，zip，jpg等文件,主要用到urlparse模块
        tmpList = []
        for url in linkList:
            path = urlparse.urlparse(url)[2]
            suffix = path.split('.')[-1]
            suffix = suffix.lower()
            if suffix in self.suffixList:
		linkList.remove(url)


    def deleteRepeatUrl(self, linkList):
	#过滤已经下载过的url，已下载过的url不应被重复下载，否则会导致性能问题
	for url in linkList:
	    if url not in self.repeatSet:
		self.repeatSet.add(url)
            else:
	        linkList.remove(url)	


    def urlfilter(self, linkList):
	#去除当前页面重复url
        linkList = list(set(linkList))
	#过滤url后缀
	self.ignoreSuffix(linkList)
	#去除所有已下载的url
	self.deleteRepeatUrl(linkList)
	return linkList


