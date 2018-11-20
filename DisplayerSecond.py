import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getFirstgoodrow(xdf,tb, height, groundheight):
    for index, row in xdf.iterrows():
        if row["ASL"] < height+ groundheight+500 and row["ASL"] > height + groundheight-500:
            return index
    return tb.head(1).index[0]
def getFirstAccel(xdf):
    for index, row in xdf.iterrows():
        if row['Acceleration'] > 5:
            return index
    return xdf.head(1).index[0]
prefix = "C:\\Users\\diego\\PycharmProjects\\KSPDataIA\\Data\\"


def processdataframe(xinvar, xtrial):
    xdf = pd.read_csv(
        "C:\\Users\\diego\\PycharmProjects\\KSPDataIA\\Data\\acceleration" + str(xinvar) + "-" + str(xtrial) + ".csv")
    xdf.set_index("Time", inplace=True)
    # selectedHeight = input("What height will you fall from?")
    terrainHeight = xdf.iloc[0]["ASL"]
    print(terrainHeight, "m = terrain height")
    xdf['Acceleration'] = xdf["GForce"]
    f2 = lambda x: x * 9.81
    xdf.Acceleration = xdf.Acceleration.map(f2)
    xdf = xdf[getFirstAccel(xdf):]
    f = lambda x: x - xdf.head(1).index[0]
    xdf.index = xdf.index.map(f)
    # xdf = xdf[xdf.TrueHeight != -1]
    print(xdf.tail(1)["ASL"])
    h = lambda x: x - xdf.ASL.iloc[0]
    xdf["TrueHeight"] = xdf.ASL.map(h)

    plt.rcParams['axes.grid'] = True

    return xdf
invar = 1
trial = 3
isp = lambda: 265+(40*invar)
df = processdataframe(invar,trial)
# df = pd.read_csv("C:\\Users\\diego\\PycharmProjects\\KSPDataIA\\Data\\acceleration"+str(invar)+"-"+str(trial)+".csv")
# df.set_index("Time", inplace=True)
# # selectedHeight = input("What height will you fall from?")
# terrainHeight = df.iloc[0]["ASL"]
# print(terrainHeight, "m = terrain height")
# df['Acceleration'] = df["GForce"]
# f2 = lambda x: x*9.81
# df.Acceleration = df.Acceleration.map(f2)
# df = df[getFirstAccel():]
# f = lambda x: x-df.head(1).index[0]
# df.index = df.index.map(f)
# # df = df[df.TrueHeight != -1]
# print(df.tail(1)["ASL"])
# h = lambda x: x - df.ASL.iloc[0]
# df["TrueHeight"] = df.ASL.map(h)

plt.rcParams['axes.grid'] = True


fig, axes = plt.subplots(nrows=1, ncols=3)
fig.set_size_inches(15,5, forward=True)

df['Acceleration'].plot(ax=axes[0])
axes[0].set_xlim(0,130)
axes[0].set_ylim(0,35)
axes[0].set_title("Acceleration")
axes[0].set_ylabel("Acceleration (m/s/s)")
plt.grid(True)

df['TrueHeight'].plot(ax=axes[1])
axes[1].set_xlim(0,130)
axes[1].set_ylim(0,160000)
axes[1].set_title("True Height")
plt.grid(True)
axes[1].set_ylabel("Height (meters)")

df['VerticalSpeed'].plot(ax=axes[2])
axes[2].set_xlim(0,130)
axes[2].set_ylim(0,3000)
axes[2].set_title("Vertical Velocity")
axes[2].set_ylabel("Vertical Velocity (m/s)")

# df["GForce"].plot()
# df.VerticalSpeed.plot(secondary_y=True, style="g")
# df["VerticalSpeed"].plot()

# plt.show()
plt.tight_layout()
print(prefix+"Plots\\"+str(isp())+"\\t"+str(trial)+"\\g1.png")
plt.savefig(prefix+"Plots\\"+str(isp())+"\\t"+str(trial)+"\\g1.png", bbox_inches='tight')






plt.figure(2, figsize=(12,5))
plt.xlabel("Time(seconds)")
ax1 = df['Acceleration'].loc[getFirstAccel(df):].plot(color='green', grid=True, label='Acceleration')
# ax1 = plt.scatter(df['Acceleration'].loc[getFirstAccel():].index,df['Acceleration'].loc[getFirstAccel():],color='green', grid=True, label='Acceleration')
ax2 = df['VerticalSpeed'].loc[getFirstAccel(df):].plot(color='blue', grid=True,secondary_y=True, label='Vertical Speed')
# ax2 = plt.scatter(df['VerticalSpeed'].loc[getFirstAccel():],color='blue', grid=True,secondary_y=True, label='Vertical Speed')
# ax3 = df['Acceleration'].loc[getFirstAccel():].plot(color='red', grid=True, label='Acceleration')
ax1.legend(loc='upper center')
ax1.set_ylim(0,35)
ax1.set_ylabel("Aceleration (m/s/s)", color='g')
ax2.set_ylabel("Vertical Velocity (m/s)", color='b')
ax2.set_ylim(0,3000)
ax2.legend(loc='lower center')
# ax3.legend(loc=3)
plt.grid(True)
plt.xlim(0,130)
# plt.legend(bbox_to_anchor=(0, 1),
#            bbox_transform=plt.gcf().transFigure)
plt.title("Vertical speed and Acceleration when rocket is started over time")
# plt.show()
plt.savefig(prefix+"Plots\\"+str(isp())+"\\t"+str(trial)+"\\g2.png", bbox_inches='tight')

plt.figure(3, figsize=(12,5))
plt.xlabel("Time (seconds)")
# ax1 = df['Acceleration'].loc[getFirstAccel():].plot(color='green', grid=True, label='Acceleration')
ax1 = plt.scatter(df['Acceleration'].loc[getFirstAccel(df):].index,df['Acceleration'].loc[getFirstAccel(df):],color='green', label='Acceleration',s=4)
# ax2 = df['VerticalSpeed'].loc[getFirstAccel():].plot(color='blue', grid=True,secondary_y=True, label='Vertical Speed')
# ax2 = plt.scatter(df['VerticalSpeed'].loc[getFirstAccel():],color='blue', grid=True,secondary_y=True, label='Vertical Speed')
# ax3 = df['Acceleration'].loc[getFirstAccel():].plot(color='red', grid=True, label='Acceleration')
plt.legend(loc='upper center')
plt.ylabel("Aceleration (m/s/s)", color='g')
# ax2.set_ylabel("Vertical Velocity (m/s)", color='b')
# ax2.legend(loc='lower center')
# ax3.legend(loc=3)
plt.grid(True)
plt.xlim(0,130)
plt.ylim(0,35)

# plt.legend(bbox_to_anchor=(0, 1),
#            bbox_transform=plt.gcf().transFigure)
plt.title("Acceleration when rocket is started over time (Scatter Plot)")
# plt.show()
plt.savefig(prefix+"Plots\\"+str(isp())+"\\t"+str(trial)+"\\g3.png", bbox_inches='tight')
plt.clf()

df1=processdataframe(1,2)
df2=processdataframe(2,2)
df3=processdataframe(3,2)

plt.figure(4,figsize=(12,5))
ax = df3["Acceleration"].plot(c='b', label="385s")
df2["Acceleration"].plot(ax=ax,c='g', label="345s")
df1["Acceleration"].plot(ax=ax,c='r', label="305s")

df1p=[1.16123576E-03,4.42308838E-02,1.59352397E+01]
df2p=[9.19947933E-04,3.75746408E-02,1.59825879E+01]
df3p=[7.44978699E-04,3.29195488E-02,1.60075232E+01]
coefficient = 16.72/(112.5**2)
BaseISP = 345
x = np.arange(130)
ax.plot(x,coefficient*(x*BaseISP/345)+15.63)
# ax.plot(x, df1p[0]*x**2+df1p[1]*x+df1p[2],c='#FFC0CB')
# ax.plot(x, df2p[0]*x**2+df2p[1]*x+df2p[2], c='#00FF00')
# ax.plot(x, df3p[0]*x**2+df3p[1]*x+df3p[2], c='c')
plt.title("The acceleration of a rocket over time based upon its specific impulse (Isp)")
plt.ylabel("Aceleration (m/s/s)", color='m')
plt.xlabel("Time (seconds)")
plt.grid(True)
plt.xlim(0,130)
plt.ylim(0,35)
plt.legend()
plt.show()
df1 = df1["Acceleration"].loc[0.26:99.4]
df2 = df2["Acceleration"].loc[0.26:112.4]
df3 = df3["Acceleration"].loc[0.28:125.58]
print("305s : " + str(np.polyfit(df1.index, df1, 2)))
print("345s : " + str(np.polyfit(df2.index, df2, 2)))
print("385s : " + str(np.polyfit(df3.index, df3, 2)))
# df1["Acceleration"].to_csv(prefix+"305s.csv")
# df2["Acceleration"].to_csv(prefix+"345s.csv")
# df3["Acceleration"].to_csv(prefix+"385s.csv")
#
# plt.figure(2, figsize=(12,5))
# plt.xlabel("Time")
# ax1 = df['TrueHeight'].loc[getFirstAccel():].plot(color='green', grid=True, label='Height')
# ax2 = df['VerticalSpeed'].loc[getFirstAccel():].plot(color='blue', grid=True,secondary_y=True, label='Vertical Speed')
# # ax3 = df['Acceleration'].loc[getFirstAccel():].plot(color='red', grid=True, label='Acceleration')
# ax1.legend(loc='best')
# ax1.set_ylabel("Height (meters)", color='g')
# ax2.set_ylabel("Vertical Velocity (m/s)", color='b')
# ax2.legend(loc='best')
# # ax3.legend(loc=3)
# plt.grid(True)
# plt.title("Vertical speed and Height when suicide burn is started")
# plt.show()


