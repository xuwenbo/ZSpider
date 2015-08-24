#!/usr/bin/python
# coding:utf-8

'''数据模型模块，UrlModel用于封装url数据，HtmlModel用于封装html数据,
   注：data队列中存放的是HtmlModel类的实例
   '''

class UrlModel(object):
    def __init__(self, url, parentUrl, time, depth):
        self.url = url              #url地址
        self.parentUrl = parentUrl  #父url
        self.time = time            #生成节点时间
        self.depth = depth          #页面深度


class HtmlModel(object):
    def __init__(self, url, html, time, depth):
        self.url = url              #url地址
        self.html = html            #html页面
        self.time = time            #生成节点时间
        self.depth = depth          #页面深度

