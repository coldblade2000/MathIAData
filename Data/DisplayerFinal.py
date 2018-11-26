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


df1, MAE305 = processdataframe(1,2,305)
df2, MAE345 = processdataframe(2,2,345)
df3, MAE385 = processdataframe(3,2,385)


plt.figure(4,figsize=(12,5))
ax = df3["Acceleration"].plot(c='b', label="385s")
df2["Acceleration"].plot(ax=ax,c='g', label="345s")
df1["Acceleration"].plot(ax=ax,c='r', label="305s")

# df1p=[1.16123576E-03,4.42308838E-02,1.59352397E+01]
# df2p=[9.19947933E-04,3.75746408E-02,1.59825879E+01]
# df3p=[7.44978699E-04,3.29195488E-02,1.60075232E+01]

x = np.arange(130)

plottingmode = 0
if plottingmode == 0:
    ax.plot(x,60000/(-((60000/9.81)/305)*x+3840), c='#FFC0CB')
    ax.plot(x,60000/(-((60000/9.81)/345)*x+3840), c='#00FF00')
    ax.plot(x,60000/(-((60000/9.81)/385)*x+3840), c='c')
elif plottingmode == 1:  # exponential
    ax.plot(x,coefficient*(x*BaseISP/305)**2+15.63, c='#FFC0CB')
    ax.plot(x,coefficient*(x*BaseISP/345)**2+15.63, c='#00FF00')
    ax.plot(x,coefficient*(x*BaseISP/385)**2+15.63, c='c')
# ax.plot(x, df1p[0]*x**2+df1p[1]*x+df1p[2],c='#FFC0CB')
# ax.plot(x, df2p[0]*x**2+df2p[1]*x+df2p[2], c='#00FF00')
# ax.plot(x, df3p[0]*x**2+df3p[1]*x+df3p[2], c='c')
plt.title("The acceleration of a rocket over time based upon its specific impulse (Isp)")
plt.ylabel("Aceleration (m/s/s)", color='m')
textstr = '\n'.join((
    r'$\mathrm{305s: }=%.2f$' % (median, ),
    r'$\mathrm{345s: }=%.2f$' % (median, ),
    r'$\mathrm{385s: }=%.2f$' % (median, ),
    ))
plt.xlabel("Time (seconds)")
plt.grid(True)
plt.xlim(0,130)
plt.ylim(15,35)
plt.legend()
plt.show()
df1 = df1["Acceleration"].loc[0.26:99.4]
df2 = df2["Acceleration"].loc[0.26:112.4]
df3 = df3["Acceleration"].loc[0.28:125.58]
print("305s : " + str(np.polyfit(df1.index, df1, 2)))
print("345s : " + str(np.polyfit(df2.index, df2, 2)))
print("385s : " + str(np.polyfit(df3.index, df3, 2)))