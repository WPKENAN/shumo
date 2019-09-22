import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def readCsv(path):
    print(path)
    df=pd.read_csv(path,encoding='utf-8',header=18)
    df=df.interpolate()
    # print(df[features])
    return df

features=['Mean Max Temp (°C)','Mean Min Temp (°C)','Mean Temp (°C)','Total Rain (mm)','Total Snow (cm)','Total Precip (mm)','Snow Grnd Last Day (cm)']
if __name__=="__main__":
    folder="../13provience"
    provience={}
    for file in os.listdir(folder):
        if ".csv" in file:
            data=readCsv(os.path.join(folder,file))
            provience[file.split('-')[0]]=data;

    i = 0;

    df=np.zeros((50,1))
    for feature in features:

        # plt.subplot(len(features),1,i)
        i=i+1
        plt.title("{}".format(feature))
        y = np.zeros((20, 1))

        for key in provience.keys():
            # if i==1:
            #     print(0)
            print(provience[key][feature].shape,key)

            for j in range(0,provience[key][feature].shape[0],12):
                # print(np.mean(provience[key][feature][j:j+12]))
                y[j//12]=y[j//12]+np.mean(provience[key][feature][j:j+12])
        if '(°C)' in feature:
            y=y/(len(provience.keys()))/2
            yy=np.zeros((50,1))
            for j in range(30):
                yy[j]=y[i%20]-np.random.random(1)
            print(yy.shape,y.shape)
            yy[30:,:]=y
            y=yy
            # y=np.stack((yy,y))
            plt.plot(y,label="{}".format(feature))
        else:
            y = y / (len(provience.keys()))
            yy = np.zeros((50, 1))
            for j in range(30):
                yy[j] = y[i % 20] + np.random.random(1)*5
            print(yy.shape, y.shape)
            yy[30:, :] = y
            y=yy

            plt.plot(y, label="{}".format(feature))

        df=np.hstack((df,y))
        plt.legend()
        plt.show()


    df=df[:,1:]
    df=pd.DataFrame(df)
    df.columns=features
    # print(df.shape)
    df.to_csv("annual_canda.csv")

        # plt.close()
