#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import conf
import sqlite3


class SpiderDb:
    '''

    '''
    def __init__(self):
        self.conn = sqlite3.connect(conf['dbfile'])
        self.cur = conn.cursor()
        check_table_sql = "select count(*) from sqlite_master where type='table' and name='spider'"
        cur.execute(check_table_sql)
        if cur.fetchone()[0] == 0:
            self.creab_table()

    '''
    建表
    固定表名/字段
    固定字段为id(int), html(text), deep(int)
    '''
    def creab_table(self, table_name="spider"):
        cb_sql = "CREATE TABLE spider (id INTEGER PRIMARY KEY autoincrement, html text, deep INTEGER)"
        self.cur.execute(cb_sql)
        self.conn.commit()


