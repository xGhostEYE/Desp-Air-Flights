
"""
Purpose:
    harvests fights departing and arriving from airports
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from pandas import *
import os
from os.path import exists


# format times
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
    
    departure_or_origin = ""
    if ('Departure' in df):
        departure_or_origin = 'Departure'
    else:
        departure_or_origin = 'Origin'
    #clean time
    time_list = list(df[departure_or_origin])
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i])
        if (len(time_list[i])>5):
            time_list[i] = time_list[i][-5:]
            cleanedflights_time.append(time_list[i])
        else:
            cleanedflights_time.append(time_list[i])
    df_cleaned = pd.DataFrame (cleanedflights_flightnumber, columns = ['Flight'])
    df_cleaned[departure_or_origin] = cleanedflights_time
    df[departure_or_origin] = df_cleaned[departure_or_origin].values
    df['Flight'] = df_cleaned['Flight'].values

    return (df)



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

    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)
    
    # combines dataframes
    df = pd.concat(dfs)

    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])

    #remove flight loop
    # discard = [arrival_location]
    # df = df[df["Origin"].str.contains('|'.join(discard))==False]

    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]

    # return df
    data = clean_data(df)
    return data


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
    dfs = pd.read_html(url.replace(" ","%20"), header=0)
    
    # combines dataframes
    df = pd.concat(dfs)
    
    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

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

if __name__ == "__main__":
    
    # scrape departures from airport
    # airport flights depart from
    departure_airport = "calgary"

    # file out
    departures_file_out = f"./__data/{departure_airport}_airport_departures.csv"

    # scrape airport departures
    airport_dept_df = harvest_data_departures(departure_airport)

    # save airport departures to csv
    airport_dept_df.to_csv(departures_file_out, index=False)


    # separator = '('
    # departure_airports = airport_dept_df['Destination'].unique().tolist()

    # for i in range(5):
    #     departure_airports[i] = departure_airports[i].split(separator, 1)[0]
    #     departure_airports[i] = departure_airports[i].rstrip()
    #     departure_airport = departure_airports[i]

    #     try:
    #         ap_dep_df = harvest_data_departures(departure)
    
    #         if not exists(file_output_origin_departures):
    #             ap_dep_df.to_csv(file_output_origin_departures, index=False)
    #         else:
    #             ap_dep_df.to_csv(file_output_origin_departures, mode='a', header=False, index=False)
    #     except Exception as e:
    #         print(f"skipping url for {departure} do to an exception:",e)
    
    # scrape arrivals to airport
    # airport flights arrive to
    arrival_airport = "Saskatoon"

    # file out
    arrival_file_out = f"./__data/{arrival_airport}_airport_arrivals.csv"
    
    # scrape airport arrivals
    airport_arvl_df = harvest_data_arrivals(arrival_airport)

    # save airport arrivals to csv
    airport_arvl_df.to_csv(arrival_file_out, index=False)


    # separator = '('
    # departures = user_airport_timetable_data['Origin'].unique().tolist()

    # for i in range(5):
    #     departures[i] = departures[i].split(separator, 1)[0]
    #     departures[i] = departures[i].rstrip()
    #     departure = departures[i]

    #     try:
    #         ap_dep_df = harvest_data_departures(departure)

    #         if not exists(file_output_arrival):
    #             ap_dep_df.to_csv(file_output_arrival, index=False)
    #         else:
    #             ap_dep_df.to_csv(file_output_arrival, mode='a', header=False, index=False)
    #     except Exception as e:
    #         print(f"skipping url for {departure} do to an exception:",e)
    


