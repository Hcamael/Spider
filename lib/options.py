#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data import conf
from optparse import OptionParser
from optparse import OptionGroup
import sys
import os
import re

'''
设置, 初始化输入参数
'''
def OParser():
    parser = OptionParser()

    parser.add_option("--version", dest="showVersion",
                      action="store_true",
                      help="Show program's version number and exit")
    # 必选参数
    target = OptionGroup(parser, "Target", "At least one of these "
                                           "options has to be provided to define the target(s)")

    target.add_option("-u", dest="url", help="Target URL")
    target.add_option("-d", dest="deep", type="int", help="spider the depth")
    target.add_option("--testself", dest="test", action="store_true", help="auto test")

    # 可选参数
    opt = OptionGroup(parser, "Options", "Optional parameters")
    opt.add_option("-f", dest="logfile", help="The custom log file path")
    opt.add_option("--key", dest="key", help="Page keywords")
    opt.add_option("-l", dest="loglevel", type="int", help="log level(1-5) "
                                                        "1, CRITICAL; "
                                                        "2, ERROR(default); "
                                                        "3, WARN; "
                                                        "4, INFO; "
                                                        "5, DEBUG;")
    opt.add_option("--thread", dest="thread", type="int", help="thread number(default 10)")
    opt.add_option("--dbfile", dest="dbfile", help="set sqlite database file")

    parser.add_option_group(target)
    parser.add_option_group(opt)

    (args, _) = parser.parse_args(sys.argv)
    if not ((args.url and args.deep) or args.test):
        errMsg = "missing a mandatory option (-u, -d) or (--testself), "
        errMsg += "use -h for basic or -hh for advanced help"
        parser.error(errMsg)

    # 进行输入参数初始化
    conf['url'] = (args.url if args.url else "http://sina.com.cn")
    name = re.findall("[\w+\.]+", conf['url'])
    try:
        conf['name'] = (name[1] if len(name) == 2 else name[0])
    except IndexError:
        errMsg = "url input error!"
        parser.error(errMsg)

    conf['deep'] = (args.deep if args.deep else 2)
    conf['test'] = args.test
    conf['key'] = args.key
    conf['loglevel'] = (args.loglevel if args.loglevel else 2)
    conf['logfile'] = (os.path.basename(args.logfile) if args.logfile \
                                                    else 'spider.log' if args.test \
                                                                        else conf['name']+".log")
    conf['dbfile'] = (os.path.basename(args.dbfile) if args.dbfile else conf['name']+".db")
    conf['thread'] = (args.thread if args.thread else 10)
