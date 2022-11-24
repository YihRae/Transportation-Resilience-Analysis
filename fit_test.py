# 拟合曲线
import numpy as np
import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.stats import ks_2samp


def power_random(x, p):
    return x * pow(1 - rd.random(), 1 / (1 - p))


# 需要拟合的函数func（）指定函数的形状
def func(p, x):
    k, b = p
    return k * x + b


# 定义偏差函数，x，y为数组中对应Xi,Yi的值
def error(p, x, y):
    return func(p, x) - y


def work(lim, F_data, N_data):
    num = len(F_data)
    tol = sum(N_data)
    pre = [0 for i in range(num)]
    pre[0] = N_data[0]
    lnF = []
    lnN = []
    for i in range(1, num):
        pre[i] = pre[i - 1] + N_data[i]
    for i in F_data:
        lnF.append(np.log(i))
    for i in range(num):
        lnN.append(np.log(pre[i] / tol))
    while len(lnF) != 0:
        if lnF[0] > lim:
            lnF.pop(0)
            lnN.pop(0)
        else:
            break
    Xi = np.array(lnF)
    Yi = np.array(lnN)
    # 设置k，b的初始值，可以任意设定，经过实验，发现p0的值会影响cost的值：Para[1]
    p0 = np.array([1, 10])
    # 把error函数中除了p0以外的参数打包到args中,leastsq()为最小二乘法函数
    Para = leastsq(error, p0, args=(Xi, Yi))
    # 读取结果
    k, b = Para[0]
    return -k + 1, math.exp(- b / k)


if __name__ == '__main__':
    ans = []
    dx = []
    xx = [[], [], [], [], [], [], [], []]
    st = 0
    gp = 10
    p_val = []
    accept_num = 0
    for i in range(st, 70):
        lim = 4.6
        xmin = 7
        file_name = './data/result_speed/F/' + str(i) + 'F.xlsx'
        df = pd.read_excel(file_name, index_col=0).reset_index(drop=True)
        F_data = df['F'].values.tolist()  # 读入 F N 数据
        N_data = df['N'].values.tolist()
        test_num = []
        for j in range(len(F_data)):
            if math.log(F_data[j]) > lim:
                continue
            if F_data[j] < xmin:
                continue
            for num in range(N_data[j]):
                test_num.append(F_data[j])
        k, b = work(lim, F_data, N_data)
        # print(k)
        xx[(i - st) // gp].append(k)
        ans.append(k)
        dx.append(100 + (i // gp) * 50)
        sample = []
        sample_num = 5000
        for j in range(sample_num):
            # sample.append(power_random(1, ans[i - st]))
            sample.append(int(power_random(xmin - 0.5, ans[i - st])+0.5))
        sample.sort(reverse=True)
        ss = []
        for j in sample:
            if math.log(j) <= lim:
                ss.append(j)
        D, p = ks_2samp(test_num, ss)
        print(str(i), ans[i-st], D, p)
        if p > 0.1:
            accept_num += 1
    print("accept:", accept_num)
    plt.title("Space Correlation")
    plt.scatter(dx, ans, color='blue', s=2, marker='.', label='point', linewidth=2)
    print(xx)
    for i in range((70 - st) // gp):
        print(dx[i * gp])
        plt.text(dx[i * gp], min(xx[i]), str(round(min(xx[i]), 3)), size=7)
        plt.text(dx[i * gp], max(xx[i]), str(round(max(xx[i]), 3)), size=7)
    plt.legend()  # 绘制图例
    plt.ylim(1, 3)
    plt.xlabel('scale')
    plt.ylabel('power')
    plt.savefig("1.png")
    plt.grid(1)
    plt.show()
    # ans = []
    # for i in range(5):
    #     lim = 3.0
    #     file_name = './cal/FF' + str(72 + i * 30) + '.csv'
    #     df = pd.read_csv(file_name, index_col=0).reset_index(drop=True)
    #     F_data = df['F'].values.tolist()  # 读入 F N 数据
    #     N_data = df['N'].values.tolist()
    #     test_num = []
    #     for j in range(len(F_data)):
    #         if math.log(F_data[j]) > lim:
    #             continue
    #         for num in range(N_data[j]):
    #             test_num.append(F_data[j])
    #     k, b = work(lim, F_data, N_data)
    #     print(k)
    #     ans.append(k)
    #     sample = []
    #     sample_num = 300
    #     for j in range(sample_num):
    #         # sample.append(power_random(1, ans[i - st]))
    #         sample.append(int(power_random(1, ans[i])+0.5))
    #     ss = []
    #     for j in sample:
    #         if math.log(j) <= lim:
    #             ss.append(j)
    #     D, p = ks_2samp(test_num, ss)
    #     print(str(i), D, p)
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
