print(Sys.time())
Sys.setlocale(category = "LC_CTYPE", locale= "zh_CN.UTF-8")
t=read.table("/Users/Jackie/Desktop/1028etl2.csv",  header = TRUE, sep = ",")


t=data.frame(t)
t[t$方向=="向東",]$方向="往東"
t[t$方向=="向西",]$方向="往西"
#t[t$方向=="向北",]$方向="往北"
#t[t$方向=="向南",]$方向="往南"
lp=levels(t$位置)
tm=c("08:00:00","09:00:00")
te=c("18:00:00","19:00:00")

lpm=matrix(0,1,length(lp))
#modelt=lm(當量~位置+方向+時間+星期+道路數,data = t)
#smt=summary(modelt)
for (i in 1:length(lp)) {
  di=levels(factor(t[t$位置==lp[i],]$方向))
  lpm[i]=median(t[t$位置==lp[i]&t$時間==te[1]&t$星期=="Fri"&t$方向==di[1],"當量"])
}
lpm
a1=a2=a3=0
r1000=r500=r0=0
for (i in 1:length(lp)) {
  if(lpm[i]>1000){
    a1=a1+1  
    r1000[a1]=lp[i]
  }else if (lpm[i]>500){
    a2=a2+1 
    r500[a2]=lp[i]
  }else{
    a3=a3+1
    r0[a3]=lp[i]  
    
  }  
}
#r1000
#r500
#r0
#建模
test=rbind(t[t$位置==lp[1],],t[t$位置==lp[2],])
t1000=t500=t0=t[t$道路==0,]
for (i in 1:length(r1000)) {
  t1000=rbind(t1000,t[t$位置==r1000[i],])  
}
#t1000
for (i in 1:length(r500)) {
  t500=rbind(t500,t[t$位置==r500[i],])  
}
for (i in 1:length(r0)) {
  t0=rbind(t0,t[t$位置==r0[i],])  
}
modelt1000=lm(當量~位置+方向+時間+星期+道路數+平均速度+平均佔有率+平均車間距,data = t1000)
#summary(modelt1000)
modelt500=lm(當量~位置+方向+時間+星期+道路數+平均速度+平均佔有率+平均車間距,data = t500)
#summary(modelt500)
modelt0=lm(當量~位置+方向+時間+星期+道路數+平均速度+平均佔有率+平均車間距,data = t0)
#summary(modelt0)

# 塞車標準值 
meq=matrix(0,1,length(lp))
for (i in 1:length(lp)) {
  meq[i]=mean(t[t$位置==lp[i]&t$平均佔有率>5&t$平均佔有率<6,]$當量)*2  
}


ti=c("上午尖峰","下午尖峰")
ti1=c("08:00:00","18:00:00")
ti2=c("09:00:00","19:00:00")
di1=c("往北","往南")
di2=c("往東","往西")
day=c( "Mon","Tue" ,"Wed","Thu","Fri" , "Sat" ,"Sun"  )
ma=length(lp)*length(ti)*2 #變數數量
ta=matrix(0,ma*2,5)
ta=data.frame(ta)
n=0


for (l in 1:5) {
  for (i in 1:length(lp)) {
    for (k in 1:2) {
      for (j in 1:length(ti1)) {
        n=n+1
        if (l==1) {
          if ("往東"%in%t[t$位置==lp[i],]$方向) {
            row.names(ta)[n*2-1]= paste0(lp[i],"-",di2[k],"-",ti[j])
            row.names(ta)[n*2]= paste0("塞車機率(",lp[i],"-",di2[k],"-",ti[j],")")        
          }else{
            row.names(ta)[n*2-1]= paste0(lp[i],"-",di1[k],"-",ti[j])
            row.names(ta)[n*2]= paste0("塞車機率(",lp[i],"-",di1[k],"-",ti[j],")")
          }
        }
        
        if ("往東"%in%t[t$位置==lp[i],]$方向 ) { 
          ta[n*2-1,l]=round(mean(t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti1[j]&t$方向==di2[k],]$當量+t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti2[j]&t$方向==di2[k],]$當量))
          ta[n*2,l]=round((1-pnorm(meq[i],mean =ta[n*2-1,l],sd=sd(t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti1[j]&t$方向==di2[k],]$當量+t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti2[j]&t$方向==di2[k],]$當量)))*100)
          
        }else{
          ta[n*2-1,l]=round(mean(t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti1[j]&t$方向==di1[k],]$當量+t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti2[j]&t$方向==di1[k],]$當量))
          ta[n*2,l]=round((1-pnorm(meq[i],mean =ta[n*2-1,l],sd=sd(t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti1[j]&t$方向==di1[k],]$當量+t[t$位置==lp[i]&t$星期==day[l]& t$時間==ti2[j]&t$方向==di1[k],]$當量)))*100)
          
        }
        if(n==ma) n=0
      } 
    }  
  }
}  

ta=na.omit(ta)
colnames(ta)=c("星期一","星期二","星期三","星期四","星期五")
for (i in 1:(nrow(ta)/2)) {
  ta[i*2,]=paste0(ta[i*2,],"%")  
}

write.table(ta, file = "/Users/Jackie/Desktop/ETLcode1103/1103.csv", col.names=NA, sep = ",")

print(Sys.time())


