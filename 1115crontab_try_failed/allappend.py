# coding: utf-8

import sys
import io
import os
import csv
import re
import datetime
import mysql.connector
from  mysql.connector import MySQLConnection, Error

def allappend():

    allappend=[]
    allappend.append(u'道路'+u','+u'方向,日期,時間,當量總和,雨量,星期\n')
    for root,dirs,files in os.walk('/Users/Jackie/Desktop/1101try/'):
        for f in files:
            if '堤頂.csv' == f:
    #             print f
                with io.open('/Users/Jackie/Desktop/1101try/'+"堤頂.csv",'r',encoding ='utf-8') as rfile:
                    temp = []
                    for line in rfile:
                        temp.append(line)
                    for ele in temp[1:]:
                        allappend.append(u'堤頂'+u','+ele)
            if '民權.csv' == f:
    #             print f

                with io.open('/Users/Jackie/Desktop/1101try/'+"民權.csv",'r',encoding ='utf-8') as rfile:
                    temp = []
                    for line in rfile:
                        temp.append(line)
                    for ele in temp[1:]:
                        allappend.append(u'民權'+u','+ele)
            if '舊宗.csv' == f:
    #             print f
                with io.open('/Users/Jackie/Desktop/1101try/'+"舊宗.csv",'r',encoding ='utf-8') as rfile:
                    temp = []
                    for line in rfile:
                        temp.append(line)
                    for ele in temp[1:]:
                        allappend.append(u'舊宗'+u','+ele)


    with io.open('/Users/Jackie/Desktop/1101try/allappend.csv','w',encoding='utf-8')as wfile:
        for ele in allappend:
            wfile.write(ele)

allappend()