# dse.py
# 模拟退火算法构建多核DSE
# v1:
#   4x4 Mesh(12 DerivO3CPU, 2 LLC, 2DDRC)
#   设计空间包括：拓扑类型，各个处理单元的摆放位置，LLC大小

import math                         
import random                                      
import os
import datetime
import matplotlib.pyplot as plt
from copy import deepcopy


def GetObjective(llc_size, location):
    # 传参运行gem5
    Location = ''
    for i in location:
        Location = Location + str(i) + ';'
    print(Location)
    LOCATION = Location.strip(';')
    print(LOCATION)
    LLC_SIZE = llc_size
    os.environ["LOCATION"] = LOCATION
    os.environ["LLC_SIZE"] = LLC_SIZE
    os.system("echo $LOCATION $LLC_SIZE")
    cmd = 'bash dse_run.sh'
    print(cmd)
    os.system(cmd)

    filename = "m5out/stats.txt"
    strVal0 = "simOps"
    line0_number = 0
    with open(filename, 'r') as file:
        for line0 in file.readlines():
            line0_number += 1
            if strVal0 in line0.strip():
                obj0 = (float)(line0.split()[1])
                break
    strVal1 = "simSeconds"
    line1_number = 0
    with open(filename, 'r') as file:
        for line1 in file.readlines():
            line1_number += 1
            if strVal1 in line1.strip():
                obj1 = (float)(line1.split()[1])
                break
    return obj0 / obj1 / math.pow(10, 5)


def Optimization_SA(Tinit, Tfinal, alpha, Num_Markov):
    # 设置LLC尺寸范围
    LLC_size = ['512kB', '1MB', '2MB', '4MB', '8MB', '16MB']

    print("DSE starts!".center(40, "*"))

    # 初始化各个参数配置
    cfg_init = 0
    location_init = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # location = "0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15"
    obj_init = GetObjective(LLC_size[cfg_init], location_init)
    print("Initial LLC size is:", LLC_size[cfg_init])
    print("Initial location is:", location_init)
    print("Begin searching......".center(40, "*"))

    cfg_best = cfg_init
    cfg_new = 0
    cfg_now = cfg_init

    location_best = deepcopy(location_init)
    location_now = deepcopy(location_init)
    location_new = deepcopy(location_init)

    obj_now = obj_init
    obj_best = obj_init

    totalMar = 0                    # 总计 Markov 链长度
    kIter = 0                       # 外循环迭代次数，温度状态数
    totalImprove = 0                # obj 改善次数
    new_param = 0                   # 产生新配置时变的参数，0, 1, 2, 3改变位置，4改变LLC尺寸
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
            new_param = random.randint(0,4)            # 设置一个参数，如果为0随机修改一个CPU L1cache大小；如果为1随即修改一个CPU L2cache大小
            cfg_new = cfg_now
            while new_param == 0 or new_param == 1 or new_param == 2 or new_param == 3: 
                print("Change location!".center(30, "*"))               
                change1 = random.randint(0, 15)
                change2 = random.randint(0, 15)
                location_new = deepcopy(location_now)
                if change1 != change2:
                    print("now location ={}".format(location_now).center(100, '#'))
                    print('change location at', change1, 'and', change2)
                    location_new[change1] = location_now[change2]
                    location_new[change2] = location_now[change1]
                    print('new location ={}'.format(location_new).center(100, '#'))
                    break
                else:
                    print('change1 = change2, change location at', change1, 'and', len(location_now)-change1)
                    location_new[change1], location_new[len(location_init)-change1-1] = location_now[len(location_now)-change1-1], location_now[change1]
                    print('new location ={}'.format(location_new).center(100, '#'))
                    break
            while new_param == 4:
                print("Change LLC size".center(30, "*"))   
                cfg_new_p = cfg_now + disturb_range[random.randint(0,3)]
                if 0 <= cfg_new_p <= 5:
                    cfg_new = cfg_new_p
                    break
            
            # 计算新的配置下目标函数值
            obj_new = GetObjective(LLC_size[cfg_new], location_new)
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
                location_now = deepcopy(location_new)
                obj_now = obj_new
                update = update + 1
                iter.append(update)
                objfunc.append(obj_new)
                if obj_new < obj_best:
                    obj_best = obj_new
                    cfg_best = cfg_new
                    location_best = deepcopy(location_new)
                    totalImprove = totalImprove + 1


            # 输出内循环结束后的数据
            print("######################### %d Inner Loop Result################################" % totalMar)
            print("Inner loop best LLC size configuration is:", LLC_size[cfg_best])
            print("Inner loop best location is:", location_best)
            print("The value of optimization objective is : ", obj_best)
            print("######################### %d Inner Loop Result################################" % totalMar)

        # 内循环结束，更新温度和外循环次数
        # alpha 代表降温系数
        Tnow = Tnow * alpha            
        kIter =  kIter + 1

    # 退出外层循环，输出最后结果
    print("The final DSE result".center(50, "*"))
    print("Best LLC size is:", LLC_size[cfg_best])
    print("Best location is:", location_best)
    print("The minimum average_packet_latency is:", obj_best)
    print("DSE Finished!".center(50, "*"))

    print("Total iteration is:", iter)
    print("The value of optimal objective set is", objfunc)

     # 将迭代产生的目标函数值可视化
    plt.plot(iter,objfunc)
    plt.xlabel('Iteration')
    plt.ylabel('average_packet_latency')
    plt.savefig("dse.jpg")


def main():
    starttime = datetime.datetime.now()
    Optimization_SA(2000, 60, 0.4, 3)
    endtime = datetime.datetime.now()
    run_time = ((endtime - starttime).seconds) / 60
    print("Total running time: %f minutes" % run_time)



if __name__ == "__main__":
    main()
