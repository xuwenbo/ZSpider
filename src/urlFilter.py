#!/usr/bin/python
#coding:utf-8

import urlparse


class UrlFilter(object):
    
    def __init__(self):
        self.repeatSet = set()
	self.suffixList = ['rar','zip','gif','jpg','js','css','png']
        
    
    def ignoreSuffix(self, linkList):
        for url in linkList:
            path = urlparse.urlparse(url)[2]
            suffix = path.split('.')[-1]
            suffix = suffix.lower()
            if(suffix not in self.suffixList):
		linkList.remove(url)


    def deleteRepeatUrl(self, linkList):
	for url in linkList:
	    if url not in self.repeatSet:
		self.repeatSet.add(url)
            else:
	        linkList.remove(url)	


    def urlfilter(self, linkList):
        linkList = list(set(linkList))
	self.ignoreSuffix(linkList)
	self.deleteRepeatUrl(linkList)
	return linkList


