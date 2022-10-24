import pandas as pd
import numpy as np


def dict_to_csv(dtc, idx1, idx2, durl):
    dtc_k = dtc.keys()
    dtc_v = dtc.values()
    dtc_t = {idx1: dtc_k, idx2: dtc_v}
    pd.DataFrame(dtc_t).to_csv(durl, encoding='utf-8')


file_name = './data/result/result_0617.csv'
d = {}
e = {}
df = pd.read_csv(file_name)
a = np.array(df)[:, 1].tolist()
b = np.array(df)[:, 2].tolist()
for x in a:
    if d.get(x, 0) == 0:
        d[x] = 1
    else:
        d[x] += 1
for x in b:
    if e.get(x, 0) == 0:
        e[x] = 1
    else:
        e[x] += 1
dict_to_csv(d, 'F', 'N', 'F17.csv')
dict_to_csv(e, 'T', 'N', 'T17.csv')