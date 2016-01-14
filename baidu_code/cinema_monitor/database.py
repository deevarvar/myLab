__author__ = 'yezhihua'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import MySQLdb

import ConfigParser


configfile = os.path.abspath(os.path.dirname(__name__)) + '/config.ini'
'''
class Singleton:
  """
  http://www.mindviewinc.com/Books/Python3Patterns/Index.php
  """
  def __init__(self, klass):
    self.klass = klass
    self.instance = None
  def __call__(self, *args, **kwds):
    if self.instance == None:
      self.instance = self.klass(*args, **kwds)
    return self.instance
'''

def ConfigSectionMap(config,section):
    dict1 = {}
    options = config.options(section)
    #print options
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

#do not need this decorator
#@Singleton
class database():
    connection = None

    def __init__(self, db):
        self.host = db

    def get_connection(self):
        if self.connection is None:
            config = ConfigParser.ConfigParser()
            config.read(configfile)
            dbinfo=ConfigSectionMap(config, self.host)
            #print dbinfo["host"]+ " " + dbinfo["user"] + " " + dbinfo["passwd"]
            #print int(dbinfo["port"])
            port=int(dbinfo['port'])
            self.connection=MySQLdb.connect(host=dbinfo["host"],user=dbinfo["user"], passwd=dbinfo["passwd"],port=port,charset='utf8')
            return self.connection
        else:
            return self.connection