# coding: utf-8

import sys
import io
import os
import csv
import re
import datetime
import mysql.connector
from  mysql.connector import MySQLConnection, Error

# 這麼多defualt是因為如果不重新設定，在使用 reload函數時，print會被印在 terminal上。
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')

def ETL():
    """
    把最原始得資料拿來做ETL，頭尾不用的去掉，加入新的欄位名稱。
    
    """
    # create 'clean' folder  if not exist.
    if not os.path.exists('/Users/Jackie/Desktop/1101try/clean'):
        os.makedirs('/Users/Jackie/Desktop/1101try/clean')
    # from infiark1/ pick only files to do the trick.
    files=[]
    for f in os.listdir('/Users/Jackie/Desktop/1024testdir/'):
        if os.path.isfile('/Users/Jackie/Desktop/1024testdir/' + f):
            files.append(f)
    # chose only the csv files to ETL and rename it.
    for f in files:
        if '.csv' in f:
            with io.open('/Users/Jackie/Desktop/1024testdir/' + f, 'r', encoding='utf-8')as rfile:
                ff=[]
                for ele in rfile:
                    ff.append(ele)
                    
                # 檔案名字用VD的編號，從檔案內的第一欄抓出來
                fname = ff[2:-2][0].split(',')[0] 
                with io.open('/Users/Jackie/Desktop/1101try/clean/' + fname + '.csv', 'w', encoding='utf-8') as wfile:
                    wfile.write(u'''EQIPnumber,location,direct,YMD,hour,laneNumber,
                    addTotal,15Total,truckflow,carflow,scooterflow,avgspeed,avgPercent,avgCarSpace''' + u'\n')
                    # 去掉檔案裡上下不用的中文敘述，再把平均速度='-1'的值挑掉不要，最後是把原來檔案內的','跟'\n'去掉。
                    for ele in ff[2:-2]:
                        if ele.split(',')[-4] == '-1.0':
                            continue
                        else:
                            wfile.write(','.join(ele.split(' '))[:-2] + '\n')

ETL()