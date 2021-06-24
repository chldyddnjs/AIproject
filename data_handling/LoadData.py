import pandas as pd
from pandas.core import groupby
file = "data/data_202001.csv"
data = pd.read_csv(file,sep=",",encoding="utf-8")
# print(data.head())
# print(data.info())
# 데이터 정제의 중요성 (머신러닝과 학습)
# 데이터의 품질과 데이터에 담긴 정보량
#데이터에서 결측값 제거,대치

#Clean Data
#Null값이 있는지 없는지 참조
data.isnull().sum(axis=0)

#Drop some columns with null values
# data_clean = data.drop(['Unnamed: 6'],axis='columns')
# data_clean.head()
# data_clean = data_clean[data_clean.통행시간 > 0]
# data.head()

#Show columns of the data frame
# print(data.집계일자)
# print(data["집계일자"])

df_data = pd.DataFrame(data,columns=['집계일자','집계시','출발영업소코드','도착영업소코드','통행시간'])
# print(df_data.head())
long_distance = df_data.통행시간 > 700 #True False만 리턴
start_from_101 = df_data[df_data.출발영업소코드 == 101]

#101 서울 105 기흥 110 목천 115 대전 120 황간 125 남구미 130 동김천 135 경주 140 부산
start_from_101_to_140 = start_from_101[start_from_101['도착영업소코드'].isin([105,110,115,120,125,130,135,140])]
# print(start_from_101_to_140)
# print(start_from_101_to_140.value_counts()) #중복된 개수가 몇개냐

#원하는 데이터를 추가하기
#dayofweek는 Monday ~ sunday -> 0~6으로 리턴
#새로운 List column 별로 추천하지 않음 효율적이지 않다.
start_from_101_to_140['요일'] = pd.to_datetime(start_from_101_to_140['집계일자'],format='%Y%m%d').dt.dayofweek
# print(start_from_101_to_140.head())

#.loc[] 추천함 효율적이다.
start_from_101_to_140.loc[:,'요일'] = pd.to_datetime(start_from_101_to_140['집계일자'],format='%Y%m%d').dt.dayofweek
# print(start_from_101_to_140.head())

#.assign()
start_from_101_to_140 = start_from_101_to_140.assign(요일=pd.to_datetime(start_from_101_to_140['집계일자'],format='%Y%m%d').dt.dayofweek)
# print(start_from_101_to_140.dtypes)

#Sort & Group Data
# print(start_from_101_to_140.sort_values(by=['통행시간']))
# print(start_from_101_to_140.sort_values(by=['통행시간'],ascending=False))
# print(start_from_101_to_140.sort_values(by=['집계일자','집계시'],ascending = False))
# print(start_from_101_to_140.groupby(start_from_101_to_140['도착영업소코드']).mean())
# print(start_from_101_to_140['통행시간'].groupby(start_from_101_to_140['도착영업소코드']).mean())
groupby_destination = start_from_101_to_140['통행시간'].groupby(start_from_101_to_140['도착영업소코드'])
# print(groupby_destination.size())
# print(groupby_destination.sum())
# print(groupby_destination.mean())
# print(groupby_destination.max())
# print(groupby_destination.min())

#Save_Data
output = "data/data_202003.csv"
start_from_101_to_140.to_csv(output,index=None,header = True)

#Merge Data
data_202001 = pd.read_csv("./data/data_202001.csv")
data_202002 = pd.read_csv("./data/data_202002.csv")
data_202003 = pd.read_csv("./data/data_202003.csv")

data_2020 = pd.concat([data_202001,data_202002,data_202003],ignore_index=True,sort=False).set_index('통행시간')
data_2020.head()

final_ = "data/data_2020.csv"
data_2020.to_csv(final_,index = None , header=True)
