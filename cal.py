import pandas as pd
import numpy as np


def dict_to_csv(dtc, idx1, idx2, durl):
    dtc_k = dtc.keys()
    dtc_v = dtc.values()
    dtc_t = {idx1: dtc_k, idx2: dtc_v}
    pd.DataFrame(dtc_t).to_csv(durl, encoding='utf-8')


file_name = './data/dataset/GM_speed/result/result_0617.csv'
a = []
b = []
df = pd.read_csv(file_name, index_col=0)
k = df.shape[1]
for i in range(k):
    a.append({})
    b.append(np.array(df)[:, i].tolist())
    for x in b[i]:
        if a[i].get(x, 0) == 0:
            a[i][x] = 1
        else:
            a[i][x] += 1
    dict_to_csv(a[i], df.columns[i], 'N', df.columns[i] + '17.csv')