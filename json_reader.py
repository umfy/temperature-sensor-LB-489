import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime
import requests

sampling = 300
if __name__ == "__main__":
    while True:
        connection = True
        try:
            web = requests.get('http://172.30.92.190/json')
        except:
            print("CONNECTION FAILED")
            connection = False

        if connection == True:
            df = pd.read_json(web)
            df = json_normalize(df['input'])
            df = df.T
            df.columns = df.loc['name']
            df = df[4:]

            now = datetime.now()
            czas = str(now.date()) + "-" + str(now.time().hour) + "-" + str(now.time().minute)

            df.insert(loc=0, column='time', value=czas)
            df.to_csv('data.csv', sep=';')

