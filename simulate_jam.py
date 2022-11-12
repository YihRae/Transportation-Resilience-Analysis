import pandas as pd
import random as rd
import math

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]


def power_random(x, p):
    return x * pow(1 - rd.random(), 1 / (1 - p))


def p2(x):
    return x * x


def p3(x):
    return x * x * x


def find(x, f):
    if f[x] == x:
        return x
    f[x] = find(f[x], f)
    return f[x]


if __name__ == '__main__':
    # tst = []
    # for i in range(1000):
    #     tst.append(power_random(1, 4))
    # pd.DataFrame({'F': tst}).sort_values(by=['F'], ascending=False) \
    #     .reset_index(drop=True).to_csv('test.csv', encoding='utf-8')
    N = 8000
    c = []
    b = 6.0
    PI = math.acos(-1.0)
    s_init = []
    p_s = []
    dx = [45, 45, 55, 55]
    dy = [45, 55, 45, 55]
    X, Y, Z = (100, 100, 100)
    cp = [[] for _ in range((X + 1) * (Y + 1))]
    for _ in range(N):
        tp = rd.randint(0, 10)
        if tp == 0:
            x = rd.randint(0, X)
            y = rd.randint(0, Y)
        else:
            tpp = rd.randint(0, 3)
            x = dx[tpp]
            y = dy[tpp]
        z = rd.randint(0, Z)
        r = power_random(1, b)
        c.append((x, y, z, r))
        s_init.append(math.log(4 / 3 * PI * p3(r)))
        p_s.append(math.log((_ + 1) / N))
    s_init.sort(reverse=True)
    f = []
    s = [0 for _ in range(N)]
    res = []
    lns = []
    ps = []
    for i in range(N):
        print(i)
        f.append(i)
        for j in range(0, i):
            p = 0
            for k in range(3):
                p += p2(c[i][k] - c[j][k])
            if p < p2(c[i][3] + c[j][3]):
                if c[i][2] > c[j][2]:
                    f[i] = find(f[j], f)
                else:
                    f[j] = find(f[i], f)
                break
        s[find(i, f)] += 4 / 3 * p3(c[i][3]) * PI
    for i in range(N):
        if s[i] > 0:
            res.append(s[i])
            cp[c[i][0] + c[i][1] * X].append(s[i])
    dl = {}
    ds = {}
    for i in range(N):
        dl[i] = sum(cp[i])
        ds[i] = len(cp[i])
    pd.DataFrame({'ID': dl.keys(), 'N': dl.values()}).sort_values(by=['N'], ascending=False) \
        .reset_index(drop=True).to_csv('sim_size.csv', encoding='utf-8')
    pd.DataFrame({'ID': ds.keys(), 'N': ds.values()}).sort_values(by=['N'], ascending=False) \
        .reset_index(drop=True).to_csv('sim_num.csv', encoding='utf-8')
    res.sort(reverse=True)
    res_len = len(res)
    for i in range(res_len):
        lns.append(math.log(res[i]))
        ps.append(math.log((i + 1) / res_len))
    pd.DataFrame({'F': res, 'L': lns, 'P': ps}).reset_index(drop=True)\
        .to_csv('sim_jam.csv', encoding='utf-8')
    pd.DataFrame({'F': s_init, 'P': p_s}).reset_index(drop=True)\
        .to_csv('sim_init.csv', encoding='utf-8')
# def build_P(N, M, P):
#     s = 0
#     for i in range(N):
#         for _ in range(M):
#             p = rd.random()
#             P[i].append(p)
#         s += sum(P[i])
#     for i in range(N):
#         for j in range(M):
#             P[i][j] /= s
#
#
# def find_v(p, s):
#     l = 0
#     r = len(s) - 1
#     while l < r:
#         m = (l + r) // 2
#         if s[m] < p:
#             l = m + 1
#         else:
#             r = m
#     return l
#
#
# def build_c(x, y, t, c, N, M, e):
#     a = [(x, y)]
#     hd = 0
#     tl = 0
#     vis = [[False for _ in range(N)] for __ in range(M)]
#     vis[x][y] = True
#     while True:
#         x, y = a[hd]
#         hd += 1
#         for i in range(4):
#             fx = x + dx[i]
#             fy = y + dy[i]
#             if fx < 0 or fx >= N:
#                 continue
#             if fy < 0 or fy >= M:
#                 continue
#             if vis[fx][fy]:
#                 continue
#             vis[fx][fy] = True
#             c -= 1
#             if c == 0:
#                 break
#             e[t][y + x * N][i] = True
#             tl += 1
#             a.append((fx, fy))
#         if c == 0:
#             break
#
#
# def cal_res(V, T, e):
#     vis = [[0 for _ in range(V)] for __ in range(T)]
#     st = []
#     ret = []
#     s = 0
#     for i in range(T):
#         for j in range(V):
#             if vis[i][j]:
#                 continue
#             st.append((i, j))
#             vis[i][j] = True
#             res = 0
#             while len(st) > 0:
#                 t, v = st[-1]
#                 x = v // N
#                 y = v % N
#                 st.pop()
#                 flag = False
#                 for k in range(4):
#                     nxt = (x + dx[k]) * N + y + dy[k]
#                     if e[t][v][k] and not vis[t][nxt]:
#                         vis[t][nxt] = True
#                         st.append((t, nxt))
#                         flag = True
#                         res += 1
#                 if not flag:
#                     continue
#                 if t < T - 1:
#                     st.append((t + 1, v))
#             if res > 0:
#                 s += 1
#                 print(s)
#                 ret.append(res)
#     return ret
#
#
# if __name__ == "__main__":
#     T = 500
#     N = 40
#     M = 40
#     V = N * M
#     P = [[] for _ in range(N)]
#     build_P(N, M, P)
#     s = [0]
#     for i in range(N):
#         for j in range(M):
#             s.append(P[i][j] + s[-1])
#     s[-1] = 1
#     a = - 2.3
#     b = - 3.0
#     c = (a + 1) / (b + 1)
#     d = 1 / c - 1
#     e = [[[False for _ in range(4)] for __ in range(V)] for ___ in range(T)]
#     for i in range(T - 2):
#         for _ in range(20):
#             t = min(min(math.ceil(power_random(1, b)), T - i - 2), 50)
#             if t % 2 == 1:
#                 t += 1
#             p = rd.random()
#             v = find_v(p, s) - 1
#             for j in range(i, i + t // 2):
#                 k = math.ceil(pow(j - i + 1, d))
#                 build_c(v % N, v // N, j, k, N, M, e)
#             for j in range(i + t // 2, i + t):
#                 k = math.ceil(pow(i + t - j + 1, d))
#                 build_c(v % N, v // N, j, k, N, M, e)
#     C = cal_res(V, T, e)
#     d = {}
#     for x in C:
#         if d.get(x, 0) == 0:
#             d[x] = 1
#         else:
#             d[x] += 1
#     pd.DataFrame({'F': d.keys(), 'N': d.values()}).sort_values(by=['F'], ascending=False) \
#         .reset_index(drop=True).to_csv('sim_jam.csv', encoding='utf-8')
