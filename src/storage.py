#!/usr/bin/python
#coding:utf-8

import Queue
import sqlite3
import os
import time
import threading
from mylogger import logger


class Storage(object):

    def __init__(self,dbName, dataQueue):
        self.dataQueue = dataQueue
	self.thread = None
        self.dbName = dbName
        self.dbPath = ''


    def initDB(self):
        try:
	    #初始化数据库文件路径，并创建数据库
            dbDir = os.getcwd() + '/db/'
            if not os.path.exists(dbDir):
                os.makedirs(dbDir)
            self.dbPath = dbDir + self.dbName

            conn = sqlite3.connect(self.dbPath)
            sqlCreateTable = '''CREATE TABLE IF NOT EXISTS zspider(
                         id integer primary key, url text, html text, time text, depth integer)'''
            conn.execute(sqlCreateTable)
            conn.close()
	    logger.debug('create db success.')
            return True
        except Exception,e:
	    logger.error('init db error : %s', str(e))
            return False


    def storageThread(self):
        if not self.initDB():
            logger.error('storage thread is stop.')
            return 
            
        conn = sqlite3.connect(self.dbPath)
        while True:
            try:
		#从data队列获取数据并插入数据库
                if self.dataQueue.qsize() > 0:
                    data = self.dataQueue.get()
                    sqlInsert = '''INSERT INTO zspider(url, time, depth) VALUES ('%s', '%s', %d)''' % (data.url, data.time, data.depth)
                    conn.execute(sqlInsert)
                    conn.commit()
                else:
                    time.sleep(1)
            except Exception, e:
		logger.error('db operate exception: %s ', str(e))
                continue


    def start(self):
	#开启存储线程，此线程用于将data队列中的数据存储到数据库
        self.thread = threading.Thread(target = self.storageThread)
        self.thread.start()
	logger.info('storage thread is started...')



