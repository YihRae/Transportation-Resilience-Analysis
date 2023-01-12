import pandas as pd
import random as rd
import math
from scipy.special import gamma

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


def ine(a, b, c, x, y, z):
    return p2(x) / p2(a) + p2(y) / p2(b) + p2(z) / p2(c) < 1


def crs(e1, e2):
    if ine(e1[3], e1[4], e1[5], e2[0] - e1[0], e2[1] - e1[1], e2[2] - e1[2]):
        return True
    px, py, pz = e2[0] - e1[0], e2[1] - e1[1], e2[2] - e1[2]
    # print(e1, e2)
    tmp = 1 - 1 / pow(p2(px) / p2(e1[3]) + p2(py) / p2(e1[4]) + p2(pz) / p2(e1[5]), 0.5)
    qx, qy, qz = e1[0] + tmp * px, e1[1] + tmp * py, e1[2] + tmp * pz
    return ine(e2[3], e2[4], e2[5], qx - e2[0], qy - e2[1], qz - e2[2])


if __name__ == '__main__':
    # tst = []
    # for i in range(1000):
    #     tst.append(power_random(1, 4))
    # pd.DataFrame({'F': tst}).sort_values(by=['F'], ascending=False) \
    #     .reset_index(drop=True).to_csv('test.csv', encoding='utf-8')
    dl = {}
    ds = {}
    norm = 3.0
    v = p3(gamma(1 + 1 / norm)) / gamma(1 + 3 / norm)
    c = []
    b = 6.0
    PI = math.acos(-1.0)
    s_init = []
    p_s = []
    xp, yp = 20, 20
    xd = [1, -1, 0, 0]
    yd = [0, 0, 1, -1]
    dx = [45, 45, 55, 55]
    dy = [45, 55, 45, 55]
    X, Y, Z = (30, 30, 100)
    N = X * Y * 5
    for i in range(X * Y):
        dl[i] = ds[i] = 0
    for num in range(1):
        cp = [[] for _ in range((X + 1) * (Y + 1))]
        for i in range(X):
            for j in range(Y):
                for k in range(5):
                    z = rd.randint(0, Z)
                    r = power_random(1, b)
                    c.append((i, j, z, r))
                    s_init.append(math.log(8 * p3(r) * v))
                    p_s.append(math.log((i * X + j + 1) / N))
        s_init.sort(reverse=True)
        f = []
        s = [0 for _ in range(N)]
        res = []
        lns = []
        ps = []
        for i in range(N):
            print(i)
            f.append(i)
            ai, bi, ci = c[i][3], c[i][3], c[i][3]
            for k in range(3):
                if c[i][0] == xp + xd[k] and c[i][1] == yp + yd[k]:
                    ci /= 4
                    ai *= 2
                    bi *= 2
            if c[i][0] == xp and c[i][1] == yp:
                ci *= 16
                ai /= 4
                bi /= 4
            for j in range(i):
                if i == 4100 and j == 4095:
                    print('ok')
                p = 0
                # for k in range(3):
                #     p += pow(abs(c[i][k] - c[j][k]), norm)
                # if p < pow(c[i][3] +  c[j][3], norm):
                #     if c[i][2] > c[j][2]:
                #         f[i] = find(f[j], f)
                #     else:
                #         f[j] = find(f[i], f)
                #     break
                aj, bj, cj = c[j][3], c[j][3], c[j][3]
                for k in range(3):
                    if c[j][0] == xp + xd[k] and c[j][1] == yp + yd[k]:
                        cj /= 4
                        aj *= 2
                        bj *= 2
                if c[j][0] == xp and c[j][1] == yp:
                    cj *= 4
                    aj /= 2
                    bj /= 2
                if crs((c[i][0], c[i][1], c[i][2], ai, bi, ci), (c[j][0], c[j][1], c[j][2], aj, bj, cj)):
                    if c[i][2] > c[j][2]:
                        f[i] = find(f[j], f)
                        break
                    else:
                        f[j] = find(f[i], f)
            s[find(i, f)] += 8 * p3(c[i][3]) * v
        for i in range(N):
            if s[i] > 0:
                res.append(s[i])
                cp[c[i][0] + c[i][1] * X].append(s[i])
        for i in range(X * Y):
            dl[i] += sum(cp[i])
            ds[i] += len(cp[i])
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
