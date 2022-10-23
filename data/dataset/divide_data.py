import pandas as pd
f_name = 'GM_road_speed_data.csv'
df = pd.read_csv(f_name, index_col=0)
df_class = df['DATE'].unique()
for c in df_class:
    df[df['DATE'].isin([c])].sort_values(by=['TIMESLICE', 'ID'])\
        .reset_index(drop=True).to_csv(f_name[:-4]+'_'+str(c)[-4:]+'.csv')