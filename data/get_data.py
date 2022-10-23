# 深圳市政府公开数据集调用

import requests
import pandas as pd
import time

import warnings

warnings.filterwarnings("ignore")

# 参数设置
RequestURL = 'https://opendata.sz.gov.cn/api/29200_00403602/1/service.xhtml'
Rows = 5000
DataSize = 2133696
PageSize = (DataSize + Rows - 1) // Rows
appKey = '6afc6b089c694e6dbe4dfc266d404e67'
header = headers = {'User-Agent': 'Custom'}
FileName = 'GPS_data_2.csv'

# 测试 返回200说明设置成功
print('Page Size:', PageSize)
strhtml = requests.get(RequestURL + '?appKey=' + appKey + '&page=1&rows=1',
                       headers=header)
print(strhtml.status_code)

# 读取
pd_data = []
for page in range(300 + 1, PageSize + 1):
    URL = RequestURL + '?appKey=' + appKey + \
          '&page=' + str(page) + '&rows=' + str(Rows)
    num = 0
    time_st = time.perf_counter()
    while True:  # 有可能读取失败 重复读取直到成功
        num = num + 1
        try:
            strhtml = requests.get(URL, headers=header)
            print(page, 'Getting:', num, 'times',
                  time.perf_counter() - time_st, 'seconds')
            break
        except Exception as e:
            continue
    strhtml.encoding = 'utf8'
    InitData = strhtml.json()['data']
    time_st = time.perf_counter()
    d = len(InitData)
    if page != PageSize:
        d = d - 1
    for r in range(0, d):
        pd_temp = pd.DataFrame.from_dict(InitData[r], orient='index').T
        pd_data.append(pd_temp)
    print(page, 'Writing:', time.perf_counter() - time_st, 'seconds')

# 存入csv 如果存xlsx可能行数超上限
pd.concat(pd_data, ignore_index=True).to_csv('./dataset/' + FileName)
