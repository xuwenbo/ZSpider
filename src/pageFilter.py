#!/usr/bin/python
# coding:utf-8

'''页面过滤模块，根据关键字对页面正文进行过滤
   流程： 1.删除页面内所有html标签获取正文内容
          2.在正文中查找关键字
          '''
import re


class PageFilter(object):
   
    def __init__(self, keyword):
        self.__keyword = keyword
	# 创建正则对象，匹配所有html标签
	self.__regex = re.compile(r'<[^>]+>', re.S)


    def isGood(self, html):
        '''页面过滤函数，根据关键字对html页面进行过滤并返回结果，
           满足存储条件返回True，否则返回False
           '''
        if self.__keyword == "":
	    return True
	# 去除html页面中所有的html标签以获得正文
	text = self.__regex.sub('', html)
	# 在正文中查找关键字
	result = re.search(self.__keyword, text)
        if result:
            return True 
        else:
            return False 

