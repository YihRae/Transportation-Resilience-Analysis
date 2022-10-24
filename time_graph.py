# 创建交通时序网络（一个节点在相邻时间片连的是无向边）并计算
import pandas as pd
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="darkgrid")


def cal_idx(idx, timeslice, vsize):
    return idx + vsize * (timeslice - 1)


def build(v_size, e_data, e_id, n_data):
    edge_ret = []

    def add(u, v, w):
        edge_ret[u].append((v, w))

    dict_edge = {}
    slice_class = n_data['TIMESLICE'].unique()
    edge_ret = [[] for i in range(v_size * int(slice_class[-1]) + 5)]
    divide_net = [n_data[n_data['TIMESLICE'].isin([c])].reset_index(drop=True)
                  for c in slice_class]
    for i in range(e_id.shape[0]):
        dict_edge[e_id.loc[i, 'ID']] = e_id.loc[i, 'INDEX']

    for i in range(1, len(slice_class)):
        for j in range(v_size):
            add(cal_idx(j, i, v_size), cal_idx(j, i - 1, v_size), 0)
            add(cal_idx(j, i - 1, v_size), cal_idx(j, i, v_size), 0)
    for net_part in divide_net:
        slice = net_part.loc[0, 'TIMESLICE']
        for i in range(net_part.shape[0]):
            cur_id = net_part.loc[i, 'ID']
            cur_idx = int(dict_edge.get(cur_id, '0'))
            if cur_idx == 0:
                continue
            if e_data.loc[cur_idx, 'JAM'] > net_part.loc[i, 'SPEED']:
                cur_fr = e_data.loc[cur_idx, 'FR']
                cur_to = e_data.loc[cur_idx, 'TO']
                add(cal_idx(cur_fr, slice, v_size), cal_idx(cur_to, slice, v_size), 1)
    return int(slice_class[-1]), edge_ret


def cal_res(v_size, edge, file_n):
    vis = [False for _ in range(v_size)]
    ret = []
    st = []
    for ver in range(v_size):
        if vis[ver]:
            continue
        st.append(ver)
        vis[ver] = True
        res = 0
        while len(st) > 0:
            cur = st[-1]
            st.pop()
            flag = False
            for e in edge[cur]:
                if int(e[1]) == 1:
                    flag = True
                    break
            if not flag:
                continue
            for e in edge[cur]:
                lst = int(e[0])
                res += int(e[1])
                if not vis[lst]:
                    vis[lst] = True
                    st.append(lst)
        if res > 0:
            ret.append(res)
    df = pd.DataFrame(ret, columns=['F'])
    df.to_csv('./data/result/result_' + file_n + '.csv')
    sns.distplot(df['F'], hist=True, kde=True, bins=30)
    plt.savefig("./data/result/frequency_" + file_n + '.jpg')
    plt.show()


if __name__ == '__main__':
    f_name = './data/dataset/GM_road_speed_data' + '_' + '0617' + '.csv'
    # 0615时间片不全 0620数据极少 0619和0620为周末其余为工作日
    net_data = pd.read_csv(f_name, usecols=['SPEED', 'DATE',
                                            'TIMESLICE', 'ID'])

    # 读取路网
    vertex_data = pd.read_csv('data/graph/vertex_data.csv', index_col=0)
    edge_data = pd.read_csv('data/graph/edge_data.csv', index_col=0)
    edge_id = pd.read_csv('data/graph/edge_id.csv', index_col=0)
    vertex_size = vertex_data.shape[0]
    slice_max, edge = build(vertex_size, edge_data, edge_id, net_data)
    cal_res(vertex_size * slice_max, edge, '0617')
