import pandas as pd
import random as rd
from scipy.stats import ks_2samp
from math import log
import matplotlib.pyplot as plt
import numpy as np
import xlwt


def coefficient_of_variation(data):
    mean = np.mean(data)
    std = np.std(data, ddof=0)
    cv = std / mean
    return cv


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


def ks_test(x_min, a, x_set, sample_num=2000, is_int=True):
    if is_int:
        sample = [int(power_random(x_min - 0.5, a) + 0.5) for _ in range(sample_num)]
    else:
        sample = [power_random(x_min, a) for _ in range(sample_num)]
    test_set = []
    for x in x_set:
        if x >= x_min:
            test_set.append(x)
    d, p = ks_2samp(test_set, sample)
    return p


def fit(x_set, is_int=True):
    p, a, xm, hh = 0, 0, 0, 0
    for x_min in range(2, 3):
        for h in range(5, 11):
            u = mle(x_set, x_min, h)
            v = ks_test(x_min, u, x_set, is_int=is_int)
            if v > p:
                p = v
                a = u
                xm = x_min
                hh = h
    return p, a, xm, hh


if __name__ == '__main__':
    # s = 0
    # lim = 100
    # g_num, g_siz, g_init, d_num = 16, 20, 200, 100
    # fy = [[] for _ in range(g_num)]
    # fx = [g_init + i * g_siz for i in range(g_num)]
    # dx = []
    # dy = []
    # xl = xlwt.Workbook()
    # xl_sh = xl.add_sheet('result')
    # for k in range(g_num * d_num):
    #     data = pd.read_excel('./data/result_speed/F/' + str(k) + 'F.xlsx')
    #     data_set = []
    #     for i in range(data.shape[0]):
    #         if data.loc[i, 'F'] >= lim:
    #             continue
    #         for j in range(data.loc[i, 'N']):
    #             data_set.append(data.loc[i, 'F'])
    #     data_set.sort()
    #     pv, alpha, data_min, h_num = fit(data_set)
    #     print(k, round(pv, 3), round(alpha, 2), data_min, h_num)
    #     fy[k // d_num].append(alpha)
    #     xl_sh.write(k % d_num, k // d_num, alpha)
    #     if pv > 0.1:
    #         s += 1
    # xl.save('test_result.xls')
    # print("Accept:", s)
    # plt.title("Space Correlation")
    # for i in range(g_num):
    #     print("CV", i, coefficient_of_variation(fy[i]))
    #     for j in range(d_num):
    #         dx.append(fx[i])
    #         dy.append(fy[i][j])
    #     plt.text(fx[i], np.mean(fy[i]), str(round(np.mean(fy[i]), 3)), size=7)
    #     plt.text(fx[i], min(fy[i]), str(round(min(fy[i]), 3)), size=7)
    #     plt.text(fx[i], max(fy[i]), str(round(max(fy[i]), 3)), size=7)
    # plt.scatter(dx, dy, color='blue', s=2, marker='.', label='point', linewidth=2)
    # plt.legend()  # 绘制图例
    # plt.ylim(1, 3)
    # plt.xlabel('scale')
    # plt.ylabel('power')
    # plt.savefig("1.png")
    # plt.grid(1)
    # plt.show()
    # ans = []
    # for k in range(5):
    #     lim = 100
    #     data = pd.read_csv('./cal/FF' + str(72 + k * 30) + '.csv')
    #     data_set = []
    #     for i in range(data.shape[0]):
    #         if data.loc[i, 'F'] >= lim:
    #             continue
    #         for j in range(data.loc[i, 'N']):
    #             data_set.append(data.loc[i, 'F'])
    #     data_set.sort()
    #     pv, alpha, data_min, h_num = fit(data_set)
    #     print(k, round(pv, 3), round(alpha, 2), data_min, h_num)
    #     ans.append(alpha)
    # plt.title("Time Correlation")
    # xx = [1, 2, 3, 4, 5]
    # plt.scatter(xx, ans, color='blue', s=2, marker='.', label='point', linewidth=2)
    # plt.legend()  # 绘制图例
    # plt.ylim(1, 4)
    # plt.xlabel('scale')
    # plt.ylabel('power')
    # plt.savefig("2.png")
    # plt.grid(1)
    # plt.show()
    N = 500
    for num in range(1, 7):
        data = pd.read_csv('sim_jam_' + str(num) + '.csv')
        data_set = []
        for i in range(data.shape[0]):
            data_set.append(data.loc[i, 'F'])
        print(len(data_set) / (N * num))
        data_set.sort()
        pv, alpha, data_min, h_num = fit(data_set, False)
        print(round(pv, 3), round(alpha, 2), data_min, h_num)
    # file_head = './data/result_speed/result_'
    # fid = [_ for _ in range(6, 19)]
    # for i in fid:
    #     f = file_head + str(i) + '.csv'
    #     data = pd.read_csv(f)
    #     data_set = data['F'].tolist()
    #     data_set.sort()
    #     pv, alpha, data_min, h_num = fit(data_set)
    #     print(i, 'F', round(pv, 3), round(alpha, 2), data_min, h_num)
    #     data_set = data['T'].tolist()
    #     data_set.sort()
    #     pv, alpha, data_min, h_num = fit(data_set)
    #     print(i, 'T', round(pv, 3), round(alpha, 2), data_min, h_num)
    # a = [int(power_random(4 - 0.5, 2.0) + 0.5) for _ in range(1000)]
    # b = [int(power_random(3 - 0.5, 2.5) + 0.5) for _ in range(2000)]
    # c = []
    # for x in a:
    #     c.append(x)
    # for x in b:
    #     c.append(x)
    # for r in range(200, 300):
    #     p = ks_test(4, r/100, b[0: 1000])
    #     print(r/100, p)