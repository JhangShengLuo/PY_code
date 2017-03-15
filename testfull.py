oli = pd.read_csv('cleanoutwvd.csv')
olier = oli.copy();
#去掉當量暫時不用

# olier.speed=(olier.speed);olier
# olier.YY=olier.YY-16;
olier=olier.drop(['direct','lane','eqflow','fakeornot','realvd'],axis=1);olier
# olier['serial'] = olier.index

"""olierc = olier.copy()
dfmin = olier.serial.min().copy()
mxmin = olier.serial.max().copy()-dfmin;
olierc.serial = ((olierc.serial-dfmin)/(mxmin));olierc"""


"""
標準化失敗
#佔有率標準化
olierc = olier.copy()
dfmin = olier.accu.min().copy()
mxmin = olier.accu.max().copy()-dfmin;
olierc.accu = ((olierc.accu-dfmin)/(mxmin));olierc

#佔有率標準化

dfminspeed = olier.speed.min().copy()
mxminspeed = olier.speed.max().copy()-dfminspeed;
olierc.speed = ((olierc.speed-dfminspeed)/(mxminspeed));olierc"""


# move accu to the end
olierclo = olier.columns.tolist()
# olierc= olierc[olierclo[-1:]+olierclo[:-1]];
# speed
olier=olier[olierclo[:-2]+olierclo[-1:]+olierclo[-2:-1]]
# olier= olier[olierclo[-1:]+olierclo[:1]+olierclo[2:3]+olierclo[1:2]]; # 有serial時的speed

#0225version
def cleanout(inp,i):
    dfvdi= inp.where(inp['sortby']==i).dropna();

    outp = dfvdi.copy()
    # 某個時間要把fakeornot去掉 
    outpp = outp.values.astype('float32')
    # 分出train 跟test
    train_size = int(len(outpp) * 0.75)
    test_size = len(outpp) - train_size
    train, test = outpp[0:train_size,:], outpp[train_size:len(outpp),:]
    if (len(train)%168 != 0) or (len(test)%168 != 0) :
        train=train[:-(len(train)%168)]
        test=test[:-(len(test)%168)]
        
    return train,test


import time
start = time.time()

sortbylist=oli['sortby'].unique().tolist()
tralist = []
teslist = []

for i in sortbylist:
    temptra,temptes=cleanout(olier,i)
    #train
    for ele in temptra.tolist():
        tralist.append(ele)
    #test
    for ele3 in temptes.tolist():
        teslist.append(ele3)

cluster01tra=np.array(tralist)
print len(cluster01tra)
cluster01tes=np.array(teslist)
print len(cluster01tes)
print(start - time.time()),'seconds'


