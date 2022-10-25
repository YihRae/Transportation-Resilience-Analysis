import pandas as pd
import time


f_name = 'road_speed_data.csv'
df = pd.read_csv(f_name, index_col=0)
time_st = 0
for i in range(df.shape[0]):
    df.loc[i, 'TIME'] = df.loc[i, 'TIME'].split(' ')[0]
    if df.loc[i, 'GOTIME'] < 0.001:
        df.loc[i, 'GOLEN'] = 0
    else:
        df.loc[i, 'GOLEN'] /= (df.loc[i, 'GOTIME'] * 5 / 18)  # 单位换算
    if i % 1000 == 0:
        time_ed = time.perf_counter()
        print(i, time_ed - time_st)
        time_st = time_ed
df.columns = ['SPEED', 'ID', 'TIMESLICE', 'AMOUNT', 'DATE', 'GOTIME']
df_class = df['DATE'].unique()
for c in df_class:
    print(c)
    df[df['DATE'].isin([c])].sort_values(by=['TIMESLICE', 'ID'])\
        .reset_index(drop=True).to_csv(f_name[:-4]+'_'+str(c)[-4:]+'.csv')