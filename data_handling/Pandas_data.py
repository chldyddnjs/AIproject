#전처리를 위한 분석데이터셋 만들기
from typing import NoReturn
import pandas as pd

INPUT_PREFIX = './data/TCS_영업소간통행시간_1시간_1개월_2020'
OUTPUT_PREFIX = './data/data_2020_1_12'
OUTPUT_EXTENSION = '.csv'

output_dataframes = [] #데이터파일담을 배열

def generateData(month):
    month_string = str(month)
    length_month_string = len(month_string)
    if length_month_string == 1:
        month_string = '0' + month_string
    input_file = INPUT_PREFIX + month_string
    output_file = OUTPUT_EXTENSION + month_string + OUTPUT_EXTENSION
    print('INPUT :',input_file, ' OUTPUT :', output_file)
    data = pd.read_csv(input_file,sep=",",encoding="euc-kr")
    # data_clean = data.drop(['Unnamed: 6'], axis='columns') #데이터 결측
    # data_clean = data_clean[data_clean.통행시간 > 0] # NULL값 버리기
    df_data = pd.DataFrame(data,columns=['집계일자','집계시','출발영업소코드','도착영업소코드','통행시간','요일']) #필요한 속성가져오기
    start_from_101 = df_data[df_data.출발영업소코드 == 101] #필요한 데이터 가져오기
    start_from_101_to_140 = start_from_101[start_from_101['도착영업소코드'].isin([105,110,115,120,125,130,135,140])] #필요한 데이터가져오기
    start_from_101_to_140 = start_from_101_to_140.assign(요일=pd.to_datetime(start_from_101_to_140['집계일자'],format='%Y%m%d').dt.dayofweek) #필요한 데이터 추가하기
    start_from_101_to_140.sort_values(by=['집계일자','집계시'],ascending = False) #데이터 정렬하기
    start_from_101_to_140.to_csv(output_file,index=None,header = True) #데이터 저장하기
    output_dataframes.append(start_from_101_to_140)

for month in range(1,13):
    generateData(month)

output_data = pd.concat(output_dataframes,ignore_index=True,sort=False) #데이터 합치기
final = OUTPUT_PREFIX + OUTPUT_EXTENSION
output_data.to_csv(final,index=None,header=True)