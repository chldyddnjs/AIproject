#차트의5대기법
import pandas as pd

file = 'data/data_2020.csv'
data = pd.read_csv(file)

import matplotlib.pyplot as plt
import seaborn as  sns

data_2PM = data[data.집계시 == 14]
print(data_2PM.info())

plt.figure(figsize=(20,10))#디스플레이를 위한 창
data_2PM_Destination = sns.countplot('도착영업소코드',data=data_2PM)
data_2PM_Destination.set_title('fuck by you',fontsize=18)
data_2PM_Destination.set_xlabel('arrivecode', fontdict = {'size':16})
data_2PM_Destination.set_ylabel('passtime', fontdict= {'size':16})
plt.show()
