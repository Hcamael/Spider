#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import conf
import sqlite3

__author__ = "Hcamael"

class SpiderDb:
    '''
    数据库操作类
    '''
    def __init__(self, dbfile):
        '''
        初始化
        :param dbfile: sqlite3 数据库文件
        '''
        self.deep = 0
        dbfile = "db/" + dbfile
        self.conn = sqlite3.connect(dbfile, check_same_thread=False)
        self.cur = self.conn.cursor()
        check_table_sql = "select count(*) from sqlite_master where type='table' and name='spider'"
        self.cur.execute(check_table_sql)
        if self.cur.fetchone()[0] == 0:
            self.creab_table()

    def __del__(self):
        '''
        销毁
        '''
        self.conn.commit()
        self.conn.close()

    def creab_table(self):
        '''
        建表
        固定表名/字段
        固定字段为id(int), html(text), url(text), deep(int), keyword(text)
        '''
        cb_sql = "CREATE TABLE spider (id INTEGER PRIMARY KEY autoincrement, html text, url text, deep INTEGER, keyword text)"
        self.cur.execute(cb_sql)
        self.conn.commit()

    def insert(self, html, url):
        '''
        必须参数
        :param html: 抓取的页面内容
        :param url: 抓取页面的url
        :param deep: 该页面的深度
        :return:
        '''
        in_sql = "INSERT INTO spider VALUES (null, ?, ?, ?, ?)"
        # 当设置了关键词然后关键词不在页面中时
        if conf['key'] and conf['key'] not in html:
            return None

        keyword = (conf['key'] if conf['key'] else '')
        self.cur.execute(in_sql, (html, url, self.deep, keyword))
        self.conn.commit()
