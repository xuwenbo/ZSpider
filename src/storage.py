#!/usr/bin/python

import Queue


class Storage(object):

    def __init__(self, dataQueue):
        self.dataQueue = dataQueue

    def start(self):
        print 'start storage...'
