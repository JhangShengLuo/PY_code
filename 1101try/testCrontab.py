#!/Users/Jackie/anaconda/bin/python
# coding: utf-8

# In[4]:

import time
import os
import sys
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr   

# import rpy2.robjects as robjects
# from rpy2.robjects.packages import importr  
ct=time.strftime('%Y%m%d',time.localtime())
if not os.path.exists('/Users/Jackie/Desktop/'+ct):
	os.makedirs('/Users/Jackie/Desktop/'+ct)

def pppp():
	# import sys
	with open('/Users/Jackie/Desktop/'+ct+'/'+'test.txt','w')as f:
		for i in sys.path:
		    f.write(i+'\n')
 
pppp()
def RPy():
    

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
            
            export_formattable(zz.fm, file = "/Users/Jackie/Django/infiArk/NeiHu/static/images/1027/1027test3.jpg")
        }
    """

    rfunc= robjects.r(rstring)
    rfunc()

RPy()




# In[ ]:



