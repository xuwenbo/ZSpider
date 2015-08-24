#!/usr/bin/python
# coding:utf-8

'''线程池模块，预先创建一定数量的线程并等待执行任务，鉴于实际需要，
   线程池中获取任务结果的功能由任务请求类自行实现

   用法： 1.创建一个请求类并从WorkRequest类继承,实现它的doWork方法(在此类中，用户可
            完成需要在线程中执行的任务)
	  2.创建一个ThreadPool实例，并调用它的putRequst方法将请求类的实例传递到线程池中执行
	  N.创建一定数量的新线程
	  N.停用一定数量的线程(并等待线程结束)
	  N.关闭线程池
	  
   例：   # 创建请求类，并从WorkRequest类继承，实现其中的doWork方法 
          class Requet(WorkRequest):
              def doWork(self):
	         print 'do work..'

	  # 创建线程池，并传入初始线程数 
          threadPool = ThreadPool(10)

          # 创建请求实例
          req = Requet()

          # 将请求实例传入线程池执行
	  threadPool.putRequest(req)

          # 让线程池再添加2个新线程
          threadPool.createWorkers(2)
	  
	  # 让线程池停用2个线程并等待线程结束
	  threadPool.dismissWorkers(2, True)
	  
	  # 关闭线程池并等待所有线程结束
	  threadPool.close(True)
   '''

import threading
import Queue

from mylogger import logger
from config import MAX_THREAD_NUM, MIN_THREAD_NUM


class WorkRequest(object):
    '''任务请求类，用户需从此类继承并实现doWork方法'''
    def doWork(self):
        pass



class WorkerThread(threading.Thread):
    '''工作线程类，由threading.Thread类派生'''
    def __init__(self, requestsQueue, pollTimeout = 5):
        threading.Thread.__init__(self)
	# 任务请求队列
        self.__requestsQueue = requestsQueue
        self.__pollTimeout = pollTimeout
        self.__dismissed = threading.Event()
        self.__isWorking = False
        self.setDaemon(True)
        self.start()
    

    def run(self):
	'''线程函数，工作线程在此函数中不断轮询任务队列，如果有任务则取出执行'''
        logger.debug('Work thread is running...')	
        while True:
	    # 检查停用事件
            if self.__dismissed.isSet():
                break
            try:
		# 从任务队列中获取WorkRequest实例
                request = self.__requestsQueue.get(True, self.__pollTimeout)
            except Queue.Empty:
                continue
           
            if self.__dismissed.isSet():
                self.__requestsQueue.put(request)
                break
            try:
		self.__isWorking = True
		# 执行请求实例的doWork方法
                request.doWork()
		self.__isWorking = False
            except Exception,e:
                pass


    def dismiss(self):
	'''停用此线程'''
        logger.debug('work thread is dismiss...')	
        self.__dismissed.set()

    
    def isBusy(slef):
	'''判断线程是否正在执行任务, True:忙碌 False:空闲'''
	return self.__isWorking



class ThreadPool(object):
    '''线程池类，提供对线程池的一系列管理操作,如创建线程、停用线程、等待线程结束、关闭线程池等'''
    def __init__(self, threadNum = 10, pollTimeout = 5):
	# 存放所有正在运行的线程对象
        self.__workers = []
	# 存放所有停用的线程对象
        self.__dismissedWorkers = []
	# 任务队列 
        self.__requestsQueue = Queue.Queue()
	self.__pollTimeout = pollTimeout
        self.createWorkers(threadNum, pollTimeout)
    
    
    def createWorkers(self, threadNum, pollTimeout):
	'''创建工作线程并将它们添加到线程池中'''
	logger.debug('Start create work thread...')
        for i in range(min(MAX_THREAD_NUM, threadNum)):
	    # 为工作线程传递任务队列
            self.__workers.append(WorkerThread(self.__requestsQueue, pollTimeout))


    def dismissWorkers(self, threadNum, doJoin = False):
	'''停用工作线程，doJoin为True则等待线程结束再返回,否则直接返回'''
	logger.debug('Dismiss worker thread, Num : %d ', threadNum)
        tmpList = []
        for i in range(min(threadNum, len(self.__workers))):
            worker = self.__workers.pop()
            worker.dismiss()
            tmpList.append(worker)

        if doJoin:
            for worker in tmpList:
                worker.join()
        else:
            self.__dismissedWorkers.extend(tmpList)
            

    def joinAllDismissedWorkers(self):
	'''等待所有停用线程结束运行'''
        for worker in self.__dismissedWorkers:
            Worker.join()
	logger.debug('All dismissed woker is quit...')
        self.__dismissedWorkers = []

    ''' 
    def __adjustmentThreadNum(self):
	# 动态调整线程数量，调整维度参考: 最大(小)线程数、繁忙线程数、空闲线程数、任务队列数
	workersNum = len(self.__workers)
	busyNum = 0
        for worker in self.__workers:
	    if worker.isBusy():
		busyNum += 1
        freeNum = workersNum - busyNum
	taskNum = self.__requestsQueue.qsize()

	# 如果当前任务队列有任务，则为它们创建新的工作线程(前提:不超过最大线程数) 
	if taskNum > 0:
	    for i in min(MAX_THREAD_NUM, workersNum + taskNum):
                self.__workers.append(WorkerThread(self.__requestsQueue, self.__pollTimeout))

	# 如果当前任务队列没有任务且空闲线程数超过繁忙线程数，则停用一半的空闲线程
        elif: taskNum == 0 and freeNum > busyNum:
	    dismissNum = max(MIN_THREAD_NUM, freeNum/2)
            self.dismissWorkers(taskNum)
    '''

    def putRequest(self, request):
	'''向线程池的任务队列添加新的任务'''
        assert isinstance(request, WorkRequest)
        assert getattr(request, 'doWork', None)
        self.__requestsQueue.put(request)


    def close(self, doJoin = False):
	'''关闭所有线程，doJoin为True则等待所有线程结束再返回，否则直接返回'''
        self.dismissWorkers(len(self.__workers) , doJoin)
        if doJoin:
            self.joinAllDismissedWorkers()
	logger.debug('All thread is quit...')


