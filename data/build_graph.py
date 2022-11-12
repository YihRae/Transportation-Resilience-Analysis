#  创建深圳交通路网
import pandas as pd


def dict_to_csv(dtc, idx1, idx2, durl):
    dtc_k = dtc.keys()
    dtc_v = dtc.values()
    dtc_t = {idx1: dtc_k, idx2: dtc_v}
    pd.DataFrame(dtc_t).to_csv(durl, encoding='utf-8')


if __name__ == '__main__':
    r_name = 'ROADSECT_NAME'
    r_to = 'ROADSECT_TO'
    r_id = 'ROADSECT_ID'
    r_from = 'ROADSECT_FROM'
    r_len = 'ROADLENGTH'
    r_jam = 'JAM_SPEED'
    road_network = pd.read_csv('dataset/road_attribute_data.csv',
                               usecols=[r_name, r_to, r_id, r_from, r_len, r_jam])
    road_size = road_network.shape[0]
    junction_id = {}  # 节点（交叉路口）编号
    dict_vertex = {}
    dict_edge = {}
    id_cur = 0
    sum_edge = 0

    edge_data = []
    vertex_data = []
    for idx in range(road_size):
        if road_network.loc[idx, r_name] < road_network.loc[idx, r_from]:
            name_from = (road_network.loc[idx, r_name], road_network.loc[idx, r_from])
        else:
            name_from = (road_network.loc[idx, r_from], road_network.loc[idx, r_name])
        if road_network.loc[idx, r_name]< road_network.loc[idx, r_to]:
            name_to = (road_network.loc[idx, r_name], road_network.loc[idx, r_to])
        else:
            name_to = (road_network.loc[idx, r_to], road_network.loc[idx, r_name])
        if junction_id.get(name_from, -1) == -1:
            junction_id[name_from] = id_cur
            id_cur = id_cur + 1
            vertex_data.append([])
        if junction_id.get(name_to, -1) == -1:
            junction_id[name_to] = id_cur
            id_cur = id_cur + 1
            vertex_data.append([])
        from_id = junction_id[name_from]
        to_id = junction_id[name_to]
        edge_data.append([road_network.loc[idx, r_id], from_id, to_id,
                          road_network.loc[idx, r_len], road_network.loc[idx, r_jam]])
        vertex_data[from_id].append(idx)
        dict_edge[road_network.loc[idx, r_id]] = sum_edge
        sum_edge = sum_edge + 1
    for idx in range(id_cur):
        for i in range(len(vertex_data[idx])):
            vertex_data[idx][i] = str(vertex_data[idx][i])
        dict_vertex[idx] = '_'.join(vertex_data[idx])
    dict_to_csv(junction_id, 'JUNCTION', 'ID', './graph/junction_id.csv')
    pd.DataFrame(edge_data, columns=['ID', 'FR', 'TO', 'LEN', 'JAM']).to_csv('./graph/edge_data.csv', encoding='utf-8')
    dict_to_csv(dict_vertex, 'ID', 'EDGE', './graph/vertex_data.csv')
    dict_to_csv(dict_edge, 'ID', 'INDEX', './graph/edge_id.csv')