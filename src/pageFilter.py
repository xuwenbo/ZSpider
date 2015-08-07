#!/usr/bin/python
#coding:utf-8

class PageFilter(object):

	def __init__(self, keywords):
		self.keywords = keywords
	
	def isGood(self, html):
		if len(html) == 0:
			return False
		else:
			return True

