import matplotlib.pyplot as plt
import pandas as pd

plt.rc('font',family='NanumBarunGohic')

#Data Load
file = "data/data_2020.csv"
data = pd.read_csv(file)

# data.head()
# data.info()

data_06_22 = data[data.집계시.isin(range(6,23))]
data_06_22.sort_values(by='집계시')
data_06_22_counting = data_06_22['집계시'].value_counts()
x = data_06_22_counting.index
labels = [str(i)+'시' for i in x]

explode = [0.1,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

values = data_06_22_counting.values
plt.figure(figsize=(7,7))
plt.pie(values,explode=explode,labels=labels,startangle= 90, shadow=True,autopct='%.1f',counterclock=False)
#Generate labels and title
plt.title("집계시 기준 통행횟수",fontsize=18)
#Show plot
plt.show()

#도착영업소코드
data_destination_counting =data['도착영업소코드'].value_counts()
# print(data_destination_counting)

x = data_destination_counting.index

labels = [str(i) for i in x]

explode = [0.2,0.1,0,0,0,0,0,0]
values = data_destination_counting.values
plt.pie(values,explode=explode,labels=labels,startangle=90,shadow=True,autopct='%1.f%%',counterclock=False)
plt.title("도착영업소 기준 통행횟수",fontsize=18)
plt.show()