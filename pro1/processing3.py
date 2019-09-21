import os
import wget
import pandas as pd
import numpy as np
import shutil
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

    return Station_ID

if __name__=="__main__":
    targetFolder="D:\github\Data\shumo\data\\year"
    Station_ID=readStation("./Station Inventory EN.csv")

    for key in Station_ID.keys():
        if not os.path.exists(os.path.join(targetFolder,str(key))):
            os.mkdir(os.path.join(targetFolder,str(key)))

        # First_Year=1900
        # Last_Year=2019
        First_Year = Station_ID[key]['MLY First Year']
        Last_Year = Station_ID[key]['MLY Last Year']

        # print(First_Year)
        print(key,First_Year,Last_Year,math.isnan(First_Year))
        if math.isnan(First_Year) or math.isnan(Last_Year):
            continue
        for year in range(int(Last_Year+1)-2,int(Last_Year+1)):
            if os.path.exists(os.path.join(targetFolder,str(key),"{}_{}.csv".format(key,year))):
                continue
            url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={}&Year={}&Month=1&Day=14&timeframe=3&submit=Download+Data"\
                .format(key,year)
            print(url)
            wget.download(url, out=os.path.join(targetFolder,str(key),"{}_{}.csv".format(key,year)))






