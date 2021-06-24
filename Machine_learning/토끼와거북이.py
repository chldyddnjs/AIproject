# @주석은 Froms를 이용한 코랩  웹표현 프로그래밍이다. 
import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import repeat

Tortoise_Speed = 1 #@param {type:"slider",min:0,max:10,step:1}
Tortoise_Bias = 4 #@param {type:"slider",min:0,max:10,step:1}
Hare_Speed = 2 #@param {type:"slider",min:0,max:10,step:1}

MAXVal = 10
INTERVAL = (MAXVal*10) + 1
doMeet = False
t_xdata,t_ydata,h_xdata,h_ydata = [],[],[],[]

#Config figure size
plt.figure(figsize=(10,10))

for t in np.linspace(0,MAXVal,INTERVAL):
    t_y = Tortoise_Speed*t + Tortoise_Bias
    h_y = Hare_Speed*t
    t_xdata.append(t)
    t_ydata.append(t_y)
    h_xdata.append(t)
    h_ydata.append(h_y)
    if(h_y >= t_y and (not doMeet)):
        doMeet = True
        meetTime = t
        meetDistance = t_y

plt.plot(t_xdata,t_ydata,label='Tortoise')
plt.plot(h_xdata,h_ydata,label="Hare")

if(doMeet):
    plt.title("The hare overcomed from "+ str(math.ceil(meetTime*100)/100) + 'hour(s)' + str(math.ceil(meetDistance*100)/100) + 'km(s)',fontsize=16)
    plt.plot(meetTime,meetDistance,'ro') #점찍기
else:
    plt.title('They will not meet',fontsize=16)

plt.xlabel('Time(hour)',fontsize=14)
plt.ylabel('Distance(km)',fontsize=14)

plt.legend() #범주가 나온다.
plt.show()

#선형회귀 모델의 절차
#지금은 여백으로 남기지만 이론을 제대로 써놓기로 한다.

#Hypothesis
velocity_Variance = 0.2 #@param {trpe:"slider",min:0,max:2,step:1}
LINES = 5
plt.figure(figsize=(5,5))

for t in np.linspace(0,MAXVal,INTERVAL):
    h_y = Hare_Speed*t
    h_xdata.append(t)
    h_ydata.append(h_y)

plt.plot(h_xdata,h_ydata,'ro',label='Hare')

plt.title('Linear Regression',fontsize=16)
plt.xlabel('Time(hour',fontsize=14)
plt.ylabel('Distance(km',fontsize=14)
plt.legend()
plt.show()

a_val = Hare_Speed + (velocity_Variance * LINES)
h_xdata,h_ydata,v_xdata,v_ydata = [],[],[],[]
for t in np.linspace(0,MAXVal,INTERVAL):
    h_y = Hare_Speed*t
    h_xdata.append(t)
    h_ydata.append(h_y)
    a = a_val - (t*velocity_Variance)
    for i in np.linspace(0,MAXVal,INTERVAL):
        h_y = a*i
        v_xdata.append(i)
        v_ydata.append(h_y)
    plt.plot(v_xdata,v_ydata,alpha=0.2)
    
plt.plot(h_xdata,h_ydata,'ro',label = 'Hare')
plt.title('Linear Regression',fontsize=16)
plt.xlabel('Time(hour',fontsize=14)
plt.ylabel('Distance(km',fontsize=14)
plt.legend()
plt.show()

import matplotlib.animation as animation
from matplotlib import rc
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.set_xlim(-0.1,2.1)
ax.set_ylim(0,400)
t_xdata,t_ydata = [],[]

def get_cost(a_val):
    cost = 0
    for i in np.linspace(0,MAXVal,INTERVAL):
        cost += pow(a_val*i - Hare_Speed*i,2)
    return cost

def animateFrame(frame):
    a_val = Hare_Speed + (velocity_Variance * LINES)
    i = frame * velocity_Variance
    a = a_val - i
    t_xdata.append(i)
    t_ydata.append(get_cost(a))
    plot = ax.plot(t_xdata,t_ydata,'ro')
    return plot
anim = animation.FuncAnimation(fig,animateFrame,frames=np.linspace(0,MAXVal,INTERVAL),blit=True,repeat=False)

ax.set_title('Geadient descent')
ax.set_xlabel('Total Cost')
ax.set_ylabel('Varience')


anim
#Show Animation