#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import conf
from data import operate
from lib.data import logger
from bs4 import BeautifulSoup
from threadpool import ThreadPool
import requests
import signal
import re
import os

__author__ = "Hcamael"

class SpiderControl:
    '''
    爬虫控制类
    '''
    def __init__(self):
        '''
        初始化
        self.url 根url
        self.deep 爬取深度
        self.db 数据库操作类
        self._thread 线程池
        '''
        logger.info('init control class')
        self.url = conf['url']
        self.deep = conf['deep']
        self.db = operate['db']
        self._thread = ThreadPool(conf['thread'], self.get_html)

    def run(self):
        '''
        主控方法
        :return: None
        '''
        logger.info("start spider, and the spider deep is " + str(self.deep))
        self.url_group = []
        self.r_group = []
        self.recursion_deep()
        logger.info("The spider page total number is : " + str(len(self.url_group)))
        self._thread._del()
        logger.info("Spider OVER!!")

    def recursion_deep(self):
        '''
        根据深度值进行爬取
        operate['db'].deep 当前深度
        self.deep 需要爬取的深度
        :return:
        '''
        if operate['db'].deep == 0:
            logger.info("spidering deep == 0 page")
            r = self.get_html(self.url)
            try:
                html = r['html']
            except:
                print "url input error!"
                logger.error("url error(%s)" %(self.url))
                return

            operate['db'].insert(html, self.url)
            self.r_group.append(r)
            operate['db'].deep += 1
            self.recursion_deep()
        elif operate['db'].deep > self.deep:
            logger.info('spider deep over!')
            return
        else:
            logger.info("spidering deep = %s" %operate['db'].deep)
            tmp = []
            url_group = []

            # 从上一个deep爬取的页面中提取url
            for x in self.r_group:
                html = x['html']
                url_group.extend(self.find_url(html))
                logger.debug("from %s page find %s url" %(x['url'], len(url_group)))

            # 当页面没匹配出任何url, 则结束退出
            if url_group == []:
                return
            # 把提取出来的url丢入线程池中
            result_list = self._thread.my_map(url_group)
            for y in xrange(len(result_list)):
                if result_list[y]['type'] == 'html':
                    tmp.append(result_list[y])
                else:
                    logger.debug("delete the not html page (%s)" % url_group[y])

            self.r_group = tmp
            operate['db'].deep += 1
            self.recursion_deep()



    def find_url(self, html):
        '''
        使用BeautifulSoup找出网页中的url
        :param html: html页面
        :return: 返回一个list, 其值为html中url
        PS: 暂只考虑a标签中的href属性中的url
        '''
        url_group = []
        logger.debug("start find url in a html")
        try:
            bs = BeautifulSoup(html, 'lxml')
        except Exception, e:
            logger.error("bs4(html) fail!\nthe error info is : " + str(e))
            return

        comp = re.compile("^https?://[/\w\.-]*/?[\w&\+%=-]*")

        for x in bs.findAll('a'):
            try:
                if comp.match(x['href']):
                    logger.debug("%s match suc" %x['href'])
                    if x['href'] not in self.url_group:
                        url_group.append(x['href'])
            except KeyError:
                logger.debug(str(x) + " | <match href fail>")
                continue

        logger.debug("find %s url"%(len(url_group)))
        self.url_group.extend(url_group)
        return url_group

    def get_html(self, url):
        '''
        :return: {'type': url返回内容类型, 一般js和html页面中会含有url, 暂不处理js}
        '''

        header = {
            "User-Agent":
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"
        }
        result = {"type": None}
        logger.info("request a url: %s" %url)
        try:
            req = requests.get(url, headers=header, timeout=4)
        except Exception, e:
            try:
                logger.error("%s @@ requests fail and the info is %s" %(url.encode('utf-8'), e))
            except:
                print url
                print isinstance(url, unicode)
            return result

        if 'text/html' in req.headers['Content-Type']:
            logger.debug("get a html page: " + url)
            result['type'] = 'html'
            result['html'] = req.text
            result['url'] = url
        elif 'text/javascript' in req.headers['Content-Type']:
            logger.debug("get a js page: " + url)
            result['type'] = 'js'
            result['html'] = req.text
            result['url'] = url
        else:
            logger.warn("the page is not a html or a js("+url+")")

        return result
