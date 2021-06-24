import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


Tortoise_Speed = 1 #@param {type:"slider",min:0,max:10,step:1}
Tortoise_Bias = 4 #@param {type:"slider",min:0,max:10,step:1}
Hare_Speed = 2 #@param {type:"slider",min:0,max:10,step:1}

MAXVal = 10
INTERVAL = (MAXVal*10) + 1
doMeet = False
t_xdata,t_ydata = [],[],

for t in np.linspace(0,MAXVal,INTERVAL):
    t_y = Tortoise_Speed*t + Tortoise_Bias
    t_xdata.append(t)
    t_ydata.append(t_y)


learning_rate = 0.01
learning_epochs = 500

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(1,input_dim=1)) #1차원 사용한다.

sgd =tf.keras.optimizers.SGD(learning_rate=learning_rate)
mse = tf.keras.losses.mean_squared_error #평균제곱오차

model.compile(loss=mse,optimizer=sgd)
model.summary()
#The tortoise learning
t_history = model.fit(t_xdata,t_ydata,epochs=learning_epochs)

plt.figure(figsize=(5,5))
plt.plot(t_history.history['loss'])
plt.show()

result = model.predict([10])
print(result)

p_ydata = model.predict(t_xdata)

plt.plot(t_xdata,t_ydata,'r*')
plt.plot(t_xdata,p_ydata,color='b')
plt.show()