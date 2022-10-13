<<<<<<< HEAD
from __future__ import print_function
from asyncio.windows_events import NULL
# from asyncio.windows_events import NULL
=======
"""
Purpose:
    harvests fights departing and arriving from airports
"""

>>>>>>> backend
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
from os.path import exists


<<<<<<< HEAD



# format times

def clean_data(df):
    cleanedflights_flightnumber = []
    cleanedflights_time = []
    flights = []

    #remove second time
    for name, values in df[['Departure']].items():
        data = values.str.split()
        for i in range(len(data)):
            cleaned_string = str(data[i]).strip("[]'")
            cleanedflights_time.append(cleaned_string)
    
    #clean flight number
    for item in df['Flight'].unique():
        item = str(item).replace(" ", "")
        if len(item) > 1:
            if (str(item[0]).isalpha() and str(item[1]).isalpha()):
                if (len(item) < 7):
                    flights.append(str(item))
                else:
                    for i in range(len(item)):
                        i+2  
                        if (str(item[i]).isalpha() and str(item[i+1]).isalpha()):
                            flights.append(str(item).rsplit(item[i],1)[0])
                            continue
    for i in range(len(flights)):
        if flights[i] == '' or len(flights[i])>7:
            continue
        else:
            cleanedflights_flightnumber.append(flights[i])
    return (cleanedflights_flightnumber, cleanedflights_time)

def harvest_data_arrivals(arrival_location):
    url = "https://www.airports-worldwide.info/search/"+arrival_location+"/arrivals"
=======
# remove flights with no flight number
# remove cargo flight
# format times

def harvest_data_departures(departure_location):
    """
    Purpose:
        scrapes flights departing from given airport
    Params:
        departure_location: airport we are scraping
    Returns:
        dataframe with departing flights from airport
    
    """
    url = "https://www.airports-worldwide.info/search/"+departure_location+"/departures"
>>>>>>> backend
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)

<<<<<<< HEAD
    for i in range(len(dfs)):
        datable_list.append(dfs[i])
    print(datable_list)
    df = pd.concat(datable_list)
    df = df[df["Status"].isin(["scheduled", "scheduleddelayed"])]
    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])
    #remove flight loop
    discard = [arrival_location]
    df = df[df["Origin"].str.contains('|'.join(discard))==False]
    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]
    
=======
    # combines dataframes
    df = pd.concat(dfs)

    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

>>>>>>> backend
    return df


def harvest_data_arrivals(arrival_location):
    """
    Purpose:
        scrapes flights arriving to the given airport
    Params:
        arrival_location: airport we are scraping
    Returns:
        dataframe with arriving flights to airport

    """

    "*** error with url, airport code may work ***"
    url = "https://www.airports-worldwide.info/airport/"+arrival_location+"/arrivals"
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)

    # combines dataframes
    df = pd.concat(dfs)

    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

<<<<<<< HEAD
    df = pd.concat(datable_list)
    df = df[df["Status"].isin(["scheduled", "scheduleddelayed"])]
    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])
    #remove flight loop
    discard = [departure_location]
    df = df[df["Destination"].str.contains('|'.join(discard))==False]
    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]
    
    return df

=======
    return df


def clean_data(file):
    #currently only removes the second time


    df = pd.read_csv(file)
>>>>>>> backend

                

if __name__ == "__main__":
    
    # scrape departures from airport
    # airport flights depart from
    departure_airport = "calgary"

    # file out
<<<<<<< HEAD
    
=======
    departures_file_out = f"./backend/__data/{departure_airport}_airport_departures.csv"
>>>>>>> backend

    # scrape airport departures
    airport_dept_df = harvest_data_departures(departure_airport)

<<<<<<< HEAD
    user_airport_timetable_data.to_csv(os.path.abspath("origin_airport_departures.csv"), index=False)
=======
    # save airport departures to csv
    airport_dept_df.to_csv(departures_file_out, index=False)
>>>>>>> backend



<<<<<<< HEAD
    file_output_origin_departures = os.path.abspath("connecting_airport_departures.csv")
    for i in range(5):
        departures[i] = departures[i].split(separator, 1)[0]
        departures[i] = departures[i].rstrip()
        departure = departures[i]
=======
    # separator = '('
    # departure_airports = airport_dept_df['Destination'].unique().tolist()

    # for i in range(5):
    #     departure_airports[i] = departure_airports[i].split(separator, 1)[0]
    #     departure_airports[i] = departure_airports[i].rstrip()
    #     departure_airport = departure_airports[i]
>>>>>>> backend

    #     try:
    #         ap_dep_df = harvest_data_departures(departure)

    #         if not exists(file_output_origin_departures):
    #             ap_dep_df.to_csv(file_output_origin_departures, index=False)
    #         else:
    #             ap_dep_df.to_csv(file_output_origin_departures, mode='a', header=False, index=False)
    #     except Exception as e:
    #         print(f"skipping url for {departure} do to an exception:",e)
    
<<<<<<< HEAD
    #backward scrape
    file_output_arrival=os.path.abspath("origin_airport_departures.csv")
    user_requested_destination = "los angeles"
    user_requested_airport_departures = harvest_data_arrivals(user_requested_destination)

    user_requested_airport_departures.to_csv(os.path.abspath("user_arrival.csv"), index=False)

    separator = '('
    departures = user_requested_airport_departures['Origin'].unique().tolist()
=======

    # scrape arrivals to airport
    # airport flights arrive to
    arrival_airport = "Saskatoon"

    # file out
    arrival_file_out = f"./backend/__data/{arrival_airport}_airport_arrivals.csv"
    
    # scrape airport arrivals
    airport_arvl_df = harvest_data_arrivals(arrival_airport)

    # save airport arrivals to csv
    airport_arvl_df.to_csv(arrival_file_out, index=False)
>>>>>>> backend


    # separator = '('
    # departures = user_airport_timetable_data['Origin'].unique().tolist()

    # for i in range(5):
    #     departures[i] = departures[i].split(separator, 1)[0]
    #     departures[i] = departures[i].rstrip()
    #     departure = departures[i]

<<<<<<< HEAD
        try:
            ap_dep_df = harvest_data_arrivals(departure)
=======
    #     try:
    #         ap_dep_df = harvest_data_departures(departure)
>>>>>>> backend

    #         if not exists(file_output_arrival):
    #             ap_dep_df.to_csv(file_output_arrival, index=False)
    #         else:
    #             ap_dep_df.to_csv(file_output_arrival, mode='a', header=False, index=False)
    #     except Exception as e:
    #         print(f"skipping url for {departure} do to an exception:",e)
    
<<<<<<< HEAD
=======
    # # clean the data for the Traveling salesman algo
    # clean_data(os.path.abspath("airport_destination.csv"))
>>>>>>> backend
