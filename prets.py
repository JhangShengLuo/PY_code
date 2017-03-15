# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import sklearn.linear_model as lm
from keras.models import Sequential,load_model,Model
from keras.layers import Dense,Reshape,advanced_activations
from keras.constraints import nonneg
import numpy as np
%matplotlib inline
import tensorflow
import keras
import math
import time
import datetime
from sklearn import cluster, datasets, metrics


oli = pd.read_csv('cleanoutwvd.csv')
olier = oli.copy();
#去掉當量暫時不用

olier.speed=(olier.speed/10);olier
olier.YY=olier.YY-16;
olier=olier.drop(['eqflow','fakeornot','realvd'],axis=1);olier

"""# move speed to the end
olierclo = olier.columns.tolist()
olier= olier[olierclo[:-2]+olierclo[-1:]+olierclo[-2:-1]];"""
olier
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



import time
start = time.time()

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(0,len(dataset)-look_back-1,look_back):
        a = dataset[i:(i+look_back), 0:nort]
        dataX.append(a)
        dataY.append(dataset[i + look_back:i+look_back+look_back, nort-1])
#     return dataX,dataY
    return np.array(dataX), np.array(dataY)

# 看資料有幾個欄位就寫幾
nort = 9
# magic number
look_back = 168
# cut off remainder
train = cluster01tra
test = cluster01tes
# check data lenth when cut off remainder
print(len(train), len(test))

# seperate data to input"X" and output"Y"
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
    
# create and fit Multilayer Perceptron model
model = Sequential()
# model = Model(input=look_back*nort,output=[look_back,2])

# RESHAPE is  working !!!!! >0<"
model.add(Reshape((look_back*nort,), input_shape=(look_back,nort)))
# Add layers to neruon network
model.add(Dense(190,input_dim=(look_back*nort), activation='relu'))
model.add(Dense(256, init='uniform', activation='relu'))
model.add(Dense(look_back, W_constraint=nonneg()))
model.compile(loss='mape', optimizer='adam')

model.fit(trainX, trainY, nb_epoch=168, batch_size=3, verbose=0)

# Estimate model performance
trainScore = model.evaluate(trainX, trainY, verbose=0)
print('Train Score: %.2f MAPE ' % trainScore)
# print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
testScore = model.evaluate(testX, testY, verbose=0)
print('Test Score: %.2f MAPE ' % testScore)
# print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))

print(start - time.time()),'seconds'

trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

pre = trainPredict.reshape(len(trainPredict)*len(trainPredict[0]),)
ori = trainY.reshape(len(trainY)*len(trainY[0]),)

print pre.mean()
print ori.mean()
print pre.std()
print ori.std()

plt.plot(pre[],color='r')

plt.plot(ori[],color='g')

plt.plot(pre,color='r')