import numpy as np
import pandas as pd
import os
import wget
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns  #用于绘制热图的工具包
from scipy.cluster import hierarchy  #用于进行层次聚类，话层次聚类图的工具包
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster,inconsistent
from scipy import cluster
import matplotlib.pyplot as plt
from sklearn import decomposition as skldec #用于主成分分析降维的包

start=1910
end=1930


def readCsv(path):
    data=pd.read_csv(path,header=22)
    # print(data[['Date/Time','Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)','Total Rain (mm)','Total Snow (cm)','Total Precip (mm)','Snow on Grnd (cm)']])
    # return data[['Date/Time','Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)','Total Rain (mm)','Total Snow (cm)','Total Precip (mm)','Snow on Grnd (cm)']]
    return data[['Mean Temp (°C)']]
    # return

def getStationId(folder,start,end):
    count=0
    Station_IDs=[]
    for Station_ID in os.listdir(folder):
        years=[]
        for year in os.listdir(os.path.join(folder,Station_ID)):
            year=year.strip('.csv').split('_')[1]
            try:
                years.append(int(year))
            except:
                continue
        if start in years and end in years:
            count+=1
            Station_IDs.append(int(Station_ID))
            # print(Station_ID)
    return Station_IDs

def getLat_Long(path):
    # print(path)
    lines=open(path,encoding='utf-8').readlines()
    Lat = -999
    Long = -999
    for i in range(len(lines)):
        line=lines[i].replace('"','')
        if line.strip('\n').split(',')[0]=='Latitude':
            Lat=float(line.strip('\n').split(',')[1])
        elif line.strip('\n').split(',')[0]=='Longitude':
            Long=float(line.strip('\n').split(',')[1])
        if Lat!=-999 and Long!=-999:
            break;

    if Lat==0 or Long==0:
        print(path)
    # print(Lat,Long)
    return [Lat,Long]

def clearData(Station_IDs,start,end,folder):
    for i in range(len(Station_IDs)):
        for j in range(start,end):
            if i == 0 and j==start:
                data=readCsv(os.path.join(folder, str(Station_IDs[i]), "{}_{}.csv".format(Station_IDs[i], j)))
                # newColumns=[]
                # for c in data.columns:
                #     newColumns.append("_"+str(Station_IDs[i]) + "_" + c)
                # data.columns=newColumns
                data.columns = [str(Station_IDs[i])]

                continue
            if i==0 and j!=start:
                tmp = readCsv(os.path.join(folder, str(Station_IDs[i]), "{}_{}.csv".format(Station_IDs[i], j)))

                # newColumns = []
                # for c in tmp.columns:
                #     newColumns.append("_"+str(Station_IDs[i]) + "_" + c)
                # tmp.columns = newColumns
                tmp.columns = [str(Station_IDs[i])]

                data = pd.concat([data, tmp], axis=0)
                continue

            if j==start:
                tmp1 = readCsv(os.path.join(folder, str(Station_IDs[i]), "{}_{}.csv".format(Station_IDs[i], start)))
                # newColumns = []
                # for c in tmp1.columns:
                #     newColumns.append("_"+str(Station_IDs[i]) + "_" + c)
                # tmp1.columns = newColumns
                tmp1.columns = [str(Station_IDs[i])]

            else:
                tmp2=readCsv(os.path.join(folder,str(Station_IDs[i]),"{}_{}.csv".format(Station_IDs[i],j)))

                # newColumns = []
                # for c in tmp2.columns:
                #     newColumns.append("_"+str(Station_IDs[i]) + "_" + c)
                tmp2.columns = [str(Station_IDs[i])]

                tmp1=pd.concat([tmp1,tmp2],axis=0)

        if i!=0:
            # print(data.shape,tmp1.shape)
            data=pd.concat([data,tmp1],axis=1)

    print(data.shape)
    newData=data;
    newData = newData.dropna(axis=1, how='all', inplace=False)

    # newData = data.fillna(value=999, method=None, axis=None, inplace=False, limit=None, downcast=None)
    # print(newData)
    print(newData.shape)


    # print(newData)
    # newData = (newData - newData.min()) / (newData.max() - newData.min())
    return newData
    # return data
def lat_long2csv(folder):
    Lat_Longs = []
    for file in os.listdir(folder):
        csvlist = os.listdir(os.path.join(folder, file));
        if len(csvlist) > 0 and ".tmp" not in csvlist[0]:
            if file == '1590':
                continue
            Lat_Longs.append(getLat_Long(os.path.join(folder, str(file), "{}".format(csvlist[0]))))
    df = pd.DataFrame(Lat_Longs)
    df.to_csv("Lat_Long.csv", sep=',', index=False, header=False)
    print(Lat_Longs)
    Lat_Longs = np.array(Lat_Longs)
    # plt.scatter(Lat_Longs[:, 1], Lat_Longs[:, 0])
    # plt.show()
    return Lat_Longs


def bestCOCLUSTER(df):
    df=df.T
    # from scipy.cluster.hierarchy import distance
    from scipy.spatial import distance
    linkmethod = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']
    paraDF = pd.DataFrame(columns=['method', 'CCC'], index=linkmethod)
    paraDF.loc[:, 'method'] = linkmethod

    for iter_m in linkmethod:
        Y = distance.pdist(np.asarray(df))
        print(Y.shape)
        Z = hierarchy.linkage(Y, method=iter_m)

        c, coph_dists = hierarchy.cophenet(Z, Y)
        paraDF.loc[iter_m, 'CCC'] = c
    paraDF.sort_values(by='CCC', ascending=False, inplace=True)
    # print(paraDF)
    row_linkage = hierarchy.linkage(distance.pdist(np.asarray(df)), method=paraDF.iloc[0, 0])
    col_linkage = hierarchy.linkage(distance.pdist(np.asarray(df).T), method=paraDF.iloc[0, 0])

    # print(paraDF.iloc[0,0])
    sns.clustermap(df, row_linkage=row_linkage, col_linkage=col_linkage,figsize=(13, 13))
    plt.show()
    return hierarchy.linkage(distance.pdist(np.asarray(df)))

def hc(df,Lat_Longs):
    from pylab import mpl
    from scipy.spatial import distance

    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    print(df)
    # df=(df - df.min()) / (df.max() - df.min())


    disMat = distance.pdist(df.values, 'euclidean')
    print("disMat",disMat.shape)
    # print(df)
    # print(df.shape)
    Z = hierarchy.linkage(disMat, method='ward')
    # print(Z.shape)

    # print(Z)
    plt.figure(figsize=(30, 20))
    hierarchy.dendrogram(Z, labels=df.index)
    plt.title("层次聚类树状图")
    plt.savefig("层次聚类树状图.jpg",dpi=240)
    plt.close()


    plt.figure(figsize=(30, 20))
    sns.clustermap(df, method='ward', metric='euclidean')
    plt.title("层次聚类热力图")
    plt.savefig("层次聚类热力图.jpg",dpi=240)
    plt.close()


    cur_clusters = fcluster(Z, 6, criterion='maxclust')
    print(len(Lat_Longs))
    print(len(cur_clusters))

    print(cur_clusters)
    plt.scatter(Lat_Longs[:,0],Lat_Longs[:,1],c=cur_clusters)
    plt.savefig('聚类结果经纬图-20类.png')
    # plt.show()
    plt.close()



    tmp=np.zeros((Lat_Longs.shape[0],3))
    tmp[:,0:2],tmp[:,2],=Lat_Longs,cur_clusters
    tmp=pd.DataFrame(tmp)
    tmp.to_csv("聚类结果.csv",sep=',', index=False, header=False)

def my(df,Lat_Longs):
    print(df)
    dis=np.zeros((df.shape[1],df.shape[1]))

    # print(df.columns[0])
    # da
    for i in range(len(df.columns)):
        for j in range(i,len(df.columns)):
            print(i,j)
            # count=[]
            count=pd.concat([df[df.columns[i]],df[df.columns[j]]],axis=1)
            count.dropna(axis=0, how='any', inplace=True)
            # print(count.shape)
            count=count.values
            # std=tmp[]

    #         for k in range(df.shape[0]):
    #
    #             if df[i][k]!=999 and df[j][k]!=999:
    #                 count.append([df[i][k],df[j][k]])
    #         # print(len(count))
    #         count=np.array(count)
            std=0
            std=np.sqrt(np.sum((count[:,0]-count[:,1])**2)/len(count))
    #         # print(std)
            dis[i,j]=std
            dis[j, i] = std
    print(dis)

    dis=pd.DataFrame(dis)
    dis.columns=df.columns;
    dis.index=df.columns
    dis = dis.fillna(value=0, method=None, axis=None, inplace=False, limit=None, downcast=None)
    dis.to_csv("tmp.csv",sep=',', index=False, header=False)
    return dis


if __name__=="__main__":
    # key=5406
    # year=2019
    # url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={}&Year={}&Month=1&Day=14&timeframe=2&submit=Download+Data" \
    #     .format(key, year)
    # print(url)
    # wget.download(url, out=os.path.join("./", "{}.csv".format(year)))

    # folder="D:\github\Data\shumo\data\data\\day"
    folder = "D:\github\Data\shumo\data\\day"


    Station_IDs=getStationId(folder,start,end)
    Station_IDs.sort()
    print(len(Station_IDs))
    print(Station_IDs)


    newdata=clearData(Station_IDs,start,end,folder)

    # Lat_Longs=lat_long2csv(folder)
    import copy
    tmp=copy.deepcopy(Station_IDs)
    for id in Station_IDs:
        flag_=1
        for c in newdata.columns:
            if id == int(c):
                flag_=0
                break;
        if flag_:
            tmp.remove(id)

    Station_IDs=copy.deepcopy(tmp)
    print(Station_IDs)
    # for i in range(92):
    #     print(Station_IDs[i],newdata.columns[i])
    Lat_Longs=[]
    for id in Station_IDs:
        print(id)
        csvlist = os.listdir(os.path.join(folder, str(id)));
        if len(csvlist) > 0 and ".tmp" not in csvlist[0]:
            if id == '1590':
                continue
            Lat_Longs.append(getLat_Long(os.path.join(folder, str(id), "{}".format(csvlist[0]))))

    # df = pd.DataFrame(Lat_Longs)
    # df.to_csv("Lat_Long.csv", sep=',', index=False, header=False)

    print(Lat_Longs)
    # ewq
    Lat_Longs = np.array(Lat_Longs)


    # plt.scatter(Lat_Longs[:, 1], Lat_Longs[:, 0])
    # plt.show()


    print("start hc")
    # hc(newdata, Lat_Longs)
    newdata=my(newdata,Lat_Longs)
    hc(newdata, Lat_Longs)

    exit(0)
    print(newdata)
    newdata=pd.DataFrame(Lat_Longs)
    newdata.index=Station_IDs

    hc(newdata,Lat_Longs)
    # bestCOCLUSTER(newdata)



    # print(data.shape)


    # print(data.columns)
    # print(data['Min Temp (°C)'])




