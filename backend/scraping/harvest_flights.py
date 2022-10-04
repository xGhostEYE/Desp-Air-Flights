from __future__ import print_function
# from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from pandas import *
import os
from os.path import exists




# remove flights with no flight number
# remove loops in path
# remove cargo flight
# format times



def harvest_data_arrivals(arrival_location):
    url = "https://www.airports-worldwide.info/airport/"+arrival_location+"/arrivals"
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)
    datable_list = []

    for i in range(len(dfs)):
        datable_list.append(dfs[i])

    df = pd.concat(datable_list)
    df = df[df["Status"].isin(["scheduled", "scheduleddelayed"])]
    return df


def harvest_data_departures(departure_location):
    url = "https://www.airports-worldwide.info/search/"+departure_location+"/departures"
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)
    datable_list = []

    for i in range(len(dfs)):
        datable_list.append(dfs[i])

    df = pd.concat(datable_list)
    df = df[df["Status"].isin(["scheduled", "scheduleddelayed"])]
    return df

#currently only removes the second time
def clean_data(file):
    df = pd.read_csv(file)

    for name, values in df[['Departure']].items():
        data = values.str.split()
        for i in range(len(data)):
            # Clean the string
            cleaned_string = str(data[i]).strip("[]'")
            
            # Count the string, and only parse longer results which have the extra data we're looking for
            chrcount = len(cleaned_string)
            if chrcount>9:
                print(cleaned_string[round(chrcount/2):])
    for name, vlaues in df[['Flight']].items():
        print(data)
                

if __name__ == "__main__":
    # file out
    file_output_origin_departures = os.path.abspath("origin_airport_departures.csv")

    #forward scrape
    # get user location
    user_location = "calgary"
    user_airport_timetable_data = harvest_data_departures(user_location)

    user_airport_timetable_data.to_csv(os.path.abspath("connecting_airport_departures.csv"), index=False)

    separator = '('
    departures = user_airport_timetable_data['Destination'].unique().tolist()



    for i in range(5):
        departures[i] = departures[i].split(separator, 1)[0]
        departures[i] = departures[i].rstrip()
        departure = departures[i]

        try:
            ap_dep_df = harvest_data_departures(departure)

            if not exists(file_output_origin_departures):
                ap_dep_df.to_csv(file_output_origin_departures, index=False)
            else:
                ap_dep_df.to_csv(file_output_origin_departures, mode='a', header=False, index=False)
        except Exception as e:
            print(f"skipping url for {departure} do to an exception:",e)
    
    
    #backward scrape
    file_output_arrival=os.path.abspath("origin_airport_departures.csv")
    user_location = "los angeles"
    user_airport_timetable_data = harvest_data_departures(user_location)

    user_airport_timetable_data.to_csv(os.path.abspath("user_arrival.csv"), index=False)

    separator = '('
    departures = user_airport_timetable_data['Origin'].unique().tolist()



    for i in range(5):
        departures[i] = departures[i].split(separator, 1)[0]
        departures[i] = departures[i].rstrip()
        departure = departures[i]

        try:
            ap_dep_df = harvest_data_departures(departure)

            if not exists(file_output_arrival):
                ap_dep_df.to_csv(file_output_arrival, index=False)
            else:
                ap_dep_df.to_csv(file_output_arrival, mode='a', header=False, index=False)
        except Exception as e:
            print(f"skipping url for {departure} do to an exception:",e)
    
    # clean the data for the Traveling salesman algo
    clean_data(os.path.abspath("airport_destination.csv"))
