#!/usr/bin/python
# coding:utf-8

'''存储模块，用于从data队列中取出数据并存入sqlite数据库
   存储模块对外的接口即data队列，它只负责从data队列取出数据
   进行存储
   '''

import os
import time

import sqlite3

from mylogger import logger
from threadPool import WorkRequest


class Storage(WorkRequest):
    '''继承自线程池中的WorkRequest类，并实现线程执行函数'''
    def __init__(self, dbName, dataQueue, exitEvent):
        self.__dataQueue = dataQueue
        self.__exitEvent = exitEvent
        self.__dbName = dbName
        self.__dbPath = ''


    def __initDB(self):
        '''初始化数据库文件路径，并创建数据库'''
        try:
            dbDir = os.getcwd() + '/db/'
            if not os.path.exists(dbDir):
                os.makedirs(dbDir)
            self.__dbPath = dbDir + self.__dbName

            conn = sqlite3.connect(self.__dbPath)
            sqlCreateTable = '''CREATE TABLE IF NOT EXISTS zspider(
                         id integer primary key, url text, html text, time text, depth integer)'''
            conn.execute(sqlCreateTable)
            conn.close()
            logger.debug('Create database success.')
            return True
        except Exception, e:
            logger.error('Init database error : %s', str(e))
            return False


    def doWork(self):
        '''重写WorkRequest类的线程执行函数，此函数将在线程池中执行'''
        logger.debug('Start storage`s doWork...')
        if not self.__initDB():
            logger.error('Storage thread is stop.')
            return

        conn = sqlite3.connect(self.__dbPath)
        cur = conn.cursor()
        while True:
            try:
                # 从data队列获取数据并插入数据库
                if self.__dataQueue.qsize() > 0:
                    data = self.__dataQueue.get()
                    sqlInsert = '''INSERT INTO zspider(url, time, depth) VALUES ('%s', '%s', %d)''' % (data.url, data.time, data.depth)
                    cur.execute(sqlInsert)
                    conn.commit()
                else:
                    time.sleep(1)
            except Exception, e:
                logger.error('Database operate exception: %s ', str(e))
                continue
            # 检测退出事件
            if self.__exitEvent.is_set():
                cur.close()
                conn.close()
                logger.info('Storage model quit...')
                return


