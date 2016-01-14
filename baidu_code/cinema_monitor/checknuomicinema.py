#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import common
import MySQLdb
import database
from CheckAction import CheckAction
import sys
import logging
import itertools
import ConfigParser
import time
#1. get bid array
#2. analyze the url content


class CheckNuomiCinema():
    ARGS_NUM = 3

    def setLogOutput(self):
        debugfile =  self.csvdir + '/' + self.third_from + '_debug.log'
        #logging.getLogger("urllib3").setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
        #init the logging
        basiclog = logging.getLogger(common.NORMAL_LOG)
        basiclog.setLevel(logging.DEBUG)
        debugHandler = logging.FileHandler(debugfile, mode='w')
        debugHandler.setLevel(logging.DEBUG)
        debugHandler.setFormatter(formatter)
        basiclog.addHandler(debugHandler)
        info = logging.StreamHandler(sys.stdout)
        info.setLevel(self.level)
        info.setFormatter(formatter)
        basiclog.addHandler(info)
        return basiclog


    def __init__(self, dbconf,third_from, level=logging.INFO):
        self.dbconf = dbconf
        self.third_from = third_from
        self.cinemasinfo = []
        self.connection = None
        self.allcinemas = []
        self.level = level
        #this is all info need for result.csv
        self.curcinema = {
            "third_from": self.third_from,
            "third_id" : 0,
            "cinema_id" : 0,
            "name" : "empty",
            #info needed from CheckAction
            "bid" : 0,
            "encoded_bid" : 0,
            "cinema_url" : "",
            "movie_infos" : [],
            "timetable_url" : [],
            "planfrom" : [],
            "isValidCinema": 0
        }
        #choose the right db
        config = ConfigParser.ConfigParser()
        config.read(database.configfile)
        dbinfo = database.ConfigSectionMap(config, dbconf)
        self.dbinuse = dbinfo['moviedb']
        self.csvdir = './csv'
        os.system("mkdir -p " + self.csvdir )
        resultfile = self.csvdir + '/' + third_from + '_result.csv'
        pfile = self.csvdir + '/' + third_from + '_problem.csv'
        mfile = self.csvdir +'/' + third_from + '_missplan.csv'
        self.resultfile = resultfile
        self.pfile = pfile
        self.mfile = mfile

        self.log = self.setLogOutput()

        #clean up result.csv
        title = u'是否是合法影院,接入方, third_id, 影院名,影院id,bid, 加密bid, 影院url, 排期url, 排期来源,电影信息\n'
        with open(self.resultfile,'w+') as resultfile:
            resultfile.write(title.encode('utf-8'))
        with open(self.pfile,'w+') as problemfile:
            problemfile.write(title.encode('utf-8'))
        with open(self.mfile,'w+') as missfile:
            missfile.write(title.encode('utf-8'))

    def checkTimeTable(self, movie_info):
        for tt in movie_info:
            if tt['num'] == 0:
                self.log.warn(str(tt['id'])+'/'+tt['name'] + ' does not have plan!')
                return 1
        return 0

    def writeresult(self,cinemainfo):
        with open(self.resultfile, 'a+', buffering=-1) as resultfile:
            with open(self.pfile, 'a+', buffering=-1) as problemfile:
                with open(self.mfile, 'a+', buffering=-1) as mfile:

                    timetablestring = '\"'
                    for tt in cinemainfo['timetable_url']:
                        timetablestring += tt + '\n'
                    timetablestring += '\"'
                    moviestring = '\"'
                    for tt in cinemainfo['movie_infos']:
                        moviestring += str(tt['id']) + '/' + tt['name'] + '/' + str(tt['num']) +'\n'
                    moviestring += '\"'

                    planfromString = '\"'
                    for planfrom in cinemainfo['planfrom']:
                        planfromString += planfrom + '\n'
                    planfromString += '\"'

                    timeTableFlag = self.checkTimeTable(cinemainfo['movie_infos'])
                    noPlanFlag = 1
                    if self.third_from in cinemainfo['planfrom']:
                        noPlanFlag = 0
                    #print moviestring
                    oneline = str(cinemainfo['isValidCinema']) + ','  + str(cinemainfo['third_from']) + ', \'' + str(cinemainfo['third_id']) + ',' + cinemainfo['name'].encode('utf-8') \
                              + ', \'' +str(cinemainfo['cinema_id']) + ',' + '\''+ str(cinemainfo['bid']) + ','+ '\'' + str(cinemainfo['encoded_bid'])\
                              + ',' + cinemainfo['cinema_url']  + ','  + timetablestring.encode('utf-8') \
                              + ',' + str(planfromString) + ',' + moviestring.encode('utf-8') \
                              + '\n'
                    resultfile.write(oneline)

                    if cinemainfo['isValidCinema'] == 0 or noPlanFlag == 1:
                        problemfile.write(oneline)
                    if timeTableFlag == 1:
                        mfile.write(oneline)

    def check(self,cinemainfo):
        #FIXME: change instant_info_dq to instant_info to online verison
        cinema_id = cinemainfo['cinemas_id']
        name = cinemainfo['name']
        third_from = cinemainfo['third_from']
        third_id = cinemainfo['third_id']
        self.curcinema['name'] = name
        self.curcinema['third_id'] = third_id
        self.curcinema['third_from'] = third_from
        self.curcinema['cinema_id'] = cinema_id
        self.log.info('start to check cinema ' + name + ' , ' + str(third_id) + ',' + str(cinema_id))
        moreinfo = CheckAction(cinema_id, self.third_from, self.dbconf, self.dbinuse).run()
        if moreinfo:
            self.curcinema['bid'] = moreinfo['bid']
            self.curcinema['encoded_bid'] = moreinfo['encoded_bid']
            self.curcinema['cinema_url'] = moreinfo['cinema_url']
            self.curcinema['timetable_url'] = moreinfo['timetable_url']
            self.curcinema['planfrom'] = moreinfo['planfrom']
            self.curcinema['isValidCinema'] = moreinfo['isValidCinema']
            self.curcinema['movie_infos'] = moreinfo['movie_infos']
            #write result
            self.writeresult(self.curcinema)
            self.allcinemas.append(self.curcinema)

    def getCinemaInfo(self):
        cinemasql = 'SELECT third_id, third_from, cinemas_id,name FROM '+ self.dbinuse  +'.t_movie_poi WHERE cinemas_id != 0 AND poi_status = 0 AND third_from LIKE \'' + self.third_from + '\''
        self.log.debug('cinema sql is '+ cinemasql)
        cinemas_info = []
        try:
            db = database.database(self.dbconf).get_connection()
            self.connection = db
            #print db
            curs = db.cursor()
            curs.execute(cinemasql)
            rows=curs.fetchall();
            desc = curs.description
            for row in rows:
                cinemas_info.append(dict(itertools.izip([col[0] for col in desc],row)))
            curs.close()
        except MySQLdb.Error as e:
            self.log.error('mysql error msg is '+str(e))
        return cinemas_info


    def run(self):
        self.log.info('check '+self.third_from)
        self.cinemasinfo = self.getCinemaInfo()
        i = 0
        for cinemainfo in self.cinemasinfo:
            #only test part
            #if i == 1:
             #   break
            i = i + 1
            time.sleep(2)
            self.check(cinemainfo)



if __name__ == '__main__':
    #print len(sys.argv)
    if len(sys.argv) < CheckNuomiCinema.ARGS_NUM:
        print 'need db_name ,third_from name, loglevel(optional)'
    else:
        print 'check all cinemas from ' + sys.argv[2]
        if len(sys.argv) == (CheckNuomiCinema.ARGS_NUM + 1):
            check = CheckNuomiCinema(dbconf=sys.argv[1],third_from=sys.argv[2], loglevel=sys.argv[3])
        else:
            check = CheckNuomiCinema(dbconf=sys.argv[1],third_from=sys.argv[2])
        check.run()
        #check.connection.close()



