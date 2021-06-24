#실질적인 머신러닝 프로젝트 
#데이터를 가능한한 단순화했다. 검증되어있는 데이터셋이 아니다.
#원리와 이해를 중점으로 한다.
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.python.keras.engine.training import Model

file = 'result.csv'
data = pd.read_csv(file)

data.head() # 데이터 확인
data.info() # 데이터 구조 확인

#101,서울 105,기흥 110,목천 115,대전 120,황간 125,남구미 130,동김천 135, 경주,140,부산
#Distance from Seoul : 0,18,75,77.03,135,184,56,214.94,239.69,338.68,406.94
#Distance fomr Seoul(Brifing) :0,20,77,135,185,240,215,339,407
data['도착영업소코드'] = data['도착영업소코드'].map({105:20,110:77,115:135,120:185,125:240,130:215,135:339,140:407})
# print(data)
data.rename(columns={'도착영업소코드':'거리'}, inplace=True)
# print(data)

#Linear Regression
import tensorflow as tf
import numpy as np

Selected_Data = '2020-01-10' #@param {type:"date"}
input_date = int(Selected_Data.replace('-',''))
# print(input_date)

data_date = data[data['집계일자'] == input_date]
print(data_date)

plt.plot(data_date['거리'],data_date['통행시간'],'r*')
plt.show()

#index를 없애고 평탄하게 만들어주는 방법
data_time = data_date.groupby(['집계일자','거리'])['통행시간'].mean()
data_out = data_time.reset_index()

#Dataframe to List
data_list = data_out.values.tolist()
data_list[:3]

# print(data_list)

x_train = [int(r[1]) for r in data_list]
#Nomarization
y_train = [int(r[2]/10) for r in data_list]
plt.plot(x_train,y_train,'r*')
plt.show()

learning_rate = 1e-8
learning_epochs = 2000

sgd = tf.keras.optimizers.SGD(learning_rate=learning_rate)
mse = tf.keras.losses.mean_squared_error

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(1,input_dim = 1))
model.compile(loss=mse,optimizer=sgd)
model.summary()

history = model.fit(x_train,y_train,epochs=learning_epochs)
plt.plot(history.history['loss'])
plt.show()

print(x_train,y_train)
Distance = 400 #@param {type:"slider",min:0,max:500,step:1}
input_data = [Distance]
predicted_value = model.predict(input_data)
print(predicted_value)
print('%3d km takes %5.1f seconds on %s' %(Distance,predicted_value[0][0]*10,Selected_Data))