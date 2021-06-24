import matplotlib.pyplot as plt
import pandas as pd

#Load Data
file = 'data/data_2020.csv'
data = pd.read_csv(file)

data_06_22 = data[data['집계시'].isin(range(6,23))]
data_06_22.sort_values(by='집계시')

data_06_22_counting = data_06_22['집계시'].value_counts()
data_06_22_counting_sorted = data_06_22_counting.sort_index()

data_days_time = data_06_22['통행시간']
x = data_days_time.index
labels = [str(i) for i in x]
y = data_days_time.values
plt.figure(figsize=(20,10))
plt.scatter(labels,y,marker='s',color='g')
# plt.title('요일 기준 통행시간',fontsize=18)
# plt.xlabel('요일',fontdict={'size':16})
# plt.ylabel('통행시간',fontdict={'size':16})
# plt.show()