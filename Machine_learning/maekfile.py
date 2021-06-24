import pandas as pd
import glob
import os

input_file = r'C:\Users\user\Desktop\data_handling\data'
output_file = r'C:\Users\user\Desktop\AI project\result.csv'

allFile_list = glob.glob(os.path.join(input_file,'data_2020*'))

allData = []
for file in allFile_list:
    df = pd.read_csv(file) #csv 파일을 읽어들인후
    allData.append(df) #삽입

dataCombine = pd.concat(allData,axis=0,ignore_index=True)
dataCombine.to_csv(output_file,index=False)