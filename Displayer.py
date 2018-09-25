import pandas as pd
import matplotlib.pyplot as plt

def getFirstgoodrow(tb, height, groundheight):
    for index, row in df.iterrows():
        if row["ASL"] < height+ groundheight+500 and row["ASL"] > height + groundheight-500:
            return index
    return tb.head(1).index[0]
def getFirstAccel ():
    for index, row in df.iterrows():
        if row['Acceleration'] > 5:
            return index
    return df.head(1).index[0]

df = pd.read_csv("C:\\Users\\diego\\PycharmProjects\\KSPDataIA\\Data\\accel.csv")
df.set_index("Time", inplace=True)
selectedHeight = input("What height will you fall from?")
terrainHeight = df.iloc[-1]["ASL"]
print(terrainHeight)
df = df[getFirstgoodrow(df, float(selectedHeight), terrainHeight):]

f = lambda x: x-df.head(1).index[0]
df.index = df.index.map(f)
# df = df[df.TrueHeight != -1]
print(df.tail(1)["ASL"])
h = lambda x: x - df.ASL.iloc[-1]
df["TrueHeight"] = df.ASL.map(h)

plt.rcParams['axes.grid'] = True

df['Acceleration'] = df["GForce"]
f2 = lambda x: x*9.81
df.Acceleration = df.Acceleration.map(f2)


fig, axes = plt.subplots(nrows=3, ncols=1)
fig.set_size_inches(5,15, forward=True)

df['Acceleration'].plot(ax=axes[0])
axes[0].set_title("Acceleration")
axes[0].set_ylabel("Acceleration (m/s/s)")
plt.grid(True)

df['TrueHeight'].plot(ax=axes[1])
axes[1].set_title("True Height")
plt.grid(True)
axes[1].set_ylabel("Height (meters)")

df['VerticalSpeed'].plot(ax=axes[2])
axes[2].set_title("Vertical Velocity")
axes[2].set_ylabel("Vertical Velocity (m/s)")

# df["GForce"].plot()
# df.VerticalSpeed.plot(secondary_y=True, style="g")
# df["VerticalSpeed"].plot()
plt.show()

plt.figure(2, figsize=(12,5))
plt.xlabel("Time")
ax1 = df['TrueHeight'].loc[getFirstAccel():].plot(color='green', grid=True, label='Height')
ax2 = df['VerticalSpeed'].loc[getFirstAccel():].plot(color='blue', grid=True,secondary_y=True, label='Vertical Speed')
# ax3 = df['Acceleration'].loc[getFirstAccel():].plot(color='red', grid=True, label='Acceleration')
ax1.legend(loc='best')
ax1.set_ylabel("Height (meters)", color='g')
ax2.set_ylabel("Vertical Velocity (m/s)", color='b')
ax2.legend(loc='best')
# ax3.legend(loc=3)
plt.grid(True)
plt.title("Vertical speed and Height when suicide burn is started")
plt.show()


