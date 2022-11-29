# diffcache_dse.py
# 模拟退火算法构建DSE
# v1:
#   四核CPU，两级cache，benchmark为machsuite的fft/gemm/sort，gem5自带的linux hello，优化cache配置使得Rank0.totalenergy + Rank1.totalenergy最小
#   两级cache都可以指定大小，每个CPU cache大小也可以不一样


import math                         
import random                       
import pandas as pd                 
import numpy as np
from cmd import Cmd
import os
import re
import pickle
import datetime
import matplotlib.pyplot as plt
from copy import deepcopy


# 定义设计空间
def ParameterSetting(cfg, num_cpus):
    # cfg[]的前num_cpu为各个CPU L1cache对应的取值编号，后num_cpu为各个CPU L2cache对应的取值编号
    l1_size_area = ['1kB', '2kB', '4kB', '8kB', '16kB', '32kB', '64kB']
    l2_size_area = ['32kB', '64kB', '128kB', '256kB', '512kB', '1MB', '2MB']
    cache_size = []
    for i in range(num_cpus):
        cache_size.append(l1_size_area[cfg[i]])
    for j in range(num_cpus, 2*num_cpus):
        cache_size.append(l2_size_area[cfg[j]])
    return deepcopy(cache_size)


# 运行gem5配置，定义/提取优化的目标
# 运行gem5配置，定义/提取优化的目标
def Get_OptObjective(cache_size, num_cpus):
    # 传参运行gem5
    l1_size = ''
    l2_size = ''
    Num_Cpus = num_cpus
    print("cache size length is:", len(cache_size))
    for i in range(Num_Cpus):
        l1_size += str(cache_size[i]) + ';'
    for j in range(Num_Cpus, 2*Num_Cpus):
        l2_size += str(cache_size[j]) + ';'
    os.environ["L1_SIZE"] = l1_size  
    os.environ["L2_SIZE"] = l2_size
    os.environ["NUM_CPUS"] = str(Num_Cpus)
    os.system("echo $L1_SIZE $L2_SIZE")
    cmd = 'bash diffcache_run.sh'
    print(cmd)
    os.system(cmd)
    cmd = 'mv m5out/stats.txt m5out/Multicore_result'
    print(cmd)
    os.system(cmd)
    cmd = 'mv m5out/config.ini m5out/Multicore_config'
    print(cmd)
    os.system(cmd)

    # 提取所需优化的目标
    file_name = 'm5out/Multicore_result/stats.txt'
    line0_number = 0
    line1_number = 0
    strVal0 = 'system.mem_ctrls.dram.rank0.totalEnergy'
    strVal1 = 'system.mem_ctrls.dram.rank1.totalEnergy'
    with open(file_name, 'r') as file:
        for line0 in file.readlines():
            line0_number += 1
            if strVal0 in line0.strip():
                obj0 = (float)(line0.split()[1])
                break
    with open(file_name, 'r') as file:
        for line1 in file.readlines():
            line1_number += 1
            if strVal1 in line1.strip():
                obj1 = (float)(line1.split()[1])
                break    
    obj = obj0 + obj1
    return obj/math.pow(10,7)


# 模拟退火算法
def Optimization_SA(Tinit, Tfinal, alpha, Num_Markov, num_cpus):
    print("############################## DSE starts! ##############################")
    # 初始化各个参数配置
    cfg_init = []
    for i in range(num_cpus):
        cfg_init.append(random.randint(0,6))
    for j in range(num_cpus, 2*num_cpus):
        cfg_init.append(random.randint(0,6))
    cache_size_init = ParameterSetting(cfg_init, num_cpus)
    # 调用Get_OptObjective获得当前配置下的输出目标函数值
    obj_init = Get_OptObjective(cache_size_init, num_cpus)
    print("Initial multicore cache size are:", cache_size_init)
    print("Initial value of optimization objective is:", obj_init)
    print("***************************************************************************")

    print("************************* Begin searching...... ***************************")
    cfg_best = cfg_init
    cfg_new = []
    for i in range(num_cpus):
        cfg_new.append(0)
    cfg_now = cfg_init
    obj_now = obj_init
    obj_best = obj_init

    totalMar = 0                    # 总计 Markov 链长度
    kIter = 0                       # 外循环迭代次数，温度状态数
    totalImprove = 0                # obj 改善次数
    new_param = 0                   # 产生新配置时变的参数，范围为[0：l1icache, 1:lidcache, 2:l2cache]
    disturb_range = [-1, 1, -2, 2]

    # 画图所需参数
    iter = [0]  # 每次新配置即为一次迭代
    update = 0  # 更新配置的次数
    objfunc = [obj_init] # 更新配置之后得到的目标函数值

    # 开始模拟退火优化
    Tnow = Tinit

    while Tnow >= Tfinal:       # 外循环，温度降到一定程度才会结束搜索
        # 在当前温度下，进行充分次数(nMarkov)的状态转移以达到热平衡
        kBetter = 0                 # 获得优质解的次数
        kBadAccept = 0              # 接受劣质解的次数
        kBadRefuse = 0              # 拒绝劣质解的次数

        # 内循环，开始进行扰动探索空间
        # 简单起见保留其中两个变量不变，只改动一个变量
        # Num_Markov表示=Markov链长度，也即内循环运行次数
        for k in range(Num_Markov):
            totalMar = totalMar + 1
            new_param = random.randint(0,1)            # 设置一个参数，如果为0随机修改一个CPU L1cache大小；如果为1随即修改一个CPU L2cache大小
            cfg_new = cfg_now
            if new_param == 0:
                l1_new = random.randint(0,num_cpus-1)     # 需要更换的l1 cache是哪个cpu
                cfg_new[l1_new] = random.randint(0,6)
            if new_param == 1:
                l2_new = random.randint(0,num_cpus-1) + num_cpus    # 需要更换的l2 cache是哪个cpu
                cfg_new[l2_new] = random.randint(0,6)
            # 计算新的配置下目标函数值
            cache_size = ParameterSetting(cfg_new, num_cpus)
            obj_new = Get_OptObjective(cache_size, num_cpus)
            delta_obj = obj_new - obj_now

            # 进行判断是否接受新解
            # obj更优直接接受，更好解数目加一
            if obj_new < obj_now:
                accept = True
                kBetter = kBetter + 1
            # 若解更差，根据 Metropolis 准则决定是否接受新解
            else:   
                pAccept = math.exp(-delta_obj / Tnow)
                if pAccept > random.random():   # 接受劣质解
                    accept = True
                    kBadAccept = kBadAccept + 1
                    print("The temperature is %f and the pAccept = %f" % (Tnow, pAccept))
                else:
                    accept = False
                    kBadRefuse = kBadRefuse + 1

            # 保存新解
            if accept == True:
                cfg_now = cfg_new
                obj_now = obj_new
                update = update + 1
                iter.append(update)
                objfunc.append(obj_new)
                if obj_new < obj_best:
                    obj_best = obj_new
                    cfg_best = cfg_new
                    totalImprove = totalImprove + 1

            # 输出内循环结束后的数据
            print("######################### %d Inner Loop Result################################" % totalMar)
            cache_size_inner_best = ParameterSetting(cfg_best, num_cpus)
            print("Inner loop best cache configuration is:", cache_size_inner_best)
            print("The value of optimization objective is : ", obj_best)
            print("######################### %d Inner Loop Result################################" % totalMar)
            print("\n\n")

        # 内循环结束，更新温度和外循环次数
        # alpha 代表降温系数
        Tnow = Tnow * alpha            
        kIter =  kIter + 1


    # 退出外层循环，输出最后结果
    print("##############################The final DSE result##############################")
    cache_size_final_best = ParameterSetting(cfg_best, num_cpus)
    print("Final best DSE cache configuration is:", cache_size_final_best)
    print("The minimum (dram.rank1.totalEnergy + dram.rank1.totalEnergy) is :", obj_best*math.pow(10,7), " pJ.")
    print("\n\n\n")
    print("############################## DSE Finished! ##############################")

    # 将迭代产生的目标函数值可视化
    plt.plot(iter,objfunc)
    plt.xlabel('Iteration')
    plt.ylabel('Objective_value')
    plt.savefig("diffcache_sa.jpg")


def main():
    starttime = datetime.datetime.now()
    Optimization_SA(200, 20, 0.7, 8, 4)
    # Tinit, Tfinal, alpha, Num_Markov, num_cpus
    endtime = datetime.datetime.now()
    run_time = ((endtime - starttime).seconds) / 60
    print("Total running time: %f minutes" % run_time)



if __name__ == '__main__':
    main()
