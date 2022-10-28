# 创建交通时序网络（一个节点在相邻时间片连的是无向边）并计算
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random as rd
import xlwt


def divide_graph(n_data, h_time, t_time):
    slice_class = n_data['TIMESLICE'].unique()
    h_time = min(h_time, len(slice_class) - 1)
    t_time = min(t_time, len(slice_class) - 1)
    divide_net = [n_data[n_data['TIMESLICE'].isin([c])].reset_index(drop=True)
                  for c in slice_class]
    return slice_class[h_time], slice_class[t_time], divide_net[h_time: t_time + 1]


def build(v_size, e_data, e_id, n_data, h_time, t_time):
    edge_ret = []
    t_min, t_max, divide_net = divide_graph(n_data, h_time, t_time)
    time_len = t_max - t_min + 1

    def cal_idx(idx, timeslice, vsize):
        return idx + vsize * timeslice

    def add(u, v, w):
        edge_ret[u].append((v, w))

    dict_edge = {}
    edge_ret = [[] for _ in range(v_size * time_len + 5)]
    for i in range(e_id.shape[0]):
        dict_edge[e_id.loc[i, 'ID']] = e_id.loc[i, 'INDEX']
    for i in range(1, time_len):
        for j in range(v_size):
            add(cal_idx(j, i, v_size), cal_idx(j, i - 1, v_size), 0)
            add(cal_idx(j, i - 1, v_size), cal_idx(j, i, v_size), 0)
    for net_part in divide_net:
        t_slice = net_part.loc[0, 'TIMESLICE'] - t_min
        for i in range(net_part.shape[0]):
            cur_id = net_part.loc[i, 'ID']
            cur_idx = int(dict_edge.get(cur_id, '0'))
            if cur_idx == 0:
                continue
            if e_data.loc[cur_idx, 'JAM'] - net_part.loc[i, 'SPEED'] > 0:
                cur_fr = e_data.loc[cur_idx, 'FR']
                cur_to = e_data.loc[cur_idx, 'TO']
                add(cal_idx(cur_fr, t_slice, v_size),
                    cal_idx(cur_to, t_slice, v_size), 1)
    return t_min, t_max, time_len, edge_ret


def cal_res(t_len, init_vsize, edge, file_n, file_save, v_c_cnt):
    v_size = init_vsize * t_len
    vis = [False for _ in range(v_size)]
    ret = []
    st = []
    c_st = []
    c_ed = []
    t_data = []
    for ver in range(v_size):
        if vis[ver]:
            continue
        st.append(ver)
        vis[ver] = True
        res = 0
        cur_tmin = ver // init_vsize
        cur_tmax = 0
        ed_tmp = ''
        while len(st) > 0:
            cur = st[-1]
            st.pop()
            flag = False
            for e in edge[cur]:
                if int(e[1]) == 1:
                    flag = True
                    break
            if not flag:
                if ed_tmp != '':
                    ed_tmp += '_'
                ed_tmp += str(cur % init_vsize)
                continue
            cur_tmax = max(cur_tmax, cur // init_vsize)
            for e in edge[cur]:
                lst = int(e[0])
                res += int(e[1])
                if not vis[lst]:
                    vis[lst] = True
                    st.append(lst)
        if res > 0:
            cur_id = ver % init_vsize
            v_c_cnt[cur_id].append(res)
            c_ed.append(ed_tmp)
            t_data.append(cur_tmax - cur_tmin + 1)
            c_st.append(cur_id)
            ret.append(res)
    df = pd.DataFrame({'F': ret, 'T': t_data, 'S': c_st, 'E': c_ed})
    df.to_csv(file_save + '/result_' + file_n + '.csv')
    sns.distplot(df['F'], hist=True, kde=True, bins=500)
    plt.savefig(file_save + "/frequency_" + file_n + '.jpg')
    # plt.show()


if __name__ == '__main__':
    file_head = './data/dataset/speed/road_speed_data_4-'
    file_list = []
    for i in range(9, 14):
        if i < 10:
            file_list.append(file_head + '0' + str(i) + '.csv')
        else:
            file_list.append(file_head + str(i) + '.csv')
    # 读取路网
    vertex_data = pd.read_csv('data/graph/vertex_data.csv', index_col=0)
    edge_data = pd.read_csv('data/graph/edge_data.csv', index_col=0)
    edge_id = pd.read_csv('data/graph/edge_id.csv', index_col=0)
    vertex_size = vertex_data.shape[0]
    head_time = 0
    tail_time = 287
    # 0615时间片不全 0620数据极少 0619和0620为周末其余为工作日
    net_data = [pd.read_csv(f_name, usecols=['SPEED', 'DATE',
                                             'TIMESLICE', 'ID']) for f_name in file_list]
    cnt = 5
    vertex_cluster = [[] for _ in range(vertex_size + 5)]
    for net in net_data:
        time_min, time_max, slice_len, edge_set = build(vertex_size, edge_data, edge_id,
                                                        net, head_time, tail_time)
        cnt += 1
        cal_res(time_max - time_min + 1, vertex_size, edge_set, str(cnt),
                './data/result_speed', vertex_cluster)
    xl =[xlwt.Workbook() for _ in range((vertex_size + 19) // 20 + 2)]
    xl_sh = xl[0].add_sheet('result')
    cnt = 0
    xlid = 0
    for i in range(vertex_size):
        num = sum(vertex_cluster[i])
        if num == 0:
            continue
        xl_sh.write(0, cnt * 2, i)
        xl_sh.write(1, cnt * 2, num)
        d_tmp = {}
        for j in range(len(vertex_cluster[i])):
            if d_tmp.get(vertex_cluster[i][j], 0) == 0:
                d_tmp[vertex_cluster[i][j]] = 1
            else:
                d_tmp[vertex_cluster[i][j]] += 1
        num = 0
        for d_key in d_tmp:
            xl_sh.write(num + 2, cnt * 2, d_key)
            xl_sh.write(num + 2, cnt * 2 + 1, d_tmp[d_key])
            num += 1
        cnt += 1
        if cnt == 20:
            cnt = 0
            xl[xlid].save('./data/result_speed/cluster/cluster' + str(xlid) + '.xls')
            xlid += 1
            xl_sh = xl[xlid].add_sheet('result')
    if cnt > 0:
        xl[xlid].save('./data/result_speed/cluster/cluster' + str(xlid) + '.xls')
    # for thenum in range(5):
    #     idx = [rd.randint(0, vertex_size - 1) for _ in range(400)]
    #     d_cv = {}
    #     for i in idx:
    #         for j in range(len(vertex_cluster[i])):
    #             if d_cv.get(vertex_cluster[i][j], 0) == 0:
    #                 d_cv[vertex_cluster[i][j]] = 1
    #             else:
    #                 d_cv[vertex_cluster[i][j]] += 1
    #     pd.DataFrame({'F': d_cv.keys(), 'N': d_cv.values()}) \
    #         .sort_values(by=['F'], ascending=False).to_excel(str(thenum) + 'F.xlsx')
