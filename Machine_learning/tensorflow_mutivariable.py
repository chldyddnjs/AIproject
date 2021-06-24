import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

plt.rc('font',family='NanumBarunGohic')

import pandas as pd

file = 'result.csv'
data = pd.read_csv(file)


# data.info()

data['도착영업소코드'] = data['도착영업소코드'].map({105:20,110:77,115:135,120:185,125:240,130:215,135:339,140:407})
data.rename(columns={'도착영업소코드':'거리'}, inplace=True)
data_destination = data[data['거리'].isin([407])]

data_time = data_destination.groupby(['집계시','요일','거리'])['통행시간'].mean()
data_distance = data_time.unstack(level=-1) #마지막에있는 축을 바꿔준다.

data_distance = data_distance.dropna()
data_out = data_distance.reset_index() #data_

#Dataframe to List
data_list = data_out.values.tolist()
#Train Dataset
x_train = [r[:2] for r in data_list]
y_train = [r[-1] for r in data_list]

#Show graph
x1 = [r[0] for r in data_list]
x2 = [r[1] for r in data_list]
y = [r[-1] for r in data_list]

fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.set_title('Multi Variable Regression')
ax.set_xlabel('집계시')
ax.set_ylabel('요일')
ax.set_zlabel('통행시간')
plot = ax.scatter(x1,x2,y,c='r')
plt.show()

import tensorflow as tf
import numpy as np

learning_rate = 1e-4
learning_epochs = 5000

#SGD
sgd = tf.keras.optimizers.SGD(learning_rate=learning_rate)
#Mean Square Error
mse = tf.keras.losses.mean_squared_error
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(1,input_shape=(2,)))
model.compile(loss=mse,optimizer=sgd)
model.summary()

history = model.fit(x_train,y_train,epochs=learning_epochs)
plt.figure(figsize=(10,10))
plt.plot(history.history['loss'])
plt.title('Cost Gradient Decent')
plt.ylabel('Total Cost')
plt.xlabel('Number of Traning')
plt.show()

print("%20 %20 " %('Step','Cost')+'\n')
for step in range(learning_epochs):
    if(step % 100 == 0):
        cost_val = history.history['loss'][step]
        print("%20i %20.5f" % (step,cost_val))

Time = 14 #param {type:"slider",min:0,max:23,step:1}
Day = 3 #param {type:"slider",min:0,max:6,step:1}
time_condition = data_out['집계시'] == Time
day_condition = data_out['요일'] == Day
data_out[time_condition & day_condition]

input = [Time,Day]
time = model.predict([input])
ml_time = time[0][0]
week_days = ['월','화','수','목','금','토','일']
print('%10s %10s %50s' %('집계시','요일','서울에서 부산까지 통행시간') + '\n')
print('%10s %10s %50s' %(str(Time),week_days,str(ml_time)) + '\n')
