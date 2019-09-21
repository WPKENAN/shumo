import os
import wget
import pandas as pd
import numpy as np
import shutil
import matplotlib.pyplot as plt
import math
'''
for station in `seq 1 10`;
do wget --content-disposition "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=${station}&Year=2008&Month=1&Day=14&timeframe=1&submit= Download+Data" ;
done
'''
def readStation(path):
    data=pd.read_csv(path)

    Station_ID={}
    columns=list(data.columns)


    for i in range(len(data)):
        sampleDict = {}
        for column in columns:
            sampleDict[column]=data[column][i]
        Station_ID[data['Station ID'][i]]=sampleDict

    # while(1):
    #     i=input("das:")
    #     i=int(i)
    #     if i in Station_ID:
    #         print(Station_ID[i])

    return Station_ID

if __name__=="__main__":
    path="./Station Inventory EN.csv"
    Station_ID=readStation(path)

    data=[]
    for key in Station_ID.keys():
        print(key)
        lat,long=Station_ID[key]['Latitude (Decimal Degrees)'],Station_ID[key]['Longitude (Decimal Degrees)']
        data.append([lat,long])

    data=np.array(data)
    plt.scatter(data[:,1],data[:,0])
    plt.show()
