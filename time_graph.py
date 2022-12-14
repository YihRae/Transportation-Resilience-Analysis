# 创建交通时序网络（一个节点在相邻时间片连的是无向边）并计算
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import xlwt
import random as rd


tmps = []


def divide_graph(n_data, h_time, t_time):
    slice_class = n_data['TIMESLICE'].unique()
    h_time = min(h_time, len(slice_class) - 1)
    t_time = min(t_time, len(slice_class) - 1)
    divide_net = [n_data[n_data['TIMESLICE'].isin([c])].reset_index(drop=True)
                  for c in slice_class]
    s = 0
    for x in divide_net[h_time: t_time + 1]:
        s += sum(x['AMOUNT'])
    tmps.append(s)
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
    for i in range(e_data.shape[0]):
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


def cal_res(t_len, init_vsize, edge, file_n, file_save, e_c_cnt, et, v_2_e):
    v_size = init_vsize * t_len
    vis = [False for _ in range(v_size)]
    ret = []
    st, c_st, c_ed = [], [], []
    t_data = []
    for ver in range(v_size):
        if vis[ver]:
            continue
        st.append(ver)
        vis[ver] = True
        res = 0
        cur_tmin, cur_tmax = ver // init_vsize, 0
        ed_tmp = ''
        init_edge = {}
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
                nxt = int(e[0])
                res += int(e[1])
                if not vis[nxt]:
                    vis[nxt] = True
                    st.append(nxt)
                if int(e[1]) == 1:
                    if cur == ver:
                        init_edge[v_2_e[(cur % init_vsize, nxt % init_vsize)]] = True
                    et[v_2_e[(cur % init_vsize, nxt % init_vsize)]] += 1
        if res > 0:
            for e in init_edge.keys():
                e_c_cnt[e].append(res)
            c_st.append(ver % init_vsize)
            c_ed.append(ed_tmp)
            t_data.append(cur_tmax - cur_tmin + 1)
            ret.append(res)
        # if res > 200:
        #     print(c_monitor[cur_tmin: cur_tmax + 1])
    print(len(ret))
    df = pd.DataFrame({'F': ret, 'T': t_data, 'S': c_st, 'E': c_ed})
    df.to_csv(file_save + '/result_' + file_n + '.csv')
    return df


if __name__ == '__main__':
    file_head = './data/dataset/speed/road_speed_data_4-'
    fid = [9, 10, 11, 12, 13, 16, 17, 18]
    file_list = []
    cnt = 10
    for i in fid:
        if i < 10:
            file_list.append(file_head + '0' + str(i) + '.csv')
        else:
            file_list.append(file_head + str(i) + '.csv')
    # 读取路网
    vertex_data = pd.read_csv('data/graph/vertex_data.csv', index_col=0)
    edge_data = pd.read_csv('data/graph/sub_edge_data.csv', index_col=0)
    edge_id = pd.read_csv('data/graph/sub_edge_id.csv', index_col=0)
    vertex_size = vertex_data.shape[0]
    edge_size = edge_data.shape[0]
    head_time = 0
    tail_time = 167
    # 0615时间片不全 0620数据极少 0619和0620为周末其余为工作日
    net_data = [pd.read_csv(f_name, usecols=['SPEED', 'DATE', 'TIMESLICE', 'ID', 'AMOUNT']) for f_name in file_list]
    edge_cluster = [[] for _ in range(edge_size + 5)]
    ect = [0 for _ in range(edge_size + 5)]
    v_to_e = {}
    for e in range(edge_size):
        v_to_e[(edge_data.loc[e, 'FR'], edge_data.loc[e, 'TO'])] = e
    tf = []
    tmp_source = [0 for _ in range(edge_size)]
    edge_cluster_date = [[] for _ in range(edge_size)]
    xl_source = xlwt.Workbook()
    xl_source_sh = xl_source.add_sheet('result')
    for i in range(len(fid)):
        print(i)
        net = net_data[i]
        time_min, time_max, slice_len, edge_set = build(vertex_size, edge_data, edge_id, net, head_time, tail_time)
        tf.append(cal_res(time_max - time_min + 1, vertex_size, edge_set, str(fid[i]),
                          './data/result_speed', edge_cluster, ect, v_to_e))
        cnt += 1
        for e in range(edge_size):
            edge_cluster_date[e].append(len(edge_cluster[e]) - tmp_source[e])
            tmp_source[e] = len(edge_cluster[e])
    pd.concat(tf).to_csv('./data/result_speed/t.csv')
    xl = [xlwt.Workbook() for _ in range((edge_size + 19) // 20 + 2)]
    xl_sh = xl[0].add_sheet('result')
    cnt, xlid, cnt_source = 0, 0, 0
    ec_num, ec_siz, ec_tim = {}, {}, {}
    ec_id = []
    for i in range(edge_size):
        ec_id.append(edge_id.loc[i, 'ID'])
        siz = sum(edge_cluster[i])
        num = len(edge_cluster[i])
        if num > 80:
            for j in range(len(fid)):
                xl_source_sh.write(cnt_source, j, edge_cluster_date[i][j])
            cnt_source += 1
        ec_siz[i] = siz
        ec_num[i] = num
        ec_tim[i] = ect[i]
        if num == 0:
            continue
        xl_sh.write(0, cnt * 2, i)
        xl_sh.write(1, cnt * 2, siz)
        xl_sh.write(1, cnt * 2 + 1, num)
        d_tmp = {}
        for j in range(len(edge_cluster[i])):
            if d_tmp.get(edge_cluster[i][j], 0) == 0:
                d_tmp[edge_cluster[i][j]] = 1
            else:
                d_tmp[edge_cluster[i][j]] += 1
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
    xl_source.save('source_date.xls')
    if cnt > 0:
        xl[xlid].save('./data/result_speed/cluster/cluster' + str(xlid) + '.xls')
    pd.DataFrame({'ID': ec_id, 'T': ec_tim.values(), 'S': ec_siz.values(), 'N': ec_num.values()}).sort_values(by=['T'], ascending=False) \
        .reset_index(drop=True).to_csv('./data/result_speed/cluster/ec_tim.csv', encoding='utf-8')
    pd.DataFrame({'ID': ec_id, 'S': ec_siz.values(), 'T': ec_tim.values(), 'N': ec_num.values()}).sort_values(by=['S'], ascending=False) \
        .reset_index(drop=True).to_csv('./data/result_speed/cluster/ec_siz.csv', encoding='utf-8')
    pd.DataFrame({'ID': ec_id, 'N': ec_num.values(), 'S': ec_siz.values(), 'T': ec_tim.values()}).sort_values(by=['N'], ascending=False) \
        .reset_index(drop=True).to_csv('./data/result_speed/cluster/ec_num.csv', encoding='utf-8')
    ccnt = 0
    for N in range(200, 501, 20):
        rd_node = {}
        for thenum in range(100):
            idx = [rd.randint(0, edge_size - 1) for _ in range(N)]
            rd_node[thenum] = idx
            d_cv = {}
            for i in idx:
                for j in range(len(edge_cluster[i])):
                    if d_cv.get(edge_cluster[i][j], 0) == 0:
                        d_cv[edge_cluster[i][j]] = 1
                    else:
                        d_cv[edge_cluster[i][j]] += 1
            pd.DataFrame({'F': d_cv.keys(), 'N': d_cv.values()}) \
                .sort_values(by=['F'], ascending=False).to_excel('./data/result_speed/F/' + str(ccnt) + 'F.xlsx')
            ccnt += 1
        pd.DataFrame(rd_node).to_csv('./data/result_speed/F/' + str(N) + 'rd.csv')
