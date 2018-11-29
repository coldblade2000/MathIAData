import pandas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

coefficient = 16.72/(112.5**2)
BaseISP = 345

def getFirstAccel(xdf):
    for index, row in xdf.iterrows():
        if row['Acceleration'] > 5:
            return index
    return xdf.head(1).index[0]
prefix = "C:\\Users\\diego\\PycharmProjects\\MathIAData\\Data\\"

def processdataframe(xinvar, xtrial, isp):
    xdf = pd.read_csv(
        prefix + "acceleration" + str(xinvar) + "-" + str(xtrial) + ".csv")
    xdf.set_index("Time", inplace=True)
    xdf['Acceleration'] = xdf["GForce"]
    f2 = lambda x: x * 9.81
    xdf.Acceleration = xdf.Acceleration.map(f2)
    xdf = xdf[getFirstAccel(xdf):]
    f = lambda x: x - xdf.head(1).index[0]
    xdf.index = xdf.index.map(f)

    xdf["PredictedAccel"] = xdf.index
    # j = lambda x: (x*(BaseISP/isp))**2*coefficient+15.63
    j = lambda x: 60000/(-((60000/9.81)/isp)*x+3840)
    xdf["PredictedAccel"] = xdf.PredictedAccel.map(j)
    count = 0
    sum = 0
    for index, row in xdf.iterrows():
        if index > 5 and not (index > 90 and row["Acceleration"]<20):
            sum += abs(row["Acceleration"]-row["PredictedAccel"])
            count += 1
    plt.rcParams['axes.grid'] = True
    MAE = sum/count
    print(F"The Mean Absolute error for an ISP of {isp} is {MAE}")
    return xdf, MAE


for xinvar in range(1,4):
    for xtrial in range(1,4):
        inputDF = pd.read_csv(prefix + "acceleration" + str(xinvar) + "-" + str(xtrial) + ".csv")

        inputDF.set_index("Time", inplace=True)
        inputDF['Acceleration'] = inputDF["GForce"]
        f2 = lambda x: x * 9.81
        inputDF.Acceleration = inputDF.Acceleration.map(f2)
        inputDF = inputDF[getFirstAccel(inputDF):]
        f = lambda x: x - inputDF.head(1).index[0]
        inputDF.index = inputDF.index.map(f)

        outputDF = inputDF[['Time', 'Acceleration']].copy()
        outputDF.to_csv(prefix+"\\ProcessedData\\")
df1, MAE305 = processdataframe(1,2,305)
df2, MAE345 = processdataframe(2,2,345)
df3, MAE385 = processdataframe(3,2,385)