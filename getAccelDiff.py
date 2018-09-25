import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def getFirstgoodrow(tb, height, groundheight):
    for index, row in df.iterrows():
        if row["ASL"] < height + groundheight + 500 and row["ASL"] > height + groundheight - 500:
            return index
    return tb.head(1).index[0]


def getFirstAccel():
    for index, row in df.iterrows():
        if row['Acceleration'] > 5:
            return index
    return df.head(1).index[0]


df = pd.read_csv("C:\\Users\\diego\\PycharmProjects\\KSPDataIA\\Data\\accel.csv")
df.set_index("Time", inplace=True)
# selectedHeight = input("What height will you fall from?")
selectedHeight = 10000
terrainHeight = df.iloc[-1]["ASL"]
print(terrainHeight)
df = df[getFirstgoodrow(df, float(selectedHeight), terrainHeight):]

f = lambda x: x - df.head(1).index[0]
df.index = df.index.map(f)
# df = df[df.TrueHeight != -1]
print(df.tail(1)["ASL"])
h = lambda x: x - df.ASL.iloc[-1]
df["TrueHeight"] = df.ASL.map(h)

plt.rcParams['axes.grid'] = True

df['Acceleration'] = df["GForce"]
f2 = lambda x: x * 9.81
df.Acceleration = df.Acceleration.map(f2)

acceldf = df["Acceleration"]
# [df.index<110][df.index>4]
acceldf = acceldf[acceldf.index<110]
acceldf = acceldf[acceldf.index>18]
grad = acceldf.diff()/acceldf.index.to_series().diff()
grad = grad.dropna()
plt.scatter(grad.index, grad, c='g', label="Raw data", s=8)
jerkpolyfit = np.polyfit(grad.index, grad, 2)
plt.plot(range(121), np.poly1d(jerkpolyfit)(np.unique(range(121))), c='r',zorder=10,label="Line of best fit")
plt.title("The derivative of Acceleration: Jerk")
plt.ylabel("Jerk (m * s^-3)")
plt.show()
print(jerkpolyfit)

secondder = grad.diff()/grad.index.to_series().diff()
plt.scatter(secondder.index, secondder, c='g', label="Raw data", s=8, zorder=10)
jouncepolyfit=np.polyfit(secondder.index, secondder, 2)
plt.plot(range(121), np.poly1d(jouncepolyfit)(range(121)), c='r', label="Line of best fit")
plt.title("The derivative of Jerk: Jounce")
plt.ylabel("Jounce (m * s^-4)")
plt.legend(loc='best')
plt.show()
print(secondder.mean())

