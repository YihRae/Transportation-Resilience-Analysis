import pandas as pd
import igraph as ig

if __name__ == '__main__':
    edge_data = pd.read_csv('data/graph/sub_edge_data.csv', index_col=0)
    edge_size = edge_data.shape[0]
    edge = []
    idx = []
    se = [675303, 148408, 794305, 671104, 34301, 12212, 141402, 14108, 657301, 675404]
    ne = [129101, 512101, 110301, 819201, 2007301, 260301, 239101, 526301, 19301, 599401]
    edge_c = []
    for i in range(edge_size):
        edge.append((edge_data.loc[i, 'FR'], edge_data.loc[i, 'TO']))
        idx.append(edge_data.loc[i, 'ID'])
        clr = 'black'
        for j in se:
            if edge_data.loc[i, 'ID'] == j:
                clr = 'blue'
        for j in ne:
            if edge_data.loc[i, 'ID'] == j:
                clr = 'red'
        edge_c.append(clr)
    g = ig.Graph()
    g.add_vertices(1397)
    g.add_edges(edge)
    g.es['ID'] = idx
    g.es['color'] = edge_c
    print(len(g.connected_components('weak')[0]))
    ig.plot(g, 'x.png', vertex_size=2)
    ID = []
    FR = []
    TO = []
    LEN = []
    JAM = []
    dv = {}
    cnt = 0
    for i in range(edge_size):
        f = False
        for j in g.connected_components('weak')[0]:
            if edge_data.loc[i, 'FR'] == j or edge_data.loc[i, 'TO'] == j:
                f = True
                break
        if f:
            fr = edge_data.loc[i, 'FR']
            to = edge_data.loc[i, 'TO']
            if dv.get(fr, -1) == -1:
                dv[fr] = cnt
                cnt = cnt + 1
            if dv.get(to, -1) == -1:
                dv[to] = cnt
                cnt = cnt + 1
            ID.append(edge_data.loc[i, 'ID'])
            FR.append(dv[fr])
            TO.append(dv[to])
            LEN.append(edge_data.loc[i, 'LEN'])
            JAM.append(edge_data.loc[i, 'JAM'])
    pd.DataFrame({'ID': ID, 'FR': FR, 'TO': TO, 'LEN': LEN, 'JAM': JAM}).sort_values(by=['ID'])\
        .reset_index(drop=True).to_csv('./data/graph/sub_edge_data.csv', encoding='utf-8')
    idx = [i for i in range(edge_size)]
    pd.DataFrame({'ID': ID, 'INDEX': idx}).to_csv('./data/graph/sub_edge_id.csv', encoding='utf-8')
