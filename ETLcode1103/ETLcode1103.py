
# coding: utf-8

# In[10]:



import time
import shutil
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

cs = time.strftime('%Y/%m/%d_%H:%M:%S',time.localtime())
print cs
# 存粹看運算時間

def ETL():
    """
    把最原始得資料拿來做ETL，頭尾不用的去掉，加入新的欄位名稱。
    
    """
    try:
        # create 'clean' folder  if not exist.
        if not os.path.exists('/Users/Jackie/Desktop/ETLcode1103/clean'):
            os.makedirs('/Users/Jackie/Desktop/ETLcode1103/clean')
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
                    with io.open('/Users/Jackie/Desktop/ETLcode1103/clean/' + fname + '.csv', 'w', encoding='utf-8') as wfile:
                        wfile.write(u'''EQIPnumber,location,direct,YMD,hour,laneNumber,
                        addTotal,15Total,truckflow,carflow,scooterflow,avgspeed,avgPercent,avgCarSpace''' + u'\n')
                        # 去掉檔案裡上下不用的中文敘述，再把平均速度='-1'的值挑掉不要，最後是把原來檔案內的','跟'\n'去掉。
                        for ele in ff[2:-2]:
                            if ele.split(',')[-4] == '-1.0':
                                continue
                            else:
                                wfile.write(','.join(ele.split(' '))[:-2] + '\n')
    except:
        with open('/Users/Jackie/Desktop/ETLcode1103/ETL.txt','w') as here3:
            here3.write(u'ETL exception'+u'\n')
            here3.write(str(sys.stderr)+u'\n')
            here3.write(str(sys.exc_info()[0])+u'\n')
            here3.write(str(sys.exc_info()[1])+u'\n')
            here3.write(str(sys.exc_info()[2])+u'\n')
        
                            
                            
def direct_add():
    """
    這個函數要做的只是把剛剛整理好的資料，
    因為有些VD的紀錄裡有一種或兩種方向或是根本沒指定方向，
    全部歸納成只有一種方向，並在檔案名稱上加入方向，
    東西南北就是EWSN，未指定就是U。
    
    """
    try:
        # create 'done' folder if not exist.
        if not os.path.exists('/Users/Jackie/Desktop/ETLcode1103/done'):
            os.makedirs('/Users/Jackie/Desktop/ETLcode1103/done')
        # from 'clean' folder chose file that is csv.
        files=[]
        for f in os.listdir('/Users/Jackie/Desktop/ETLcode1103/clean/'):
            if os.path.isfile('/Users/Jackie/Desktop/ETLcode1103/clean/'+f):
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
                with io.open('/Users/Jackie/Desktop/ETLcode1103/clean/'+f,'r',encoding='utf-8')as rfile:
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
                    with io.open('/Users/Jackie/Desktop/ETLcode1103/done/'+'N'+f,'w',encoding='utf-8') as nfile:
                        nfile.write(ff[0])
                        for ele in Ntemp:
                            nfile.write(ele)
                if Stemp:
                    with io.open('/Users/Jackie/Desktop/ETLcode1103/done/'+'S'+f,'w',encoding='utf-8') as sfile:
                        sfile.write(ff[0])
                        for ele in Stemp:
                            sfile.write(ele)
                if  Etemp:
                    with io.open('/Users/Jackie/Desktop/ETLcode1103/done/'+'E'+f,'w',encoding='utf-8') as efile:
                        efile.write(ff[0])
                        for ele in Etemp:
                            efile.write(ele)
                if Wtemp:
                    with io.open('/Users/Jackie/Desktop/ETLcode1103/done/'+'W'+f,'w',encoding='utf-8') as wfile:
                        wfile.write(ff[0])
                        for ele in Wtemp:
                            wfile.write(ele)
                if Utemp:
                    with io.open('/Users/Jackie/Desktop/ETLcode1103/done/'+'U'+f,'w',encoding='utf-8') as ufile:
                        ufile.write(ff[0])
                        for ele in Utemp:
                            ufile.write(ele)
    except:
        with open('/Users/Jackie/Desktop/ETLcode1103/direct_add.txt','w') as here3:
            here3.write(u'direct_add exception'+u'\n')
            here3.write(str(sys.stderr)+u'\n')
            here3.write(str(sys.exc_info()[0])+u'\n')
            here3.write(str(sys.exc_info()[1])+u'\n')
            here3.write(str(sys.exc_info()[2])+u'\n')
        
def insert_data():
    """
    主要是使用連結資料庫的第三方套件mysql.connector，
    以python去對資料庫做連結，在利用for loop把資料insert到正確的table下。
    
    """
    try:
        # 連結資料庫的第三方套件
        cnx = mysql.connector.connect(user='root', password='apple', database='VDDB')
        cursor = cnx.cursor()
        files = []
        for f in os.listdir('/Users/Jackie/Desktop/ETLcode1103/done/'):
            if os.path.isfile('/Users/Jackie/Desktop/ETLcode1103/done/' + f):
                files.append(f)
        replace2 = []
        for f in files:
            if '.csv' in f:
                #利用正規表達式，從檔名去找table名
                match = re.findall('[A-Z0-9]+', f)
                tablename = str(match[0])
                # 讀取要寫入的檔案
                with io.open('/Users/Jackie/Desktop/ETLcode1103/done/' + f, 'r', encoding='utf-8') as rcsv:
                    content = []
                    for line in rcsv:
                        content.append(line)
                    # 不要欄位名稱，所以要先將內容放在一個list，在取資料時，直接放棄第一筆[1:]
                    for element in content[1:]:
                        #不需要第一行標題 [1:]
                        #先用list再轉成tuple
                        mylist=[tablename,]
                        for ele in element.split(','):
                            mylist.append(str(ele).strip())
                        #轉成tuple
                        mytuple = tuple(mylist)
                        replace2.append(mytuple) 
        #這裡要注意的是'{r[1]}','{r[2]}'...等等到r5要加引號是因為在query時就要加''號，因為'00:00:00'沒加''會出錯！！！
        for ele in replace2:         
            query = ('''insert into {r[0]} (EQIPnumber,location,direct,YMD,hour,laneNumber,addTotal,15Total,
        truckflow,carflow,scooterflow,avgspeed,avgPercent,avgCarSpace)values
        ('{r[1]}','{r[2]}','{r[3]}','{r[4]}','{r[5]}',{r[6]},{r[7]},{r[8]},
        {r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]});'''.format(r=ele))
            cursor.execute(query)
            cnx.commit()
        cursor.close()
        cnx.close()
    except:
        with open('/Users/Jackie/Desktop/ETLcode1103/insert_data.txt','w') as here3:
            here3.write(u'insert_data exception'+u'\n')
            here3.write(str(sys.stderr)+u'\n')
            here3.write(str(sys.exc_info()[0])+u'\n')
            here3.write(str(sys.exc_info()[1])+u'\n')
            here3.write(str(sys.exc_info()[2])+u'\n')


def query():
    """
    1027ETL改正版，原先的query太多筆，所以現在將要查詢的table整個寫成一個list
    
    """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='VDDB',
                                       user='root',
                                       password='apple')
        cursor = conn.cursor()
        # 將要查詢的table以及所屬道路寫成list，方便印出也可以用在query上。
        Tablename=['UVSSWC60,成功路3段','NVQ6WK40,成功路2段','SVQ6WK40,成功路2段','NVQKWL40,成功路2段',                   'SVQKWL40,成功路2段','SVQKWL00,成功路2段','NVQKWL00,成功路2段','SVQRTE00,舊宗路2段',                   'NVQRTE00,舊宗路2段','SVSNRE00,瑞光路','NVSNRE00,瑞光路','NVS6TI00,瑞光路','SVS6TI00,瑞光路',                   'EVQEUU60,民權東路六段','EVQKWL60,民權東路六段','EVQKWL61,民權東路六段','WVQEUU60,民權東路六段',                   'WVQKWL60,民權東路六段','WVQKWL61,民權東路六段','NVS9TE00,港墘路','SVS9TE00,港墘路',                   'NVRPSV00,堤頂大道1段','SVRPSV00,堤頂大道1段','NVPMSV40,堤頂大道1段','SVPMSV40,堤頂大道1段',                   'NVT5QV00,堤頂大道2段','SVT5QV00,堤頂大道2段']
        # 開一個csv檔寫入
        with io.open('/Users/Jackie/Desktop/ETLcode1103/allappend.csv','w',encoding='utf-8')as RDBque:
            # 寫欄位名稱
            RDBque.write("VD編號,道路,位置,道路數,方向,日期,時間,當量,平均速度,平均佔有率,平均車間距,星期"+u'\n')
            i=0
            for ele in Tablename:
                table=[]
                table.append(ele.split(',')[0])
                # 這裡query的寫法參照format的特殊用法，https://pyformat.info/
                select_join=("""select {r[0]}.location,{r[0]}.lanenumber,{r[0]}.direct,{r[0]}.YMD,{r[0]}.hour,
                {r[0]}.15Total  ,{r[0]}.avgspeed ,{r[0]}.avgpercent , {r[0]}.avgCarSpace ,rain.WD from {r[0]} 
                join rain on {r[0]}.YMD=rain.YMD;""".format(r=table))
                cursor.execute(select_join)
                # Using the cursor as iterator
                i+=1
                # 不喜歡用fetchone，fetchmany，fetchall直接取cursor
                for rows in cursor:
                    RDBque.write(Tablename[i-1][1:]+u',')
                    for element in range(len(rows)):
                        #  如果element是最後一個元素，就寫入換行
                        if element == len(rows)-1:
                            RDBque.write(format(rows[element]).decode('utf-8')+u'\n')
                        elif rows[element] == """成功路(文德路-金龍路)-成功路3段152號前路燈桿(已附掛市警局CCTV)""":
                            RDBque.write(u'成功路3段152號前路燈桿'+u',')
                        else:
                            RDBque.write(format(rows[element]).decode('utf-8')+u',')
        
    except Error as e:
        print(e)
        with open('/Users/Jackie/Desktop/ETLcode1103/query.txt','w') as here3:
            here3.write(u'query exception'+u'\n')
            here3.write(str(sys.stderr)+u'\n')
            here3.write(str(sys.exc_info()[0])+u'\n')
            here3.write(str(sys.exc_info()[1])+u'\n')
            here3.write(str(sys.exc_info()[2])+u'\n')

    finally:
        cursor.close()
        conn.close()


# In[11]:

def move_to_hist_dir():
    try:
        ct=time.strftime('%Y%m%d',time.localtime())
        if not os.path.exists('/Users/Jackie/Desktop/1025hist/'+ct):
            os.makedirs('/Users/Jackie/Desktop/1025hist/'+ct)
        for root,dirs,files in os.walk('/Users/Jackie/Desktop/1024testdir/'):
            for ele in files:
                if '.csv' in ele:
                    print ele
                    shutil.move('/Users/Jackie/Desktop/1024testdir/'+ele,'/Users/Jackie/Desktop/1025hist/'+ct+'/')
    except:
        with open('/Users/Jackie/Desktop/ETLcode1103/move_to_hist_dir.txt','w') as here3:
            here3.write(u'move_to_hist_dir exception'+u'\n')
            here3.write(str(sys.stderr)+u'\n')
            here3.write(str(sys.exc_info()[0])+u'\n')
            here3.write(str(sys.exc_info()[1])+u'\n')
            here3.write(str(sys.exc_info()[2])+u'\n')


# In[12]:

ETL()
move_to_hist_dir()
direct_add()
insert_data()
query()
cs = time.strftime('%Y/%m/%d_%H:%M:%S',time.localtime())
print cs
# 存粹看運算時間






