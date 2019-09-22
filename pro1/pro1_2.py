import numpy as np
import pandas as pd
import os
import wget
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns  # 用于绘制热图的工具包
from scipy.cluster import hierarchy  # 用于进行层次聚类，话层次聚类图的工具包
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, inconsistent
from scipy import cluster
import matplotlib.pyplot as plt
from sklearn import decomposition as skldec  # 用于主成分分析降维的包

start = 1910
end = start+30
features=['Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)','Total Rain (mm)','Total Snow (cm)','Total Precip (mm)']
def readCsv(path):
    # print(path)

    data = pd.read_csv(path, header=22)
    # print(data[['Date/Time','Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)','Total Rain (mm)','Total Snow (cm)','Total Precip (mm)','Snow on Grnd (cm)']])
    # return data[['Date/Time','Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)','Total Rain (mm)','Total Snow (cm)','Total Precip (mm)','Snow on Grnd (cm)']]
    try:
        data=data[features]
    except:
        lines = open(path,encoding='utf-8').readlines();
        for i in range(len(lines)):
            if "Date/Time" in lines[i]:
                break;
        # print(i)
        data = pd.read_csv(path, header=i-2)
        # print(data)
        data = data[features]
        # print(data)
        # dsa
    return data



# return


def getStationId(folder, start, end):
    count = 0
    Station_IDs = []
    for Station_ID in os.listdir(folder):
        years = []
        for year in os.listdir(os.path.join(folder, Station_ID)):
            year = year.strip('.csv').split('_')[1]
            try:
                years.append(int(year))
            except:
                continue
        if start in years and end in years:
            count += 1
            Station_IDs.append(int(Station_ID))
            # print(Station_ID)
    return Station_IDs


def getLat_Long(path):
    # print(path)
    lines = open(path, encoding='utf-8').readlines()
    Lat = -999
    Long = -999
    for i in range(len(lines)):
        line = lines[i].replace('"', '')
        if line.strip('\n').split(',')[0] == 'Latitude':
            Lat = float(line.strip('\n').split(',')[1])
        elif line.strip('\n').split(',')[0] == 'Longitude':
            Long = float(line.strip('\n').split(',')[1])
        if Lat != -999 and Long != -999:
            break;

    if Lat == 0 or Long == 0:
        print(path)
    # print(Lat,Long)
    return [Lat, Long]


def clearData(Station_IDs, start, end, folder):
    dicData={}
    for i in range(len(Station_IDs)):
        for j in range(start, end):
            if j == start:
                tmp1 = readCsv(os.path.join(folder, str(Station_IDs[i]), "{}_{}.csv".format(Station_IDs[i], start)))

            else:
                tmp2 = readCsv(os.path.join(folder, str(Station_IDs[i]), "{}_{}.csv".format(Station_IDs[i], j)))
                tmp1 = pd.concat([tmp1, tmp2], axis=0)

        tmp1=tmp1.dropna(axis=1,how="all",inplace=False)
        if tmp1.shape[1] !=len(features):
            continue
        dicData[Station_IDs[i]]=tmp1
    return dicData


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



def hc(df, Lat_Longs):
    from pylab import mpl
    from scipy.spatial import distance

    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    print(df)
    # df=(df - df.min()) / (df.max() - df.min())

    disMat=df.values
    # disMat = distance.pdist(df.values, 'euclidean')
    # print("disMat", disMat.shape)
    # print(df)
    # print(df.shape)
    Z = hierarchy.linkage(disMat, method='ward')
    # print(Z.shape)

    # print(Z)
    plt.figure(figsize=(30, 20))
    hierarchy.dendrogram(Z, labels=df.index)
    plt.xticks(rotation=90)
    plt.title("{}-{} 层次聚类树状图".format(start,end))
    plt.savefig("{}_{}层次聚类树状图.png".format(start,end), dpi=240)
    plt.close()

    plt.figure(figsize=(30, 20))
    sns.clustermap(df, method='ward', metric='euclidean')
    plt.xticks(rotation=90)
    plt.title("{}-{} 层次聚类热力图".format(start,end))
    plt.savefig("{}_{}层次聚类热力图.png".format(start,end), dpi=240)
    plt.close()

    cur_clusters = fcluster(Z, 6, criterion='maxclust')
    print(len(Lat_Longs))
    print(len(cur_clusters))

    print(cur_clusters)
    plt.scatter(Lat_Longs[:, 0], Lat_Longs[:, 1], c=cur_clusters)
    plt.savefig('{}-{}聚类结果经纬图-6类.png'.format(start,end))
    # plt.show()
    plt.close()

    tmp = np.zeros((Lat_Longs.shape[0], 3))
    tmp[:, 0:2], tmp[:, 2], = Lat_Longs, cur_clusters
    tmp = pd.DataFrame(tmp)
    tmp.to_csv("{}_{}聚类结果.csv".format(start,end), sep=',', index=False, header=False)



if __name__ == "__main__":
    for i in range(1929,2019,30):

        start = i
        end = start+30
        # folder="D:\github\Data\shumo\data\data\\day"
        folder = "D:\github\Data\shumo\data\\day"

        Station_IDs = getStationId(folder, start, end)
        Station_IDs.sort()
        print(len(Station_IDs))
        # print(Station_IDs)

        dicData = clearData(Station_IDs, start, end, folder)
        Station_IDs = list(dicData.keys());
        Station_IDs.sort()
        # print(len(Station_IDs))
        # print(Station_IDs)

        Lat_Longs = []
        for id in Station_IDs:
            print(id)
            csvlist = os.listdir(os.path.join(folder, str(id)));
            if len(csvlist) > 0 and ".tmp" not in csvlist[0]:
                if id == '1590':
                    continue
                Lat_Longs.append(getLat_Long(os.path.join(folder, str(id), "{}".format(csvlist[0]))))
        Lat_Longs = np.array(Lat_Longs)

        dis = np.zeros((len(Station_IDs), len(Station_IDs)))
        for i in range(len(Station_IDs)):
            for j in range(i, len(Station_IDs)):
                print(i, j)
                df1 = dicData[Station_IDs[i]]
                df2 = dicData[Station_IDs[j]]

                f = 0
                stds = 0;
                for k in range(len(features)):
                    count = pd.concat([df1[df1.columns[k]], df2[df2.columns[k]]], axis=1)
                    count.dropna(axis=0, how='any', inplace=True)
                    count = count.values
                    if len(count) == 0:
                        std = 0
                    else:
                        std = np.sqrt(np.sum((count[:, 0] - count[:, 1]) ** 2) / len(count))
                        stds += std
                        f += 1
                if f==0:
                    dis[i, j] = dis[j, i] = 999
                else:
                    dis[i, j] = dis[j, i] = stds / f

        dis = pd.DataFrame(dis)
        dis.columns = Station_IDs;
        dis.index = Station_IDs
        dis = dis.fillna(value=0, method=None, axis=None, inplace=False, limit=None, downcast=None)
        dis.to_csv("{}_{}_经纬度-类别.csv".format(start, end), sep=',', index=False, header=False)

        print("start hc")
        # hc(newdata, Lat_Longs)
        # newdata = my(dis, Lat_Longs)
        hc(dis, Lat_Longs)






