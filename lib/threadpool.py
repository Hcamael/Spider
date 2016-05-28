#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import operate
from data import logger
from process import ShowProcess
import threading
import Queue
import time

stop = 0

class SiThread(threading.Thread):
    '''
    线程类
    '''
    def __init__(self, queue1, queue2, f):
        threading.Thread.__init__(self)
        self._queue = queue1
        self._result = queue2
        self._f = f
        logger.info('init a thread')

    def run(self):
        global stop

        logger.debug("run a thread")
        while True:
            url = self._queue.get()
            if url == 'stop':
                logger.info(str(threading.currentThread().ident) + " be stoped")
                break
            r = self._f(url)
            self._result.put(r)

class DbThread(threading.Thread):
    '''
    INSERT数据库线程
    '''
    def __init__(self, queue1):
        threading.Thread.__init__(self)
        logger.debug("init a database thread....")
        self._queue = queue1

    def run(self):
        global stop

        while True:
            r = self._queue.get()
            if r == 'stop':
                logger.info("database thread be stoped")
                break
            if r['type'] == 'html':
                operate['db'].insert(r['html'], r['url'])
            else:
                logger.warn("not a html page")


class ThreadPool:
    '''
    线程池 by Hcamael
    '''
    def __init__(self, num, func):
        '''
        self._queue 参数队列
        self._result 返回结果队列
        self.pool 线程池
        :param num: 线程数
        :param func: 函数
        '''
        logger.info("init a thread pool class")
        self._queue = Queue.Queue()
        self._result = Queue.Queue()
        self._dbqueue = Queue.Queue()
        self.pool = []
        self.num = num
        # 线程池
        self.build_thread_pool(func)
        # insert db 线程
        self.dbt = DbThread(self._dbqueue)
        self.dbt.start()
        # 显示进度
        self.process_bar = ShowProcess()

    def _del(self):
        global stop

        logger.info("destory thread pool")
        for x in self.pool:
            self._queue.put('stop')
        for t in self.pool:
            t.join()
        self._dbqueue.put('stop')
        self.dbt.join()
        logger.debug("destory thread pool suc")

    def build_thread_pool(self, f):
        '''
        创建线程池
        :param f: 函数(非通用,仅支持单参数)
        :return: 线程池列表
        '''
        logger.info("build thread pool, and the number is " + str(self.num))
        for x in xrange(self.num):
            pool = SiThread(self._queue, self._result, f)
            pool.start()
            self.pool.append(pool)

    def my_map(self, arg):
        '''
        自建一个map方法
        :param arg: 为一个列表, 值为传入f的参数
        :return: [f(arg[0]), f(arg[1])....]
        '''
        result = []

        if isinstance(arg, type([])):
            logger.debug("start a map function, and input the url number is %s" %(len(arg)))
            # 当一个深度结束再进行下一个深度? 要不然如何判断进度?
            while not self._queue.empty():
                print "wait..."
                pass
            for a in arg:
                    self._queue.put(a)
            self.process_bar._run(len(arg), self._queue)
            for a in arg:
                r = self._result.get()
                self._dbqueue.put(r)
                result.append(r)
            logger.debug("over a map function")
        else:
            logger.error("the arg is not a list!!!")
        return result
