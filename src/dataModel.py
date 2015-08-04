#!/usr/bin/python

class UrlModel(object):
    
    def __init__(self, url, parentUrl, time, depth):
        self.url = url
        self.parentUrl = parentUrl
        self.time = time
        self.depth = depth


class HtmlModel(object):

    def __init__(self, url, html, time, depth):
        self.url = url
        self.html = html
        self.time = time
        self.depth = depth
