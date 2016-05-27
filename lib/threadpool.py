#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import operate
import threading
import Queue
import time

class SiThread(threading.Thread):
    '''
    线程类
    '''
    def __init__(self, queue1, queue2, f):
        threading.Thread.__init__(self)
        self._queue = queue1
        self._result = queue2
        self._f = f

    def run(self):
        while True:
            url = self._queue.get()
            if url == 'stop':
                break
            r = self._f(url)
            if r['type'] == 'html':
                operate['db'].insert(r['html'], url)
            self._result.put(r)


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

        self._queue = Queue.Queue()
        self._result = Queue.Queue()
        self.pool = []
        self.num = num
        self.build_thread_pool(func)

    def _del(self):
        for x in xrange(self.num):
            self._queue.put('stop')

    def build_thread_pool(self, f):
        '''
        创建线程池
        :param f: 函数(非通用,仅支持单参数)
        :return: 线程池列表
        '''

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
            for a in arg:
                self._queue.put(a)
                result.append(self._result.get())

        return result
