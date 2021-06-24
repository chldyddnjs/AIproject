import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
from numpy.core.numeric import True_
import pandas as pd

#Load Data
file = 'result.csv'
data = pd.read_csv(file)

data.head()
data.info()
#서울에서 부산까지 도착하는지 안하는지 예측하는 모델이므로 부산데이터를 추려야한다.
data['도착영업소코드'] = data['도착영업소코드'].map({105:20,110:77,115:135,120:185,125:240,130:215,135:339,140:407})
data.rename(columns= {'도착영업소코드':'거리'},inplace=True_)
data_destination = data[data['거리']==407]

data_time = data_destination.groupby(['집계시','요일','거리'])['통행시간'].mean()

data_distance = data_time.unstack(level=-1)
data_distance.dropna() #null 값 없애기
data_out = data_distance.reset_index() #1차원으로 펴주는 함수
stat = data_out.describe()

mean_value = stat[407][1]
# print(mean_value)

data_out['Binary'] = data_out[407] >= mean_value
data_out['Binary'] = data_out['Binary'].map({True:1,False:0})

data_list = data_out.values.tolist()
print(data_list)

#Train Dataset
x_train = [r[:2] for r in data_list]
y_train = [r[-1] for r in data_list]

#Binary Classification using Tensorflow
import tensorflow as tf
import numpy as np

learning_rate = 1e-4
learning_epochs = 1000
sgd = tf.keras.optimizers.SGD(learning_rate=learning_rate)
mse = tf.keras.losses.mean_squared_error

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(1,input_shape=(2,),activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
model.summary()
history = model.fit(x_train,y_train,epochs = learning_epochs)
plt.figure(figsize=(10,10))
plt.plot(history.history['loss'],color='r',label ='Cost')
plt.plot(history.history['accuracy'],color='b',label ='Acc')
plt.title('Cost and Acc')
plt.ylabel('cost,acc')
plt.xlabel('learning num')
plt.legend()
plt.show()

for step in range(learning_epochs):
    if(step % 100 == 0):
        cost_val = history.history['loss'][step]
        acc_val = history.history['accuracy'][step]
        print("%20i %20.5f %20.5f" % (step,cost_val,acc_val))


Time = 14 #@param {type:"slider",min=0,max=10,step=1}
Day = 3 #@param {type:"slider",min=0,max=10,step=1}

time_condition = data_out['집계시'] == Time
day_condition = data_out['요일'] == Day
data_out[time_condition & day_condition]

input = [Time,Day]
result = model.predict([input])

print("%10s %20s" % ('result','delay') + '\n')
if(result[0] > 0.5):
    print("%10.7f %20s" % (result[0],'delay'))
else:
    print("%10.7f %20s" % (result[0],'not delay'))