#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import conf
from data import operate
from bs4 import BeautifulSoup
import requests
import re

__author__ = "Hcamael"

class SpiderControl:
    '''
    爬虫控制类
    '''
    def __init__(self):
        '''
        初始化
        '''
        self.url = conf['url']
        self.deep = conf['deep']
        self.key = conf['key']
        self.db = operate['db']

    def run(self):
        '''
        主控方法
        :return: None
        '''

        self.url_group = []
        self.r_group = []
        deep = 0

        r = self.get_html()
        html = r['html']
        operate['db'].insert(html, self.url, deep)
        self.r_group.append(r)

        # 根据深度值进行爬取
        while self.deep:
            deep += 1
            for x in self.r_group:
                tmp = []
                html = r['html']
                self.find_url(html)
                for y in self.url_group:
                    self.url = y
                    r = self.get_html()
                    if r['type'] == 'html':
                        operate['db'].insert(r['html'], self.url, self.deep)
                        tmp.append(r)

            self.r_group = tmp
            self.deep -= 1

    def find_url(self, html):
        '''
        使用BeautifulSoup找出网页中的url
        :param html: html页面
        PS: 暂只考虑a标签中的href属性中的url
        '''
        bs = BeautifulSoup(html, 'lxml')
        comp = re.compile("^(https?://)?[/\w\.-]*\?[\w&\+%=-]*")

        for x in bs.findAll('a'):
            try:
                if comp.match(x['href']):
                    if x['href'] not in self.url_group:
                        self.url_group.append(x['href'])
            except KeyError:
                continue

    def get_html(self):
        '''
        :return: {'type': url返回内容类型, 一般js和html页面中会含有url, 暂不处理js}
        '''

        header = {
            "User-Agent":
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"
        }
        result = {"type": None}

        req = requests.get(self.url, headers=header)
        if 'text/html' in req.headers['Content-Type']:
            result['type'] = 'html'
            result['html'] = req.text
        elif 'text/javascript' in req.headers['Content-Type']:
            result['type'] = 'js'
            result['html'] = req.text

        return result
