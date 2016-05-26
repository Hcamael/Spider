#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sqlite3

conn = sqlite3.connect('test.db')

c = conn.cursor()

c.execute("CREATE TABLE spider (id int, html text, deep int)")

conn.commit()

conn.close()
	