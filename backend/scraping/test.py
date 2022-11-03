from __future__ import print_function
from cmath import nan
# from asyncio.windows_events import NULL
from bs4 import BeautifulSoup as BeautifulSoup
import re
from urllib.request import urlopen
import pandas as pd
from pandas import *
import os
import requests
from os.path import exists



def clean_data(df):
    """
    Purpose:
        cleans the csv files so it's easier for the algo to read it
    Params:
        dataframe: dataframe of flights
    Returns:
        lists of cleaned data
    """
    # for index,item in df['Flight'].items():
    #     item = str(item).replace(" ", "")
    #     if len(item) > 1:
    #         if (str(item[0]).isalpha() and str(item[1]).isalpha() and str(item[2]).isalpha()==False):
    #             continue
    #         else:
    #             df.drop(index,inplace=True)
    cleanedflights_flightnumber = []
    cleanedflights_time = []
    flights = []
    #clean flight number
    for index,item in df['Flight'].items():
        item = str(item).replace(" ", "")
        if len(item) > 1:
            flights.append(str(item)[:6])
        else:
            df.drop(index,inplace=True)
            # if (str(item[0]).isalpha() and str(item[1]).isalpha()):
            #     if (len(item) <= 6):
            #         flights.append(str(item))
            #     else:
            #         # flights.append(str(item)[:len(str(item))-6])
            #         # changed here
            #         for i in range(len(item)):
            #             i+2  
            #             if (str(item[i]).isalpha() and str(item[i+1]).isalpha()):
            #                 flights.append(str(item).rsplit(item[i],1)[0])
            #                 continue
    for i in range(len(flights)):
        if flights[i] == '':
            continue
        elif str(flights[i][len(flights[i])-1:]).isalpha():
            flights[i] = str(flights[i])[:-1]
            cleanedflights_flightnumber.append(flights[i])
        else:
            cleanedflights_flightnumber.append(flights[i])
    
    departure_or_arrival = ""
    if ('Departure' in df):
        departure_or_arrival = 'Departure'
    else:
        departure_or_arrival = 'Arrival'
    destination_or_origin = ""
    if ('Destination' in df):
        destination_or_origin = 'Destination'
    else:
        destination_or_origin = 'Origin'
    #clean time
    time_list = list(df[departure_or_arrival])
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i])
        if (len(time_list[i])>5):
            time_list[i] = time_list[i][-5:]
            cleanedflights_time.append(time_list[i])
        else:
            cleanedflights_time.append(time_list[i])
    df_cleaned = pd.DataFrame (cleanedflights_flightnumber, columns = ['Flight'])
    df_cleaned[departure_or_arrival] = cleanedflights_time
    df[departure_or_arrival] = df_cleaned[departure_or_arrival].values
    df['Flight'] = df_cleaned['Flight'].values
    # seperating airport code and city name
    new = df[destination_or_origin].str.split("(", n = 1, expand = True)
    df["City Name"]= new[0]
    df["Airport Code"] = new[1]
    df["Airport Code"] = df["Airport Code"].str.replace(r')', '')
    df.drop(columns =[destination_or_origin], axis=1,inplace = True)
    # df.drop(df.columns.difference(['a','b']), 1, inplace=True)
    return (df)



def harvest_data_arrivals(arrival_location):
    """
    Purpose:
        scrapes flights arriving to the given airport
    Params:
        arrival_location: airport we are scraping
    Returns:
        dataframe with arriving flights to airport

    """
    url = "https://www.airports-worldwide.info/search/"+arrival_location+"/arrivals"
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    list_of_dataframes = pd.read_html(url.replace(" ","%20"))
    
    # combines dataframes
    df = pd.concat(list_of_dataframes)
    
    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]
    
    #remove unammed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])

    # remove flight loop
    discard = [arrival_location]
    df = df[df["Origin"].str.contains('|'.join(discard))==False]
    
    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]
    data = clean_data(df)
    return data



def harvest_data_departures(departure_location,initial_search):
    """
    Purpose:
        scrapes flights departing from given airport
    Params:
        departure_location: airport we are scraping
    Returns:
        dataframe with departing flights from airport
    
    """

    url = "https://www.airports-worldwide.info/search/"+departure_location+"/departures"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    urls = []
    interval = soup.find_all("nav", {"id": "intervals"})
    data = re.findall(r'(https?://[^\s]+)', str(interval[0]))
    for i in range(len(data)):
        urls.append(data[i].split(">", 1)[0])
    list_of_dataframes = None
    for i in range(len(urls)):
        
        urls[i] = urls[i].encode('ascii', errors='ignore')
        urls[i] = urls[i].decode('ascii', errors='ignore')
        list_of_dataframes = pd.read_html(urls[i].replace(" ","%20"))
    
    # combines dataframes
    df = pd.concat(list_of_dataframes)

    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])
    
    #remove unammed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    #remove flight loop
    discard = [departure_location]
    df = df[df["Destination"].str.contains('|'.join(discard))==False]
    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]
    data = clean_data(df)
    # new_row = {"City Name":"above data from: "+departure_location}
    # #append row to the dataframe
    # data = data.append(new_row, ignore_index=True)
    return data

#currently only removes the second time



                

if __name__ == "__main__":

    # file out
    # forward scrape
    # get user location
    initial_search = True
    user_location = "calgary"
    # need user requested destination
    user_requested_destination = "los angeles"
    user_airport_timetable_data = harvest_data_departures(user_location,initial_search)
    user_airport_timetable_data.to_csv(os.path.abspath("origin_airport_departures.csv"), index=False)
    separator = '('
    departures = user_airport_timetable_data['City Name'].unique().tolist()
    
    file_output_origin_departures = os.path.abspath("connections_to_destination.csv")
    initial_search = False
    for i in range(len(departures)):
        departures[i] = departures[i].split(separator, 1)[0]
        departures[i] = departures[i].rstrip()
        departure = departures[i]
        try:
            ap_dep_df = harvest_data_departures(departure,initial_search)
            if not exists(file_output_origin_departures):
                ap_dep_df.to_csv(file_output_origin_departures, index=False)
            else:
                ap_dep_df.to_csv(file_output_origin_departures, mode='a', header=False, index=False)
        except Exception as e:
            print(f"skipping url for {departure} do to an exception:",e)

    

        


    # #backward scrape
    # user_requested_destination = "los angeles"
    # user_requested_airport_departures = harvest_data_arrivals(user_requested_destination)
    
    # user_requested_airport_departures.to_csv(os.path.abspath("destination_airport_arrivals.csv"), index=False)
    # separator = '('
    # departures = user_requested_airport_departures['City Name'].unique().tolist()
    # file_output_arrival=os.path.abspath("connections_from_destination.csv")
    # # replace 5 with len(departures)
    # for i in range(len(departures)):
    #     departures[i] = departures[i].split(separator, 1)[0]
    #     departures[i] = departures[i].rstrip()
    #     departure = departures[i]
    #     try:
    #         ap_dep_df = harvest_data_departures(departure,user_requested_destination)
    #         if not exists(file_output_arrival):
    #             ap_dep_df.to_csv(file_output_arrival, index=False)
    #         else:
    #             ap_dep_df.to_csv(file_output_arrival, mode='a', header=False, index=False)
    #     except Exception as e:
    #         print(f"skipping url for {departure} do to an exception:",e)
