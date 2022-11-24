import pandas as pd
import random as rd
from scipy.stats import ks_2samp
from math import log
import matplotlib.pyplot as plt


def power_random(x, p):
    return x * pow(1 - rd.random(), 1 / (1 - p))


def cal(n_set, x_min, x_max, h, l=1.1, r=6.0):
    n = sum(n_set)
    a = 0
    mx = - 10000000
    while l < r:
        val = -n * log(x_min ** (1 - l) - x_max ** (1 - l))
        for i in range(h):
            val += n_set[i] * log((x_min * 2 ** i) ** (1 - l) - (x_min * 2 ** (i + 1)) ** (1 - l))
        if val > mx:
            mx = val
            a = l
        l += 0.01
    return a


def mle(x_set, x_min, h):
    x_max = 2 ** h * x_min
    p = 0
    x_cnt = [0 for _ in range(h)]
    for x in x_set:
        if x < x_min:
            continue
        if x >= x_max:
            break
        while x >= 2 ** (p + 1) * x_min:
            p += 1
        x_cnt[p] += 1
    return cal(x_cnt, x_min, x_max, h)


def ks_test(x_min, a, x_set, sample_num=2000):
    sample = [int(power_random(x_min - 0.5, a) + 0.5) for _ in range(sample_num)]
    test_set = []
    for x in x_set:
        if x >= x_min:
            test_set.append(x)
    d, p = ks_2samp(test_set, sample)
    return p


def fit(x_set):
    p, a, xm, hh = 0, 0, 0, 0
    for x_min in range(1, 9):
        for h in range(5, 10):
            u = mle(x_set, x_min, h)
            v = ks_test(x_min, u, x_set)
            if v > p:
                p = v
                a = u
                xm = x_min
                hh = h
    return p, a, xm, hh


if __name__ == '__main__':
    s = 0
    lim = 100
    g_num = 7
    d_num = 10
    fy = [[] for _ in range(g_num)]
    fx = [100 + i * 50 for i in range(g_num)]
    dx = []
    dy = []
    for k in range(g_num * d_num):
        data = pd.read_excel('./data/result_speed/F/' + str(k) + 'F.xlsx')
        data_set = []
        for i in range(data.shape[0]):
            if data.loc[i, 'F'] >= lim:
                continue
            for j in range(data.loc[i, 'N']):
                data_set.append(data.loc[i, 'F'])
        data_set.sort()
        pv, alpha, data_min, h_num = fit(data_set)
        print(k, round(pv, 3), round(alpha, 2), data_min, h_num)
        fy[k // d_num].append(alpha)
        if pv > 0.1:
            s += 1
    print("Accept:", s)
    plt.title("Space Correlation")
    for i in range(g_num):
        for j in range(d_num):
            if fy[i][j] == max(fy[i]) or fy[i][j] == min(fy[i]):
                continue
            dx.append(fx[i])
            dy.append(fy[i][j])
        plt.text(fx[i], min(fy[i]), str(round(min(fy[i]), 3)), size=7)
        plt.text(fx[i], max(fy[i]), str(round(max(fy[i]), 3)), size=7)
    plt.scatter(dx, dy, color='blue', s=2, marker='.', label='point', linewidth=2)
    plt.legend()  # 绘制图例
    plt.ylim(1, 3)
    plt.xlabel('scale')
    plt.ylabel('power')
    plt.savefig("1.png")
    plt.grid(1)
    plt.show()