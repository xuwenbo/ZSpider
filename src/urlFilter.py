#!/usr/bin/python
#coding:utf-8

import urlparse
import hashlib
import sys

from config import SUFFIX_LIST 
from mylogger import logger


class UrlFilter(object):
    
    def __init__(self, startUrls):
	#用于去重已下载的url
        self.repeatSet = set()

        #获取初始url域名,用于比较其它url是否是此站内的链接
        host = urlparse.urlparse(startUrls[0]).hostname
	domain = host.split('.')[::-1]
	if domain[-1] == "www":
	    del domain[-1]
	self.legalDomain = domain


    def isLegalDomain(self, url):
	host = urlparse.urlparse(url).hostname
	if host == None:
	    return False
	domain = host.split('.')[::-1]
	for index in range(len(self.legalDomain)):
	    if not domain[index] == self.legalDomain[index]:
		return False
	return True


    def deleteExternalLink(self, linkList):
        tmpList = []
	for url in linkList:
	    if self.isLegalDomain(url):
		tmpList.append(url)
	return tmpList

    
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
    
    
    def getHashValue(self, url):
	md5 = hashlib.md5()
	md5.update(url)
	return md5.hexdigest()


    def deleteRepeatUrl(self, linkList):
	#过滤已经下载过的url，已下载过的url不应被重复下载，否则会导致性能问题
        cleanList = []
        for url in linkList:
	    urlmd5 = self.getHashValue(url)
	    if urlmd5 not in self.repeatSet:
		self.repeatSet.add(urlmd5)
		cleanList.append(url)
	return cleanList


    def getRepeatSetSize(self):
	return len(self.repeatSet)
    

    def urlfilter(self, linkList):
	#去除当前页面重复url
        tmpList1 = list(set(linkList))
	#去除站外链接
	tmpList2 = self.deleteExternalLink(tmpList1)
	#过滤url后缀
	tmpList3 = self.ignoreSuffix(tmpList2)
	#去除所有已下载的url
	return  self.deleteRepeatUrl(tmpList3)

