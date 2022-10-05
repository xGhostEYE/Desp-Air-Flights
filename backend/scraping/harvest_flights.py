"""
Purpose:
    harvests fights departing and arriving from airports
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
from os.path import exists


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
    url = url.encode('ascii', errors='ignore')
    url = url.decode('ascii', errors='ignore')
    dfs = pd.read_html(url.replace(" ","%20"), header=0)

    # combines dataframes
    df = pd.concat(dfs)

    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

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

    return df


def clean_data(file):
    #currently only removes the second time


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
    
    # scrape departures from airport
    # airport flights depart from
    departure_airport = "calgary"

    # file out
    departures_file_out = f"./backend/__data/{departure_airport}_airport_departures.csv"

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
    arrival_file_out = f"./backend/__data/{arrival_airport}_airport_arrivals.csv"
    
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
    
    # # clean the data for the Traveling salesman algo
    # clean_data(os.path.abspath("airport_destination.csv"))
