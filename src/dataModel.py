#!/usr/bin/python
#coding:utf-8

class UrlModel(object):
    count = 0
    
    def __init__(self, url, parentUrl, time, depth):
        self.url = url                #url地址
        self.parentUrl = parentUrl    #父url
        self.time = time              #生成节点时间
        self.depth = depth            #页面深度

        UrlModel.count +=1

    def __del__(self):
	UrlModel.count -=1

    def howmany(self):
	return UrlModel.count

class HtmlModel(object):

    count = 0

    def __init__(self, url, html, time, depth):
        self.url = url                #url地址
        self.html = html              #html页面
        self.time = time              #生成节点时间
        self.depth = depth            #页面深度
	HtmlModel.count += 1
 
    def __del__(self):
	HtmlModel.count -= 1

    def howmany(self):
	return HtmlModel.count
