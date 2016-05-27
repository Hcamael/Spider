#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib.data import conf
from lib import control
from lib.data import logger
from lib.data import operate
from lib.options import oparser
from lib.database import SpiderDb

__author__ = "Hcamael"

if __name__ == '__main__':
    logger.debug("Begin Spider")
    oparser()
    operate['db'] = SpiderDb(conf['dbfile'])
    c = control.SpiderControl()
    c.run()

