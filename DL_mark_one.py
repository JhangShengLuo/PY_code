# fix random seed for reproducibility

np.random.seed(7)
mldf = pd.read_csv('mltest.csv', engine='python')
# First thing first, format data to what we need
mltt = mldf.ix[:,[3,4,5,6,8,9,10,7]].copy()
mltt.columns = ['a','b','c','d','e','f','g','h'];mltt
mltt.replace(to_replace='東',value=1,inplace=True );mltt
mltt.c=pd.to_datetime(mltt.c);
mltt.c = pd.to_datetime(mltt.c);
mltt['weekday'] = mltt['c'].dt.dayofweek;mltt
mltt.c= mltt.c.dt.dayofyear;mltt
mltt.replace(to_replace='00:00:00',value=0,inplace=True );mltt
mltt.replace(to_replace='01:00:00',value=1,inplace=True );mltt
mltt.replace(to_replace='02:00:00',value=2,inplace=True );mltt
mltt.replace(to_replace='03:00:00',value=3,inplace=True );mltt
mltt.replace(to_replace='04:00:00',value=4,inplace=True );mltt
mltt.replace(to_replace='05:00:00',value=5,inplace=True );mltt
mltt.replace(to_replace='06:00:00',value=6,inplace=True );mltt
mltt.replace(to_replace='07:00:00',value=7,inplace=True );mltt
mltt.replace(to_replace='08:00:00',value=8,inplace=True );mltt
mltt.replace(to_replace='09:00:00',value=9,inplace=True );mltt
mltt.replace(to_replace='10:00:00',value=10,inplace=True );mltt
mltt.replace(to_replace='11:00:00',value=11,inplace=True );mltt
mltt.replace(to_replace='12:00:00',value=12,inplace=True );mltt
mltt.replace(to_replace='13:00:00',value=13,inplace=True );mltt
mltt.replace(to_replace='14:00:00',value=14,inplace=True );mltt
mltt.replace(to_replace='15:00:00',value=15,inplace=True );mltt
mltt.replace(to_replace='16:00:00',value=16,inplace=True );mltt
mltt.replace(to_replace='17:00:00',value=17,inplace=True );mltt
mltt.replace(to_replace='18:00:00',value=18,inplace=True );mltt
mltt.replace(to_replace='19:00:00',value=19,inplace=True );mltt
mltt.replace(to_replace='20:00:00',value=20,inplace=True );mltt
mltt.replace(to_replace='21:00:00',value=21,inplace=True );mltt
mltt.replace(to_replace='22:00:00',value=22,inplace=True );mltt
mltt.replace(to_replace='23:00:00',value=23,inplace=True );mltt

cols =mltt.columns.tolist()
mltt= mltt[cols[:3]+cols[-1:]+cols[3:-1]];mltt
mltt.columns = ['a','b','c','d','e','f','g','h','i'];mltt

mlttva = mltt.values
mlttva = mlttva.astype('float32')

# seperate train and test data to 67%/33%
train_size = int(len(mlttva) * 0.67)
test_size = len(mlttva) - train_size
train, test = mlttva[0:train_size,:], mlttva[train_size:len(mlttva),:]
# check the lenth of data
print(len(train), len(test))

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(0,len(dataset)-look_back-1,look_back):
        a = dataset[i:(i+look_back), 0:9]
        dataX.append(a)
        dataY.append(dataset[i + look_back:i+look_back+look_back, 8])
#     return dataX,dataY
    return np.array(dataX), np.array(dataY)
# magic number
look_back = 168
# cut off remainder
train = train[:-(len(train)%look_back)]
test = test[:-(len(test)%look_back)]
# check data lenth when cut off remainder
print(len(train), len(test))
# seperate data to input"X" and output"Y"
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# create and fit Multilayer Perceptron model
model = Sequential()

# RESHAPE is  working !!!!! >0<"
model.add(Reshape((look_back*9,), input_shape=(look_back,9)))
# Add layers to neruon network
model.add(Dense(190,input_dim=(look_back*9), activation='relu'))
model.add(Dense(30, init='uniform', activation='relu'))
model.add(Dense(look_back))
model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(trainX, trainY, nb_epoch=150, batch_size=2, verbose=0)


# Estimate model performance
trainScore = model.evaluate(trainX, trainY, verbose=0)
print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
testScore = model.evaluate(testX, testY, verbose=0)
print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))

# predict result
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# Jackie veriosn plot

pre = testPredict.reshape(len(testPredict)*len(testPredict[0]),)
ori = testY.reshape(len(testY)*len(testY[0]),)

plt.plot(pre[-168:],color='r')
plt.plot(ori[-168:],color='g')
plt.show()


