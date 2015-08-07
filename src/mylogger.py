#!/usr/bin/python
#coding:utf-8

import logging
import os
from helper import timestamp


logDir = os.getcwd() + '/log/'
if not os.path.exists(logDir):
    os.makedirs(logDir)


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(logDir + timestamp() +'_zspider.log')
ch = logging.StreamHandler()

fh.setLevel(logging.DEBUG)
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
