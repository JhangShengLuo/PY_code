# coding: utf-8

import sys
import io
import os
import csv
import re
import datetime
import mysql.connector
from  mysql.connector import MySQLConnection, Error

def Gquery(info):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='1025try',
                                       user='root',
                                       password='apple')
        cursor = conn.cursor()
        query=[]
        if info == '舊宗':
            GNquery = ("""select NVQRTE00.direct,NVQRTE00.YMD,NVQRTE00.hour,NVQRTE00.15Total 
            ,rain.rain,rain.WD from NVQRTE00 join rain on NVQRTE00.YMD=rain.YMD;""")
            GSquery = ("""select SVQRTE00.direct,SVQRTE00.YMD,SVQRTE00.hour,SVQRTE00.15Total 
            ,rain.rain,rain.WD from SVQRTE00 join rain on SVQRTE00.YMD=rain.YMD;""")
            query.append(GNquery)
            query.append(GSquery)

            # Using the cursor as iterator
            
        elif info == '民權':
            MEquery = ("""select EVQEUU60.direct,EVQEUU60.YMD,EVQEUU60.hour,(EVQEUU60.15Total + EVQKWL60.15Total
            + EVQKWL61.15Total) 'total' ,rain.rain,rain.WD from EVQEUU60 join EVQKWL60 on 
            (EVQEUU60.YMD=EVQKWL60.YMD and EVQEUU60.hour=EVQKWL60.hour) join EVQKWL61 on 
            (EVQEUU60.YMD=EVQKWL61.YMD and EVQEUU60.hour=EVQKWL61.hour) join rain on EVQEUU60.YMD=rain.YMD;""")

            MWquery = ("""select WVQEUU60.direct,WVQEUU60.YMD,WVQEUU60.hour,(WVQEUU60.15Total + WVQKWL60.15Total
            + WVQKWL61.15Total) 'total' ,rain.rain,rain.WD from WVQEUU60 join WVQKWL60 on 
            (WVQEUU60.YMD=WVQKWL60.YMD and WVQEUU60.hour=WVQKWL60.hour) join WVQKWL61 on
            (WVQEUU60.YMD=WVQKWL61.YMD and WVQEUU60.hour=WVQKWL61.hour) join rain on WVQEUU60.YMD=rain.YMD;""")
            query.append(MEquery)
            query.append(MWquery)
            
        elif info == '堤頂':
            TNquery = ("""select NVRPSV70.direct,NVRPSV70.YMD,NVRPSV70.hour,(NVRPSV70.15Total + NVTXQL00.15Total
            + NVT5QV00.15Total + NVSPRA40.15Total + NVPMSV40.15Total + NVRPSV00.15Total) 'total' , 
            rain.rain,rain.WD from NVRPSV70 join NVTXQL00 on (NVRPSV70.YMD=NVTXQL00.YMD and 
            NVRPSV70.hour=NVTXQL00.hour) join NVT5QV00 on (NVRPSV70.YMD=NVT5QV00.YMD and
            NVRPSV70.hour=NVT5QV00.hour)join NVSPRA40 on (NVRPSV70.YMD=NVSPRA40.YMD and 
            NVRPSV70.hour=NVSPRA40.hour)join NVPMSV40 on (NVRPSV70.YMD=NVPMSV40.YMD and
            NVRPSV70.hour=NVPMSV40.hour)join NVRPSV00 on (NVRPSV70.YMD=NVRPSV00.YMD and
            NVRPSV70.hour=NVRPSV00.hour)join rain on NVRPSV70.YMD=rain.YMD;""")

            TSquery = ("""select SVTXQL00.direct,SVTXQL00.YMD,SVTXQL00.hour,(SVTXQL00.15Total + SVT5QV00.15Total
            + SVSPRA40.15Total + SVPMSV40.15Total + SVRPSV00.15Total) 'total' ,rain.rain,rain.WD from SVTXQL00
            join SVT5QV00 on  (SVTXQL00.YMD=SVT5QV00.YMD and SVTXQL00.hour=SVT5QV00.hour)join SVSPRA40 on 
            (SVTXQL00.YMD=SVSPRA40.YMD and SVTXQL00.hour=SVSPRA40.hour)join SVPMSV40 on 
            (SVTXQL00.YMD=SVPMSV40.YMD and SVTXQL00.hour=SVPMSV40.hour)join SVRPSV00 on 
            (SVTXQL00.YMD=SVRPSV00.YMD and SVTXQL00.hour=SVRPSV00.hour)join rain on SVTXQL00.YMD=rain.YMD;""")
            query.append(TNquery)
            query.append(TSquery)

           
        with io.open('/Users/Jackie/Desktop/1101try/'+info+'.csv','w',encoding='utf-8')as RDBque:
            RDBque.write(u"方向,日期,時間,當量總和,雨量,星期"+u'\n')
            for ele in query:
                cursor.execute(ele)
                for rows in cursor:
                    for ele in range(len(rows)):
                        if ele == len(rows)-1:
                            RDBque.write(format(rows[ele]).decode('utf-8')+u'\n')
                        else:
                            RDBque.write(format(rows[ele]).decode('utf-8')+u',')
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

Gquery('堤頂')
Gquery('舊宗')
Gquery('民權')
