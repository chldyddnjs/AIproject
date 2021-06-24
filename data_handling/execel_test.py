import pandas as pd
file = 'data/1.xlsx'
data = pd.read_excel(file)

data_test = data[data['발송여부'] == '입금완료']
print(data)
print(data_test)
final_file = 'data/1_test.xlsx'
data_test.to_excel(final_file,index=None,header=True)
