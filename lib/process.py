#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import logger
import threading
import click

__author__ = "Hcamael"

class ShowProcess:
    '''
    每隔10s显示进度
    '''
    def __init__(self):
        '''
        初始化当前深度, 正常情况下是从0开始
        '''
        logger.info("init process~")
        print "=== 当前进度为："
        self.deep = 0
        self._pbar = click.progressbar(length=1, label="deep 0 : ")

    def __del__(self):
        print "=== The END!"

    def _run(self, length, queue):
        '''
        启动方法
        :param length: 当前深度爬取的URL长度
        :return: None
        '''
        self.deep += 1
        logger.info("begin run deep %s process bar, the length is %s" % (self.deep, length))
        label = "deep %s: " %(self.deep)

        # 结束上一个进度条
        self._finish_pbar()
        # 新建一个进度条
        self._pbar = click.progressbar(length=length, label=label, show_percent=False, show_pos=True)
        # 每隔10s显示一次进度
        timer = threading.Timer(0, self.timer, [queue, length])
        timer.start()

    def timer(self, queue, length):
        '''
        根据队列来判断进度
        :param queue: URL队列
        :param length: URL长度
        :return:
        '''
        bar = self._pbar
        if bar.finished:
            return
        else:
            logger.debug("complete: %s/%s" %(bar.length-queue.qsize(), bar.length))
            now_lenth = queue.qsize()
            bar.update(length-now_lenth)
            timer = threading.Timer(10, self.timer, [queue, now_lenth])
            timer.start()

    def _finish_pbar(self):
        '''
        结束上一个进度条
        :return:
        '''
        logger.info("deep %s over!" %(self.deep-1))
        self._pbar.finish()
        self._pbar.render_progress()
        self._pbar.render_finish()
