from __future__ import print_function
from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from pandas import *
import os
from os.path import exists
from time import sleep



def harvest_data(departure_location,file_output):
    url = "https://www.airports-worldwide.info/search/"+departure_location+"/departures"
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)
    datable_list = []

    for i in range(len(dfs)):
        datable_list.append(dfs[i])

    #check if file is empty
    if not exists(file_output):
        pd.concat(datable_list, ignore_index=True).to_csv(file_output)
    else:
        pd.concat(datable_list, ignore_index=True).to_csv(file_output, mode='a', header=False)

                

#get user location
user_location = "calgary"
harvest_data(user_location,"C:/Users/melvi/Documents/Coding/practice/user_location_airport_timetable.csv")
user_airport_timetable_data = read_csv("C:/Users/melvi/Documents/Coding/practice/user_location_airport_timetable.csv")


separator = '('
departures = user_airport_timetable_data['Destination'].tolist()


#remove duplicates with set
departures = list(set(departures))
for i in range(len(departures)):
    departures[i] = departures[i].split(separator,1)[0]
    departures[i] = departures[i].rstrip()
    print(departures[i])
    #sleep(0.1)
    try:
        harvest_data(departures[i],"C:/Users/melvi/Documents/Coding/practice/departures.csv")
    except Exception as e:
        print("skipping url do to an exception",e)
    

