from __future__ import print_function
from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from pandas import *
import os
from os.path import exists


def harvest_data(departure_location):
    url = "https://www.airports-worldwide.info/search/"+departure_location+"/departures"
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)
    datable_list = []

    for i in range(len(dfs)):
        datable_list.append(dfs[i])

    return pd.concat(datable_list)


if __name__ == "__main__":
    # file out
    file_output="../__data/airport_departure.csv"

    # get user location
    user_location = "calgary"
    user_airport_timetable_data = harvest_data(user_location)

    user_airport_timetable_data.to_csv("../__data/user_departure.csv", index=False)

    separator = '('
    departures = user_airport_timetable_data['Destination'].unique().tolist()

    for i in range(len(departures)):
        departures[i] = departures[i].split(separator, 1)[0]
        departures[i] = departures[i].rstrip()
        departure = departures[i]

        try:
            ap_dep_df = harvest_data(departure)

            if not exists(file_output):
                ap_dep_df.to_csv(file_output, index=False)
            else:
                ap_dep_df.to_csv(file_output, mode='a', header=False, index=False)

        except Exception as e:
            print(f"skipping url for {departure} do to an exception:",e)
    

