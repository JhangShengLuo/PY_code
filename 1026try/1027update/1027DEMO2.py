
# coding: utf-8

# # 全部的程式碼連接在一起試跑看看

# In[ ]:




# In[21]:

#!/usr/bin/env python


# 原始檔更換欄位名稱，及頭尾去掉

import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')

import csv,io
import os
     
if not os.path.exists('done'):
    os.makedirs('done')
    
files=[]
for f in os.listdir('./infiark1/'):
    if os.path.isfile('./infiark1/'+f):
        files.append(f)
for f in files:
    if '.csv' in f:
        with io.open('infiark1/'+f,'r',encoding='utf-8')as rfile:
            ff=[]
            for ele in rfile:
                ff.append(ele)
#                 檔案名字用VD的編號
            fname = ff[2:-2][0].split(',')[0]
            with io.open('done/'+fname+'.csv','w',encoding='utf-8') as wfile:
                wfile.write(u'''EQIPnumber,location,direct,YMD,hour,laneNumber,addTotal,15Total,truckflow,carflow,scooterflow,avgspeed,avgPercent,avgCarSpace'''+u'\n')
                for ele in ff[2:-2]:
                    if ele.split(',')[-4] == '-1.0':
                        continue
                    else:
                        wfile.write(','.join(ele.split(' '))[:-2]+'\n')
                


# In[22]:

# 把方向自動分成東西南北跟未指定

import csv,io
import os

if not os.path.exists('clean'):
    os.makedirs('clean')


files=[]
for f in os.listdir('./done/'):
    if os.path.isfile('./done/'+f):
        files.append(f)
for f in files:
    if '.csv' in f:
        Ntemp=[]
        Stemp=[]
        Etemp=[]
        Wtemp=[]
        Utemp=[]
        ff=[]
        with io.open('./done/'+f,'r',encoding='utf-8')as rfile:
            for line in rfile:
                ff.append(line)
            for ele in ff[1:]:
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
#                 這裡挑出方向之後在VD編號上再加入方向性  
                
        if Ntemp:
            with io.open('clean/'+'N'+f,'w',encoding='utf-8') as nfile:
                nfile.write(ff[0])
                for ele in Ntemp:
                    nfile.write(ele)
        if Stemp:
            with io.open('clean/'+'S'+f,'w',encoding='utf-8') as sfile:
                sfile.write(ff[0])
                for ele in Stemp:
                    sfile.write(ele)
        if  Etemp:
            with io.open('clean/'+'E'+f,'w',encoding='utf-8') as efile:
                efile.write(ff[0])
                for ele in Etemp:
                    efile.write(ele)
        if Wtemp:
            with io.open('clean/'+'W'+f,'w',encoding='utf-8') as wfile:
                wfile.write(ff[0])
                for ele in Wtemp:
                    wfile.write(ele)
        if Utemp:
            with io.open('clean/'+'U'+f,'w',encoding='utf-8') as ufile:
                ufile.write(ff[0])
                for ele in Utemp:
                    ufile.write(ele)


# In[ ]:




#  # DB要設定好！！

# In[23]:

# 這個是把新資料insert到資料庫

import csv,io,os,re
import sys
#載入sys是因為要重啟sys預設編碼改成'utf-8'，下面的default等等是因為reload sys的話print在jupyter會印不出來，再重新設定
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')


import mysql.connector

cnx = mysql.connector.connect(user='root',password='apple', database='1027DEMO')
cursor = cnx.cursor()

files=[]
for f in os.listdir('./clean/'):
    if os.path.isfile('./clean/'+f):
        files.append(f)
replace2=[]
for f in files:
    if '.csv' in f:
        #利用正規表達式，從檔名去找table名
        match=re.findall('[A-Z0-9]+',f)
        tablename=str(match[0])
#         print tablename
        with io.open('./clean/'+f,'r',encoding='utf-8') as rcsv:
            content=[]
            for line in rcsv:
                content.append(line)
            for element in content[1:]:
                #不需要第一行標題 [1:]
#                 print element.split(',')
#                 print mytuple
                mylist=[tablename,]#先用list再轉成tuple
                for ele in element.split(','):
#                     print str(ele)
                    mylist.append(str(ele).strip())
                mytuple = tuple(mylist)#轉成tuple
#                 print mytuple
                replace2.append(mytuple) 
# print replace2[0][2]
           
#這裡要注意的是'{r[1]}','{r[2]}'...等等到r5要加引號是因為在query時就要加''號，因為'00:00:00'沒加''會出錯！！！
for ele in replace2:         
    query = ('''insert into {r[0]} (EQIPnumber,location,direct,YMD,hour,laneNumber,addTotal,15Total,
truckflow,carflow,scooterflow,avgspeed,avgPercent,avgCarSpace)values
('{r[1]}','{r[2]}','{r[3]}','{r[4]}','{r[5]}',{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]})
;'''.format(r=ele))
#     print query
    cursor.execute(query)
    cnx.commit()
cursor.close()

cnx.close()


# In[ ]:




# In[ ]:




# # DB 要設定好！！！

# In[24]:

import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')

import datetime
import csv,io
import mysql.connector

cnx = mysql.connector.connect(user='root',password='apple', database='1027DEMO')
cursor = cnx.cursor()

# query = ("select * from totala;") #整個TABLE全選
GNquery = ("""select NVQRTE00.direct,NVQRTE00.YMD,NVQRTE00.hour,NVQRTE00.15Total 
,rain.rain,rain.WD from NVQRTE00 join rain on NVQRTE00.YMD=rain.YMD;""")

GSquery = ("""select SVQRTE00.direct,SVQRTE00.YMD,SVQRTE00.hour,SVQRTE00.15Total 
,rain.rain,rain.WD from SVQRTE00 join rain on SVQRTE00.YMD=rain.YMD;""")


query=[GNquery,GSquery]


# Using the cursor as iterator
with io.open('舊宗.csv','w',encoding='utf-8')as RDBque:
    RDBque.write("方向,日期,時間,當量總和,雨量,星期"+u'\n')
    for ele in query:
        cursor.execute(ele)
        for rows in cursor:
            for ele in range(len(rows)):
                if ele == len(rows)-1:
                    RDBque.write(format(rows[ele]).decode('utf-8')+u'\n')
                else:
                    RDBque.write(format(rows[ele]).decode('utf-8')+u',')
cursor.close()
cnx.close()


# In[25]:

import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')

import datetime
import csv,io
import mysql.connector

cnx = mysql.connector.connect(user='root',password='apple', database='1027DEMO')
cursor = cnx.cursor()

# query = ("select * from totala;") #整個TABLE全選
TNquery = ("""select NVRPSV70.direct,NVRPSV70.YMD,NVRPSV70.hour,(NVRPSV70.15Total + NVTXQL00.15Total
+ NVT5QV00.15Total + NVSPRA40.15Total + NVPMSV40.15Total + NVRPSV00.15Total)
'total' ,rain.rain,rain.WD from NVRPSV70 join NVTXQL00 on (NVRPSV70.YMD=NVTXQL00.YMD and NVRPSV70.hour=NVTXQL00.hour)
join NVT5QV00 on (NVRPSV70.YMD=NVT5QV00.YMD and NVRPSV70.hour=NVT5QV00.hour)join NVSPRA40 on 
(NVRPSV70.YMD=NVSPRA40.YMD and NVRPSV70.hour=NVSPRA40.hour)join NVPMSV40 on 
(NVRPSV70.YMD=NVPMSV40.YMD and NVRPSV70.hour=NVPMSV40.hour)join NVRPSV00 on 
(NVRPSV70.YMD=NVRPSV00.YMD and NVRPSV70.hour=NVRPSV00.hour)join rain on NVRPSV70.YMD=rain.YMD;""")

TSquery = ("""select SVTXQL00.direct,SVTXQL00.YMD,SVTXQL00.hour,(SVTXQL00.15Total + SVT5QV00.15Total
+ SVSPRA40.15Total + SVPMSV40.15Total + SVRPSV00.15Total) 'total' ,rain.rain,rain.WD from SVTXQL00 join SVT5QV00 on 
(SVTXQL00.YMD=SVT5QV00.YMD and SVTXQL00.hour=SVT5QV00.hour)join SVSPRA40 on 
(SVTXQL00.YMD=SVSPRA40.YMD and SVTXQL00.hour=SVSPRA40.hour)join SVPMSV40 on 
(SVTXQL00.YMD=SVPMSV40.YMD and SVTXQL00.hour=SVPMSV40.hour)join SVRPSV00 on 
(SVTXQL00.YMD=SVRPSV00.YMD and SVTXQL00.hour=SVRPSV00.hour)join rain on SVTXQL00.YMD=rain.YMD;""")


query=[TNquery,TSquery]


# Using the cursor as iterator
with io.open('堤頂.csv','w',encoding='utf-8')as RDBque:
    RDBque.write("方向,日期,時間,當量總和,雨量,星期"+u'\n')
    for ele in query:
        cursor.execute(ele)
        for rows in cursor:
            for ele in range(len(rows)):
                if ele == len(rows)-1:
                    RDBque.write(format(rows[ele]).decode('utf-8')+u'\n')
                else:
                    RDBque.write(format(rows[ele]).decode('utf-8')+u',')
cursor.close()
cnx.close()




# In[26]:

import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')

import datetime
import csv,io
import mysql.connector

cnx = mysql.connector.connect(user='root',password='apple', database='1027DEMO')
cursor = cnx.cursor()

# query = ("select * from totala;") #整個TABLE全選
MEquery = ("""select EVQEUU60.direct,EVQEUU60.YMD,EVQEUU60.hour,(EVQEUU60.15Total + EVQKWL60.15Total + 
EVQKWL61.15Total) 'total' ,rain.rain,rain.WD from EVQEUU60 join EVQKWL60 on (EVQEUU60.YMD=EVQKWL60.YMD and 
EVQEUU60.hour=EVQKWL60.hour) join EVQKWL61 on (EVQEUU60.YMD=EVQKWL61.YMD and EVQEUU60.hour=EVQKWL61.hour)
join rain on EVQEUU60.YMD=rain.YMD;""")

MWquery = ("""select WVQEUU60.direct,WVQEUU60.YMD,WVQEUU60.hour,(WVQEUU60.15Total + WVQKWL60.15Total
+ WVQKWL61.15Total) 'total' ,rain.rain,rain.WD from WVQEUU60 join WVQKWL60 on (WVQEUU60.YMD=WVQKWL60.YMD 
and WVQEUU60.hour=WVQKWL60.hour) join WVQKWL61 on (WVQEUU60.YMD=WVQKWL61.YMD and WVQEUU60.hour=WVQKWL61.hour)
join rain on WVQEUU60.YMD=rain.YMD;""")


query=[MEquery,MWquery]


# Using the cursor as iterator
with io.open('民權.csv','w',encoding='utf-8')as RDBque:
    RDBque.write("方向,日期,時間,當量總和,雨量,星期"+u'\n')
    for ele in query:
        cursor.execute(ele)
        for rows in cursor:
            for ele in range(len(rows)):
                if ele == len(rows)-1:
                    RDBque.write(format(rows[ele]).decode('utf-8')+u'\n')
                else:
                    RDBque.write(format(rows[ele]).decode('utf-8')+u',')
cursor.close()
cnx.close()




# In[27]:

#把三張表合成一張表！！！


import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')


import csv,io,os

allappend=[]
allappend.append(u'道路'+u','+'方向,日期,時間,當量總和,雨量,星期\n')
with io.open("堤頂.csv",'r',encoding ='utf-8') as rfile:
    temp = []
    for line in rfile:
        temp.append(line)
    for ele in temp[1:]:
        allappend.append(u'堤頂'+u','+ele)
with io.open("民權.csv",'r',encoding ='utf-8') as rfile:
    temp = []
    for line in rfile:
        temp.append(line)
    for ele in temp[1:]:
        allappend.append(u'民權'+u','+ele)
        
with io.open("舊宗.csv",'r',encoding ='utf-8') as rfile:
    temp = []
    for line in rfile:
        temp.append(line)
    for ele in temp[1:]:
        allappend.append(u'舊宗'+u','+ele)
        
        
with io.open('allappend.csv','w',encoding='utf-8')as wfile:
    for ele in allappend:
        wfile.write(ele)
# for ele in allappend:
#     print ele


# In[28]:

# import os
# os.getcwd()


# In[ ]:




# In[29]:

def RPy():
    import rpy2.robjects as robjects
    from rpy2.robjects.packages import importr

    rstring="""
        function(){
            library(htmltools)
            library(webshot)
            library(gridExtra)
            library(grid)
            library(formattable)
            setwd(".")

            Sys.setlocale(category = "LC_CTYPE", locale= "zh_CN.UTF-8")

            m1=read.table("allappend.csv",  header = TRUE, sep = ",")
            #modelal=lm(carValume~roadname+diretion+timezone+as.character(weekday),data = al)
            #smal=summary(modelal)
            #s=smal$sigma

            ro=c("堤頂","舊宗","民權")
            re=c(12000,2800,5500)
            ti=c("上午尖峰","下午尖峰")
            ti1=c("08:00:00","18:00:00")
            ti2=c("09:00:00","19:00:00")
            di1=c("往北","往南")
            di2=c("往東","往西")
            day=c( "Mon","Tue" ,"Wed","Thu","Fri" , "Sat" ,"Sun"  )
            ma=length(ro)*length(ti)*2 #變數數量
            ta=matrix(0,ma*2,5)

            ta=data.frame(ta)
            n=0
            for (l in 1:5) {
              for (i in 1:length(ro)) {
                for (k in 1:2) {
                  for (j in 1:length(ti1)) {
                    n=n+1
                    if (l==1) {
                      if (ro[i]=="民權") {
                        row.names(ta)[n*2-1]= paste0(ro[i],"-",di2[k],"-",ti[j])
                        row.names(ta)[n*2]= paste0("塞車機率(",ro[i],"-",di2[k],"-",ti[j],")")        
                      }else{
                        row.names(ta)[n*2-1]= paste0(ro[i],"-",di1[k],"-",ti[j])
                        row.names(ta)[n*2]= paste0("塞車機率(",ro[i],"-",di1[k],"-",ti[j],")")
                      }
                    }
                    if (ro[i]=="民權") { 
                      ta[n*2-1,l]=round(mean(m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti1[j]&m1$方向==di2[k],]$當量總和+m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti2[j]&m1$方向==di2[k],]$當量總和))
                      ta[n*2,l]=round((1-pnorm(re[i],mean =ta[n*2-1,l],sd=sd(m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti1[j]&m1$方向==di2[k],]$當量總和+m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti2[j]&m1$方向==di2[k],]$當量總和)))*100)

                    }else{
                      ta[n*2-1,l]=round(mean(m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti1[j]&m1$方向==di1[k],]$當量總和+m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti2[j]&m1$方向==di1[k],]$當量總和))
                      ta[n*2,l]=round((1-pnorm(re[i],mean =ta[n*2-1,l],sd=sd(m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti1[j]&m1$方向==di1[k],]$當量總和+m1[m1$道路==ro[i]&m1$星期==day[l]& m1$時間==ti2[j]&m1$方向==di1[k],]$當量總和)))*100)

                    }
                    if(n==ma) n=0
                  } 
                }  
              }
            }  


            tam=rep(0,ma)
            for (i in 1:ma) {
              tam[i]=mean(as.numeric(ta[i*2,]))
              tam[i]=tam[i]+0.0001*i  
            }  


            rtam=ma-rank(tam)+1

            tb=matrix(0,ma*2,5)
            tb=data.frame(tb)
            for (i in 1:ma){
              row.names(tb)[rtam[i]*2]=row.names(ta)[i*2]
              row.names(tb)[rtam[i]*2-1]=row.names(ta)[i*2-1]
              for (j in 1:5) {
                tb[rtam[i]*2,j]=ta[i*2,j]
                tb[rtam[i]*2-1,j]=ta[i*2-1,j]   
              }
            }
            colnames(tb)=c("星期一","星期二","星期三","星期四","星期五")
            for (i in 1:ma) {
              tb[i*2,]=paste0(tb[i*2,],"%")  
            }

            # grid.table(tb)

            df <- data.frame(
              zzz = tb[0],
              aaa = tb[1], 
              bbb = tb[2],
              ccc = tb[3],
              ddd = tb[4],
              eee = tb[5],
              stringsAsFactors = FALSE
            )


            zz.fm <- formattable(df , list(
              aaa = color_tile("white", "orange"),
              bbb = color_tile("white", "orange"),
              ccc = color_tile("white", "orange"),
              ddd = color_tile("white", "orange"),
              eee = color_tile("white", "orange"),
              zzz = color_tile("white", "orange")

            ))


            export_formattable <- function(f, file, width = "100%", height = NULL, 
                                           background = "white", delay = 0.2){
              w <- as.htmlwidget(f, width = width, height = height)
              path <- html_print(w, background = background, viewer = NULL)
              url <- paste0("file:///",normalizePath(path,winslash="/"))
              webshot(url,
                      file = file,
                      selector = ".formattable_widget",
                      delay = delay)
            }
            
            export_formattable(zz.fm, file = "/Users/Jackie/Django/infiArk/NeiHu/static/images/1027/1027test.jpg")
        }
    """

    rfunc= robjects.r(rstring)
    rfunc()



# In[30]:

RPy()


# In[ ]:



