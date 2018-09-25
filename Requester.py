import requests
import json
import pandas as pd
import time as Time


def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)

print("Starting in -1")
defaultdict = [{'ASL': 2636.4994024340413, 'VerticalSpeed': 0.00018107751869411715, 'GForce': 0.161729381354316, 'TrueHeight': 3.812524, 'Time': 3651.740000065016}]

df = pd.DataFrame(defaultdict)
df.set_index('Time', inplace=True)
for x in range(0,5):
    print("Starting in ",5-x)
    Time.sleep(1)

try:
    while True:  # 30 NBA Teams
        base_url = "http://127.0.0.1:8085/telemachus/datalink?"
        team_url = base_url + "ASL=v.altitude&VerticalSpeed=v.verticalSpeed&GForce=v.geeForce&TrueHeight=v.heightFromTerrain&Time=v.missionTime"
        data = get_data(team_url)
        print(data)
        time = data.pop("Time")
        df.loc[time] = data
        # df = df.append(data)
        # print(df.loc[time])
        Time.sleep(0.01)
except KeyboardInterrupt:
    df.drop([3651.740000065016],inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    invar = 1
    trial = 1
    df.to_csv("C:\\Users\\diego\\PycharmProjects\\KSPDataIA\\Data\\acceleration"+str(invar)+"-"+str(trial)+".csv")
    exit()



