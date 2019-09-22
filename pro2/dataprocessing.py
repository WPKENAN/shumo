import os
import shutil
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
import copy
def readTxt(path):

    lines=open(path).readlines()
    # print(lines)
    data=[]
    for line in lines:
        if line.startswith('#') or line.startswith("%"):
            continue
        line=line.strip()
        # print(line)
        # data.append(line.split())
        if len(line.split())==0:
            continue
        a_float_m = map(float, line.split())
        data.append(list(a_float_m))
    # print(data)

    # print(df)
    # print(df.shape)
    return np.array(data)

def readPaifang():
    m={}
    for i in range(12):
        path="SUMMARY{:02}.MONTHLY.MASS.DAT.txt".format(i+1)
        path=os.path.join(".\data",path)
        # print(path)
        lines = open(path).readlines()
        # print(lines)
        data = []
        lines=lines[5:]
        for line in lines:
            if line.startswith('#') or line.startswith("%"):
                continue
            line = line.strip()
            # print(line)
            # data.append(line.split())
            if len(line.split()) == 0:
                continue
            a_float_m = map(float, line.split())
            data.append(list(a_float_m))

        m[i+1]=copy.deepcopy(data)
        # print(len(data))
    keys=list(m.keys())
    keys.sort()
    print(keys)
    # print(m)

    data=np.zeros((2013-1950+1,12))
    for i in range(1950,2013+1):
        for j in range(12):
            # print(m[j+1][0][0])
            # print(data[i-1950,j])
            data[i-1950,j]=m[j+1][i-1950][3]
    # print(data)

    data=data.reshape(data.shape[0]*data.shape[1],1)
    # print(data[:24])
    # plt.figure()
    # plt.plot(data)
    # plt.show()
    # plt.close()
    return pd.DataFrame(data[:431])

if __name__=="__main__":
    path="./data/co2_mm_mlo.txt"
    data=readTxt(path)

    month=data[304:-3,[0]]+0.01*data[304:-3,[1]]


    # print(month)
    co2=data[304:-3,[4]]
    co2=pd.DataFrame(co2)
    print(co2.shape)

    path = "./data/ch4_mm_gl.txt"
    data = readTxt(path)
    ch4 = data[:, [3]]
    ch4 = pd.DataFrame(ch4)
    print(ch4.shape)

    path = "./data/Complete_TMAX_complete.txt"
    data = readTxt(path)
    TMAX = data[1602:-1, 2]
    TMAX=pd.DataFrame(TMAX)
    # print(TMAX)
    # print(TMAX.shape)

    path = "./data/Complete_TAVG_complete.txt"
    data = readTxt(path)
    TAVG = data[2802:-3, 2]
    TAVG = pd.DataFrame(TAVG)
    # print(TAVG)
    # print(TAVG.shape)

    path = "./data/Complete_TMIN_complete.txt"
    data = readTxt(path)
    TMIN = data[1602:-1, 2]
    # print(TMIN)
    TMIN = pd.DataFrame(TMIN)

    path = "./data/Land_and_Ocean_complete.txt"
    data = readTxt(path)
    TOCEAN = data[1602:-3,2]
    TOCEAN=pd.DataFrame(TOCEAN)
    print(TAVG.values.shape)

    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 4))
    plt.plot(TOCEAN,label='陆地和海洋平均')
    plt.plot((TOCEAN.values-0.29*TAVG.values)/0.69,label='海洋温度')
    plt.plot(TAVG,label='陆地温度')

    # print(TOCEAN)
    plt.legend()
    plt.title("1983.7-2019.5陆地海洋温度变化图")
    plt.ylabel("°C")
    plt.xlabel("time")
    plt.savefig("1983.7-2019.5 land_ocean.png", dpi=200)

    # plt.show()

    print(TOCEAN.shape)

    path = "./data/google.csv"
    google = pd.read_csv(path,header=None)
    # plt.plot(google.values)
    # plt.show()
    # print(google)
    # print(google.shape)
    # google = pd.DataFrame(google)
    # print(TAVG.values.shape)

    FOSSIL_FUEL = readPaifang()

    data=pd.concat([co2,ch4,TMAX,TAVG,TMIN,TOCEAN,FOSSIL_FUEL,google],axis=1)
    data=data.values
    print(data.shape)

    data=np.hstack([month,data])
    print(data.shape)



    df=pd.DataFrame(data)
    df.columns=['Date','CO2','CH4','TMAX','TAVG','TMIN','TOCEAN','FOSSIL_FUEL','ATTENTATION']
    df.to_csv("data.csv",sep=',',index=None)

    from sklearn.preprocessing import LabelEncoder


