import matplotlib.pyplot as plt
import pandas as pd

# plt.rc('font',family='NanumBarunGohic')

#Load Data
file = 'data/data_2020.csv'
data = pd.read_csv(file)

data.head()
data.info()

#Linchar start(함수이름 잘보기)
data_06_22 = data[data.집계시.isin(range(6,23))]
data_06_22_counting = data_06_22['집계시'].value_counts()

data_06_22_counting_sorted = data_06_22_counting.sort_index()
print(data_06_22_counting_sorted)

x = data_06_22_counting_sorted.index
y = data_06_22_counting_sorted.values
labels = [str(i)+'시' for i in x]

plt.figure(figsize=(20,10))
plt.plot(labels,y,marker='s',color='r')
plt.title("집계시 기준 통행횟수",fontsize=18)
plt.xlabel('집계시',fontdict={'size':16})
plt.ylabel('통행횟수',fontdict={'size':16})
plt.show()

data_destination_counting = data['도착영업소코드'].value_counts()
data_destination_counting_sorted = data_destination_counting.sort_index()

x = data_destination_counting_sorted.index
y = data_destination_counting_sorted.values

labels = [str(i) for i in x]

labels = ['기흥','목천','대전','황간','남구미','동김천','경주','부산']

plt.figure(figsize=(20,10))
plt.plot(labels,y,marker='*',color='b')
plt.title('도착영업소 기준 통행횟수',fontsize=18)
plt.xlabel('도착영업소코드',fontdict={'size':16})
plt.ylabel('통행횟수',fontdict={'size':16})
plt.show()

# data_weekdays = data.groupby(by=['요일']).mean()
# print(data_weekdays)

# data_weekdays_time = data_weekdays['통행시간']
# x = data_weekdays_time.index
# labels = ['월','화','수','목','금','토','일']

# y = data_weekdays_time.values

# plt.figure((20,10))
# plt.plot(labels,y,marker='d',color='g')
# plt.title('요일 기준 통행시간',fontsize=18)
# plt.xlabel('요일',fontdict={'size':16})
# plt.ylabel('통행시간',fontdict={'size':16})
# plt.show()

