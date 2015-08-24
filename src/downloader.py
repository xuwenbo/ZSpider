#!/usr/bin/python 
# coding:utf-8

'''下载模块用于从url队列中取出链接进行下载,并在下载完成后将html页面封装为内部
   数据格式放入html队列中以等待解析线程解析，
   
   下载模块与解析模块之间的关系：下载模块和解析模块互为生产者和消费者，下载模块
   从url队列取出数据进行消费，也生产html页面并放入html队列。解析模块从html队列
   取出数据消费，也生成url链接并放入url队列

   由于功能的划分，代码中将下载模块和解析模块独立分开，它们之间的接口仅为url队列
   和html队列两个容器。
   
   '''

import sys
import time
import random

import requests
from splinter import Browser

from mylogger import logger
from dataModel import HtmlModel
from helper import timestamp
from threadPool import WorkRequest
from config import *

reload(sys)
sys.setdefaultencoding("utf-8")


class Downloader(WorkRequest):
    '''继承自线程池中的WorkRequest类，并实现线程执行函数
       功能:用于从url队列取出链接进行下载并存入html队列
       '''
    def __init__(self, dlQueue, downloadMode, htmlQueue, exitEvent, downloadingFlag):
        self.__htmlQueue = htmlQueue
	# 下载队列，存放了主线程为其分配的url节点
        self.__dlQueue = dlQueue 
        self.__downloadMode = downloadMode
        self.__exitEvent = exitEvent
        self.__downloadingFlag = downloadingFlag


    def __isBigPage(self, url):
        '''判断页面(文件)大小，过滤较大页面(文件)'''
        try:
            response = requests.head(url)
            contentLen = response.headers['content-length']
            contentLen = int(contentLen)
            if contentLen > MAX_PAGE_SIZE:
		logger.warning('This is big page, Length : %d, URL : %s', contentLen, url)
                return True 
            return False 
        except Exception,e:
            return False 


    def __staticDownload(self, url):
        '''静态下载函数，使用requests模块进行下载'''
        if self.__isBigPage(url):
            return ""
        user_agent = random.choice(USER_AGENTS)
        headers = {'User-Agent': user_agent}
        try:
#            logger.debug('Downloading url : %s', url)
            response = requests.get(url, timeout=CONNECT_TIME_OUT, headers=headers)
            if response.status_code == 200:
                try:
                    # 再次判断文件大小，用于处理重定向链接
                    contentLen = response.headers['content-length']
                    contentLen = int(contentLen)
                    if contentLen > MAX_PAGE_SIZE:
			logger.warning('This is redirect page, before URL : %s, after URL : %s', url, response.url)
                        return ""
                except Exception,e:
                    pass

                page = response.text
                # 判断文件的实际大小，防止content-length与实际文件大小不符的情况
                if len(page) > MAX_PAGE_SIZE:
		    logger.warning('Downloaded big file, Length : %d , URL : %s', len(page), url)
                    return ""
                return page
            else:
                logger.warning('Download failed. status code : %d', response.status_code)
                return ""
        except Exception, e:
            logger.warning('Download exception (static): %s', str(e))
            return ""


    def __dynamicDownload(self, url):
        '''动态下载模块，使用了splinter模块、phantomjs模块(需单独安装)'''
        try:
#            logger.debug('Downloading url : %s', url)
            browser = Browser('phantomjs')
            browser.visit(url)
            html = browser.html
            browser.quit()
            return html
        except Exception, e:
            logger.warning('Download exception (dynamic): %s', str(e))
            return ""


    def __downloadPage(self, url):
        '''判断下载模式:静态下载/动态下载'''
        if self.__downloadMode == 0:
            return self.__staticDownload(url)
        elif self.__downloadMode == 1:
            return self.__dynamicDownload(url)


    def doWork(self):
        '''重写WorkRequest类的线程执行函数，此函数将在线程池中执行，
	   功能：从为自己分配的下载队列中取出url进行下载
	   '''
        logger.debug('Start downloader`s doWork...')
        while True:
            if self.__dlQueue.qsize() > 0:
                urlNode = self.__dlQueue.get()
                self.__downloadingFlag += 1
                page = self.__downloadPage(urlNode.url)
                if len(page) == 0:
                    self.__downloadingFlag -= 1
                    continue
#                logger.debug('download page success, url: %s', urlNode.url)
                # 将下载的html页面封装为内部数据格式并添加到html队列供解析模块解析
                htmlNode = HtmlModel(urlNode.url, page, timestamp(), urlNode.depth)
                self.__htmlQueue.put(htmlNode)
                self.__downloadingFlag -= 1
            # 检测退出事件
            if self.__exitEvent.is_set():
                logger.info('Download model quit...')
                return
            # 下载时间间隔
            time.sleep(FETCH_TIME_INTERVAL)


