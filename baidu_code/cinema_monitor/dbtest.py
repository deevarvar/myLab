#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import common
import MySQLdb
import database
import logging
import itertools

def FetchOneAssoc(cursor) :
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value
    return dict


def sql2json():
    offlinedb = 'instant_info_dq'
    third_from = 'dadi'
    cinemasql = 'SELECT third_id, third_from, cinemas_id,name FROM '+ offlinedb  +'.t_movie_poi WHERE cinemas_id != 0 AND third_from LIKE \'' + third_from + '\' limit 1'
    logging.debug('cinema sql is '+ cinemasql)
    cinemas_id = []
    try:
        db = database.database('local').get_connection()
        #print db
        curs = db.cursor()
        curs.execute(cinemasql)

        rows=curs.fetchall();
        desc = curs.description
        #print desc
        list = []

        for row in rows:

            print row
            print row[0]
            list.append(dict(itertools.izip([col[0] for col in desc],row)))

        for content in list:
            print content

        curs.close()
        db.close()

    except MySQLdb.Error as e:
        logging.error('mysql error msg is '+str(e))


def createTable():
    try:
        db = database.database('local').get_connection()
        db.select_db('instant_info_dq')
        curs = db.cursor()

        createsql = (
        "CREATE TABLE IF NOT EXISTS `t_movie_refund_order` ("
        "`id` bigint(12) NOT NULL AUTO_INCREMENT COMMENT '自增ID',"
  	"`movie_order_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '订单id',"
  "`seq_time` int(11) NOT NULL DEFAULT '0' COMMENT '场次开始时间',"
  "`third_order_id` varchar(50) NOT NULL DEFAULT '' COMMENT '第三方订单号',"
  "`third_from` varchar(20) NOT NULL DEFAULT '' COMMENT '第三方来源',"
  "`third_id` varchar(40) NOT NULL DEFAULT '' COMMENT '第三方影院id',"
  "`temp_third_order_id` varchar(36) NOT NULL DEFAULT '' COMMENT '第三方临时订单号',"
  "`sync_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '订单是否出票成功，0：未知，1：出票成功',"
  "PRIMARY KEY (`id`),"
  "UNIQUE KEY `order_id` (`movie_order_id`),"
  "KEY `seq_time` (`seq_time`)"
  ") ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='退款订单表' AUTO_INCREMENT=9 ;"

        )

        curs.execute(createsql)
       #INSERT INTO `instant_info_dq`.`t_movie_refund_order` (`id`, `movie_order_id`, `seq_time`, `third_order_id`, `third_from`, `third_id`, `temp_third_order_id`,`sync_status`) VALUES (NULL, '123', '1428589800', '20150409154610030103', 'dadi', '0001', '0', '1');
        insertsql = (
            "insert into t_movie_refund_order "
            " (`id`, `movie_order_id`, `seq_time`, `third_order_id`, `third_from`, `third_id`, `temp_third_order_id`,`sync_status`)"
            " Values (%(id)s, %(movie_order_id)s, %(seq_time)s, %(third_order_id)s, %(third_from)s, %(third_id)s, %(temp_third_order_id)s, %(sync_status)s)"


        )

        sampledata = {
            'id': '1',
            'movie_order_id' : '123',
            'seq_time': '12334567',
            'third_order_id': '456',
            'third_from': 'dadi',
            'third_id': '0001',
            'temp_third_order_id': '123',
            'sync_status': '0'
        }
        curs.execute(insertsql, sampledata)
        db.commit()
        curs.close()

        db.close()
    except MySQLdb.Error as e:
        logging.error('mysql error msg is ' + str(e))





sql2json()
#createTable()
