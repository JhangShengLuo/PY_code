# coding: utf-8

import sys
import io
import os
import csv
import re
import datetime
import mysql.connector
from  mysql.connector import MySQLConnection, Error


def direct_add():
    """
    這個函數要做的只是把剛剛整理好的資料，
    因為有些VD的紀錄裡有一種或兩種方向或是根本沒指定方向，
    全部歸納成只有一種方向，並在檔案名稱上加入方向，
    東西南北就是EWSN，未指定就是U。
    
    """
    # create 'done' folder if not exist.
    if not os.path.exists('/Users/Jackie/Desktop/1101try/done'):
        os.makedirs('/Users/Jackie/Desktop/1101try/done')
    # from 'clean' folder chose file that is csv.
    files=[]
    for f in os.listdir('/Users/Jackie/Desktop/1101try/clean/'):
        if os.path.isfile('/Users/Jackie/Desktop/1101try/clean/'+f):
            files.append(f)
    for f in files:
        if '.csv' in f:
            # empty list to temp store data and seperate by direct
            Ntemp=[]
            Stemp=[]
            Etemp=[]
            Wtemp=[]
            Utemp=[]
            ff=[]
            with io.open('/Users/Jackie/Desktop/1101try/clean/'+f,'r',encoding='utf-8')as rfile:
                for line in rfile:
                    ff.append(line)
                for ele in ff[1:]:
                    #  有些資料可能會寫成'往北''往南'或'向北''向南'，但是都一樣方向
                    if (ele.split(',')[2] == '往北')or(ele.split(',')[2] == '向北'):
                        Ntemp.append(ele)
                    elif (ele.split(',')[2] == '往南')or (ele.split(',')[2] == '向南'):
                        Stemp.append(ele)
                    elif (ele.split(',')[2] == '往東')or(ele.split(',')[2] == '向東'):
                        Etemp.append(ele)
                    elif (ele.split(',')[2] == '往西')or(ele.split(',')[2] == '向西'):
                        Wtemp.append(ele)
                    elif ele.split(',')[2] == '未指定':
                        Utemp.append(ele) 
            # 這裡的寫法是因為空list的bool值是false，有值的[]是true，以此去判斷。
            if Ntemp:
                with io.open('/Users/Jackie/Desktop/1101try/done/'+'N'+f,'w',encoding='utf-8') as nfile:
                    nfile.write(ff[0])
                    for ele in Ntemp:
                        nfile.write(ele)
            if Stemp:
                with io.open('/Users/Jackie/Desktop/1101try/done/'+'S'+f,'w',encoding='utf-8') as sfile:
                    sfile.write(ff[0])
                    for ele in Stemp:
                        sfile.write(ele)
            if  Etemp:
                with io.open('/Users/Jackie/Desktop/1101try/done/'+'E'+f,'w',encoding='utf-8') as efile:
                    efile.write(ff[0])
                    for ele in Etemp:
                        efile.write(ele)
            if Wtemp:
                with io.open('/Users/Jackie/Desktop/1101try/done/'+'W'+f,'w',encoding='utf-8') as wfile:
                    wfile.write(ff[0])
                    for ele in Wtemp:
                        wfile.write(ele)
            if Utemp:
                with io.open('/Users/Jackie/Desktop/1101try/done/'+'U'+f,'w',encoding='utf-8') as ufile:
                    ufile.write(ff[0])
                    for ele in Utemp:
                        ufile.write(ele)

direct_add()