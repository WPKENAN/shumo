import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy

def readCsv(path):
    df=pd.read_csv(path,header=None)
    values=df.values
    pre=copy.deepcopy(values[::-1])
    pre=pre[0:90]
    np.random.shuffle(pre)
    data=np.vstack((pre[0:90]-np.random.random(1)*5,values))
    np.random.shuffle(pre)
    data = np.vstack((pre[0:90]-np.random.random(1)*5, data))
    np.random.shuffle(pre)
    data = np.vstack((pre[0:62] - np.random.random(1) * 5, data))
    print(data.shape)

    df=pd.DataFrame(data)
    df.to_csv("./data/google.csv")
    # plt.plot(data)
    # plt.show()

    # print(df)
if __name__=="__main__":
    path="google_pre.csv"
    readCsv(path)