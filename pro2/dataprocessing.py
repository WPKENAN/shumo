import os
import shutil
import pandas as pd
import numpy as np


def readTxt(path):

    lines=open(path).readlines()
    data=[]
    for line in lines:
        if line.startswith('#'):
            continue
        line=line.strip()
        # print(line)
        # data.append(line.split())
        a_float_m = map(float, line.split())
        data.append(list(a_float_m))
    # print(data)

    # print(df)
    # print(df.shape)
    return np.array(data)



if __name__=="__main__":
    path="./data/co2_mm_mlo.txt"
    data=readTxt(path)

    month=data[304:-3,[0]]+0.01*data[304:-3,[1]]
    print(month)
    co2=data[304:-3,[4]]
    print(co2.shape)

    path = "./data/ch4_mm_gl.txt"
    data = readTxt(path)
    ch4 = data[:, [3]]
    print(ch4.shape)


    data=np.hstack([co2,ch4])
    data=np.hstack([month,data])
    print(data.shape)

    df=pd.DataFrame(data)
    df.columns=['Date','CO2','CH4']
    df.to_csv("data.csv",sep=',',index=None)

    from sklearn.preprocessing import LabelEncoder


