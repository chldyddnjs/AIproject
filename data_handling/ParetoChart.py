import matplotlib.pyplot as plt
import pandas as pd

#Load Data
file = "data/data_2020.csv"
data = pd.read_csv(file)

data.head()
data.info()

#4. 집계시
data_06_22 = data[data.isin(range(6,23))]
data_06_22.sort_values(by='집계시')
data_06_22_counting = data_06_22['집계시'].value_counts()

x = data_06_22_counting.index
x = [str(i) for i in x] #avoiding sorting index

y = data_06_22_counting.values
ratio = y / y.sum()
ratio_sum = ratio.cumsum() #누적치

#Configure figure size
fig, barChart = plt.subplots(figsize=(20,10))
#create bar chart
barChart.bar(x,y)
#create
lineChart = barChart.twinx()
lineChart.plot(x,ratio_sum,'-ro',alpha = 0.5) #다시한번 알아보기
#create right annotations on line chart
ranges = lineChart.get_yticks()
print(ranges)
lineChart.set_yticklabels(['{:,.1%}'.format(x) for x in ranges]) # 퍼센티지 포맷
#Create annotations on line chart
ratio_sum_percentage = ['{0:.0%}'.format(x) for x in ratio_sum]
for i,txt in enumerate(ratio_sum_percentage):
    lineChart.annotate(txt,(x[i],ratio_sum[i]),fontsize=14)
#Generate labels and title
barChart.set_xlabel('집계시',fontdict= {'size':16})
barChart.set_ylabel('통행횟수',fontdict= {'size':16})
plt.title('Pareto Chart - 통행횟수 by 집계시',fontsize=18)
#show plt
plt.show()


data_destination_counting = data['도착영업소코드'].value_counts()
data_destination_counting
x = data_destination_counting.index
x = [str(i) for i in x]
y=data_destination_counting.values
ratio = y / y.sum()
ratio_sum = ratio.cumsum()

#Configure figure size
fig,barChart = plt.subplots(figsize=(20,10))
barChart.bar(x,y)
#create line Chart
lineChart = barChart.twinx()
lineChart.plot(x,ratio_sum,'-ro',alpha=0.5)
#create right side labels
ranges = lineChart.get_yticks()
print(ranges)
lineChart.set_yticklabels(['{:,.1%}'.format(x) for x in ranges]) # 퍼센티지 포맷
#Create annotations on line chart
ratio_sum_percentage = ['{0:.0%}'.format(x) for x in ratio_sum]
for i,txt in enumerate(ratio_sum_percentage):
    lineChart.annotate(txt,(x[i],ratio_sum[i]),fontsize=14)
#Generate labels and title
barChart.set_xlabel('도착영업소코드',fontdict={'size':16})
barChart.set_ylabel('통행횟수',fontdict={'size':16})
plt.title("pareto chart - 통행횟수 by 도착영업소코드",fontsize=14)
#Show plt
plt.show()