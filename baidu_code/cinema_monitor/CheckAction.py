__author__ = 'yezhihua'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO: add UT


import requests
import common
import os
from pyquery import PyQuery
import common
import time
import logging
import sys
import re
import MySQLdb
import database

class CheckAction():
    HTMLDIRBASE= "./html"
    TIMETABLEDIRBASE = "./timetable"
    def __init__(self, cinemaid, third_from, dbconf, dbinuse):
        self.cinemaid = cinemaid
        self.dbconf = dbconf
        self.dbinuse = dbinuse
        self.connection = None
        self.bid = 0
        self.encoded_bid = 0
        self.htmlname = ''
        self.movieinfos = []
        self.htmldir = self.HTMLDIRBASE + '/'+ third_from + '/'+ str(cinemaid)
        self.timetabledir =  self.TIMETABLEDIRBASE + '/' + third_from + '/' + str(cinemaid)
        self.result = {
            "bid" : 0,
            "encoded_bid" : 0,
            "cinema_url" : "",
            'movie_infos': [],
            "planfrom" : [],
            "timetable_url" : [],
            "isValidCinema": 0

        }
        self.log = logging.getLogger(common.NORMAL_LOG)

        os.system("mkdir -p " + self.htmldir )
        os.system("mkdir -p " + self.timetabledir )
        os.environ["TZ"] = "Asia/Shanghai"
        time.tzset()

    def getBid(self):
        cinemaid = self.cinemaid
        cinemasql = 'SELECT bid FROM '+ self.dbinuse  +'.t_movie_cinemas WHERE cinemas_id = ' + str(cinemaid) + ' and status = 1'
        try:
            db = database.database(self.dbconf).get_connection()
            self.connection = db
            curs = db.cursor()
            curs.execute(cinemasql)
            rows=curs.fetchone();
            for row in rows:
                bid = row
                #do the check
                self.bid = bid
                self.result['bid'] = bid
            curs.close()
            return 0
        except MySQLdb.Error as e:
            self.log.error('mysql error msg is '+str(e))
        return 1

    def getHtml(self):
        encode = common.encodebid(self.bid)
        cinemaurl = common.NUOMI_PREFIX+str(encode)
        self.log.info('cinema url is '+cinemaurl)
        self.encoded_bid = encode
        self.result['encoded_bid'] = encode
        self.result['cinema_url'] = cinemaurl
        try:
            rsp = requests.get(cinemaurl)

            redirect = 0
            for his in rsp.history:
                if his.status_code == 302:
                    redirect = 1
                    break
            if redirect == 0:
                htmlfile = self.htmldir + '/'+str(self.cinemaid)+'.html'
                with open(htmlfile,'w+') as hfile:
                    hfile.write(rsp.content)
                    self.htmlname = htmlfile
                    return 0
            else:
                self.log.info(cinemaurl + 'rsp is 302, move temporarily!')
                return 1
        except requests.exceptions.RequestException as e:    # This is the correct syntax
            self.log.error(e)
            return 1

    def getThirdFrom(self, link):
        third_from_pattern = '.*third_from=(?P<third_from>(.*))'
        m = re.search(third_from_pattern, link)
        if m is not None:
            third_from = m.group('third_from')
            self.log.debug(' thirdfrom is '+third_from)
            if third_from not in self.result['planfrom']:
                self.result['planfrom'].append(third_from)
        else:
            self.log.error(link + 'does not have a valid third_from!')

    def getSeqno(self):
        pass

    def getmovieids(self):
        #print self.htmlname
        if len(self.htmlname) != 0:
            jquery = PyQuery(filename=self.htmlname)
            length = jquery('.j-img-wrapper').length
            if length > 0:
                self.result['isValidCinema'] = 1
                for index in range(0,length):
                    movieid = jquery('.j-img-wrapper').eq(index).attr('movieid')
                    name = jquery('.j-img-wrapper img').eq(index).attr('alt')
                    movieinfo = {}
                    movieinfo['id'] = movieid
                    movieinfo['name'] = name
                    self.log.debug(movieinfo['id']+ '/' + movieinfo['name'])
                    self.movieinfos.append(movieinfo)
                self.result['movie_infos'] = self.movieinfos
                return 0
            else:
                self.log.info(str(self.cinemaid) + ' is not cinema.')
                self.result['isValidCinema'] = 0

                return 1
        return 1

    def getTimetable(self):
        timetableurls = []
        movieids = []
        for movieinfo in self.movieinfos:
            second = common.getSeconds()
            movieid = movieinfo['id']
            moviename = movieinfo['name']
            turl = common.TIMETABLE_URL + 'cinemaid='+ str(self.encoded_bid) + '&mid=' + movieid + '&needMovieInfo=1&tploption=1&_=' + second
            self.log.debug('timetable url is '+ turl)
            self.log.info('start to check plan for ' + moviename)
            timetableurls.append(turl)
            movieids.append(movieid)
            #get page
            try:
                rsp = requests.get(turl)
                timetablefile = self.timetabledir + '/'+str(movieid)+'.html'
                with open(timetablefile,'w+') as hfile:
                    hfile.write(rsp.content)
                jquery = PyQuery(filename=timetablefile)
                length = jquery('.btn-choose-seat').length
                movieinfo['num'] = length
                if length == 0:
                    self.log.warn(str(self.cinemaid) + ' does not have plans for movie ' + moviename)
                for index in range(0,length):
                    link = jquery('.btn-choose-seat').eq(index).attr('href')
                    self.log.debug('movie link is '+link)
                    self.getThirdFrom(link)

                self.result['timetable_url'] = timetableurls
            except requests.exceptions.RequestException as e:
                self.log.error(e)


    def checkplan(self):
        pass


    def run(self):
        if(self.getBid() != 1):
            if(self.getHtml() != 1):
                if(self.getmovieids() != 1):
                    self.getTimetable()
            else:
                self.log.info(str(self.cinemaid) + ' is not place.')
                self.result['isValidCinema'] = 0
            self.log.debug(self.result)
            return self.result
        return []

#3574080d5096fa5a774ff1e0
#CheckAction('3574080d5096fa5a774ff1e0').run()
#CheckAction('123').run()

if __name__ == '__main__':
    if len(sys.argv) == 5:
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        #init the logging
        logging.basicConfig(filename='./singlecheck.log', level = logging.DEBUG)
        logging.FileHandler('./singlecheck.log', mode='w')
        root = logging.getLogger()
        info = logging.StreamHandler(sys.stdout)
        info.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
        info.setFormatter(formatter)
        root.addHandler(info)
        CheckAction(cinemaid = sys.argv[1], third_from = sys.argv[2],dbconf = sys.argv[3] ,dbinuse = sys.argv[4]).run()
    else:
        logging.error('missing cinemaid , third_from, dbconf, dbinuse')
        logging.error('example: python CheckAction.py 8350 dadi local instant_info_dq')