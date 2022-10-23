# 合并格式相同的csv文件
# 用于由于内存不足导致的分开存储的数据集的合并
import pandas as pd
init_file = ['GPS_data_1.csv', 'GPS_data_2.csv']  # 输入待合并的文件名
pd_file = []
result_file = './dataset/GPS_data.csv'
for file in init_file:
    pd_file.append(pd.read_csv('./dataset/'+file, index_col=0))
pd.concat(pd_file, ignore_index=True).to_csv(result_file)