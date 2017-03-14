
# coding: utf-8

# In[3]:

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import csv,io
import mysql.connector



cnx = mysql.connector.connect(user='root',password='apple', database='infiark')
cursor = cnx.cursor()

# query = ("select * from totala;") #整個TABLE全選
query = ("""select YMD, roadname, direct, timezone, sum(carvolume) volume, Weekday, rain from totala
where(roadname='堤頂大道' and direct='往南' and timezone='下午尖峰')group by YMD,Weekday,rain;""") 


# Using the cursor as iterator
cursor.execute(query)
with io.open('resultSA.csv','w',encoding='utf-8')as RDBque:
#     整個table全選的話要寫這些欄位
#     RDBque.write("date,road,roadname,roadvalue,roadblock,diretion,timezone,carValume,weekday,rain"+u'\n')
    RDBque.write("YMD,roadname,diretion,timezone,carValume,weekday,rain"+u'\n')
    for rows in cursor:
        for ele in range(len(rows)):
            if ele == len(rows)-1:
                RDBque.write(format(rows[ele]).decode('utf-8')+u'\n')
            else:
                RDBque.write(format(rows[ele]).decode('utf-8')+u',')
            
        
#             print (ele)



# Using a while loop
# cursor.execute(query)
# row = cursor.fetchone()
# while row is not None:
#     print(row)
#     row = cursor.fetchone()




cursor.close()
cnx.close()


# In[9]:

def RPy():
    import rpy2.robjects as robjects
    from rpy2.robjects.packages import importr

    rstring="""
        function(){
            setwd(".")
            neihu<- read.table("resultSA.csv", header = TRUE, sep = ",")
            attach(neihu)
            jpeg(file="NeiHuSA.jpeg")
            model=lm(carValume~weekday)
            summary(model)
            yf=predict(model)
            plot(carValume,type = "l", col= 4,xaxt="n",main="Result",xlab="blue=actuality red=forecast",ylab="equivalent",sub="105.04.11~105.09.18")
            lines(yf, col= 2)
            detach(neihu)
            dev.off()
        }
    """

    rfunc= robjects.r(rstring)
    rfunc()



# In[10]:

RPy()


# In[ ]:



