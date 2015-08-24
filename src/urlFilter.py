#!/usr/bin/python
# coding:utf-8

'''url过滤模块，用于过滤不符合条件的url
   其对外的接口即一个存放了url的list，它接受一个未过滤的urlList，
   并返回一个过滤后的urlList
   '''

import urlparse
import hashlib

from mylogger import logger
from config import SUFFIX_LIST 


class UrlFilter(object):
    '''url过滤类，实现功能包括：去除站外url、去除特定后缀url、去除重复url''' 
    def __init__(self, startUrls):
	# 用于存放已下载的url
        self.__repeatSet = set()

        # 获取初始url域名,用于比较其它url是否是站内链接
        host = urlparse.urlparse(startUrls[0]).hostname
	domain = host.split('.')[::-1]
	if domain[-1] == "www":
	    del domain[-1]
	self.__legalDomain = domain


    def __isLegalDomain(self, url):
	'''判断url是否为站内链接'''
	try:
	    host = urlparse.urlparse(url).hostname
	    if host == None:
	        return False
	    domain = host.split('.')[::-1]
	    for index in range(len(self.__legalDomain)):
	        if not domain[index] == self.__legalDomain[index]:
		    return False
	except Exception,e:
	    logger.error('isLegalDomain() exception: %s', str(e))
	    return False
	return True


    def __deleteExternalLink(self, linkList):
	'''删除站外链接'''
        tmpList = []
	for url in linkList:
	    if self.__isLegalDomain(url):
		tmpList.append(url)
	return tmpList

    
    def __ignoreSuffix(self, linkList):
	'''过滤url后缀，如rar，zip，jpg等文件'''
        tmpList = []
        for url in linkList:
	    try:
                path = urlparse.urlparse(url)[2]
                suffix = path.split('.')[-1]
                suffix = suffix.lower()
                if suffix not in SUFFIX_LIST:
		    tmpList.append(url)
	    except Exception,e:
		logger.error('ignoreSuffix() exception : %s, URL : %s', str(e), url)
		continue
	return tmpList
    
    
    def __getHashValue(self, url):
	'''获取url的hansh值'''
	md5 = hashlib.md5()
	md5.update(url)
	return md5.hexdigest()


    def __deleteRepeatUrl(self, linkList):
	'''过滤已经下载过的url, 并将url的hash值保存起来以供以后进行比较'''
        cleanList = []
        for url in linkList:
	    urlmd5 = self.__getHashValue(url)
	    if urlmd5 not in self.__repeatSet:
		self.__repeatSet.add(urlmd5)
		cleanList.append(url)
	return cleanList


    def getRepeatSetSize(self):
	return len(self.__repeatSet)
    

    def urlfilter(self, linkList):
	'''url过滤模块对外接口,接受未过滤的urlList，返回过滤后的urlList'''
	# 去除当前页面重复url
        tmpList1 = list(set(linkList))
	# 去除站外链接
	tmpList2 = self.__deleteExternalLink(tmpList1)
	# 过滤url后缀
	tmpList3 = self.__ignoreSuffix(tmpList2)
	# 去除所有已下载的url
	return  self.__deleteRepeatUrl(tmpList3)

