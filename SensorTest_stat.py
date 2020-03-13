import requests
import re
import csv
import time
from datetime import datetime
import pandas as pd

sampling = 300
if __name__ == "__main__":
    while True:
        connection = True
        try:
            #r = requests.get('http://192.168.10.1/json')
            pd.read_json('json.json')
        except:
            print("CONNECTION FAILED")
            connection = False
            

        if connection == True:
            plik = open('Temp_data_3.csv', 'a')
            czytnik = csv.writer(plik)
            
            now = datetime.now()
            temperatura = re.findall('(\d+.\d+)\s&deg;C', str(r.text))
            temperatura.reverse()

            czas = str(now.date()) + "-" + str(now.time().hour) + "-" + str(now.time().minute)

            temperatura.append(czas)
            temperatura.reverse()
            
            czytnik.writerow(temperatura)
            print(temperatura)
            plik.close()
        else:
            print("Attempting to reconnect: http://192.168.10.1...")
            
        time.sleep(sampling)
