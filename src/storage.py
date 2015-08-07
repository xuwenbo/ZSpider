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
            dbDir = os.getcwd() + '/db/'
            if not os.path.exists(dbDir):
                os.makedirs(dbDir)
            self.dbPath = dbDir + self.dbName

            conn = sqlite3.connect(self.dbPath)
            sqlCreateTable = '''CREATE TABLE IF NOT EXISTS zspider(
                         id integer primary key, url text, html text, time text, depth integer)'''
            conn.execute(sqlCreateTable)
            conn.close()
            return True
        except Exception,e:
            print 'init db failed.'
            return False


    def storageThread(self):
        if not self.initDB():
            print 'storage thread is stop.'
            return 
            
        conn = sqlite3.connect(self.dbPath)
        while True:
            try:
                if self.dataQueue.qsize() > 0:
                    data = self.dataQueue.get()
                    sqlInsert = '''INSERT INTO zspider(url, time, depth) VALUES ('%s', '%s', %d)''' % (data.url, data.time, data.depth)
#                    print sqlInsert
                    conn.execute(sqlInsert)
                    conn.commit()
                else:
                    time.sleep(1)
            except Exception, e:
                print 'insert db except : %s ' % str(e)
                continue


    def start(self):
        self.thread = threading.Thread(target = self.storageThread)
        self.thread.start()
	print 'storage thread is running'







