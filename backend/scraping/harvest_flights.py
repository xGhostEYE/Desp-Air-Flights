
"""
Purpose:
    harvests fights departing and arriving from airports
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from os.path import exists
import requests
import re
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
import pandas as pd
from datetime import date
import time


def price_scrape(origin, destination, startdate, requests):
    
    global results
    df = pd.DataFrame()

    url = "https://www.kayak.com/flights/" + origin + "-" + destination + "/" + startdate + "?sort=bestflight_a&fs=stops=0"
    print("\n" + url)

    chrome_options = webdriver.ChromeOptions()
    agents = ["Firefox/66.0.3","Chrome/73.0.3683.68","Edge/16.16299"]
    print("User agent: " + agents[(requests%len(agents))])
    chrome_options.add_argument('--user-agent=' + agents[(requests%len(agents))] + '"')    
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    driver.implicitly_wait(20)
    driver.get(url)

    #Check if Kayak thinks that we're a bot
    time.sleep(5) 
    soup=BeautifulSoup(driver.page_source, 'lxml')

    if soup.find_all('p')[0].getText() == "Please confirm that you are a real KAYAK user.":
        print("Kayak thinks I'm a bot, which I am ... so let's wait a bit and try again")
        driver.close()
        time.sleep(20)
        return "failure"

    time.sleep(20) #wait 20sec for the page to load
    
    soup=BeautifulSoup(driver.page_source, 'lxml')
    
    #get the arrival and departure times
    deptimes = soup.find_all('span', attrs={'class': 'depart-time base-time'})
    arrtimes = soup.find_all('span', attrs={'class': 'arrival-time base-time'})
    meridies = soup.find_all('span', attrs={'class': 'time-meridiem meridiem'})
    airline = soup.find_all('div', attrs={'class': 'bottom'})
    booking = soup.find_all('a', attrs={'class': 'booking-link'})
    deptime = []
    for div in deptimes:
        deptime.append(div.getText()[:-1])    
        
    arrtime = []
    for div in arrtimes:
        arrtime.append(div.getText()[:-1])   

    meridiem = []
    for div in meridies:
        meridiem.append(div.getText())  
    airlines = []
    for div in airline:
        airlines.append(div.getText())
    booking_list = []    
    for div in booking:
        booking_list.append(div.getText())
    booking_clean = []
    for i in range(len(booking_list)):
        m = re.search('[0-9.]+', booking_list[i])
        if m:
            booking_clean.append(m.group())
        else:
            continue
    listthing_clean = []
    airlines_clean = []
    for i in range(len(airlines)):
        listthing_clean.append(("\n".join(item for item in airlines[i].split('\n') if item)))
    for i in range(len(listthing_clean)):
        if len(listthing_clean[i]) > 3 and "\n" not in listthing_clean[i]:
            airlines_clean.append(listthing_clean[i])

    df['Departure'] = deptime
    df['Arrival'] = arrtime
    df['Carrier'] = airlines_clean
    df['Cost'] = booking_clean
    return df

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
    for i in range(len(flights)):
        if flights[i] == '':
            continue
        elif str(flights[i][len(flights[i])-1:]).isalpha():
            flights[i] = str(flights[i])[:-1]
            cleanedflights_flightnumber.append(flights[i])
        else:
            cleanedflights_flightnumber.append(flights[i])
            
    #determine if the DB is from departure or arrival
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
    url = "https://www.airports-worldwide.info/airport/"+arrival_location+"/arrivals"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    list_of_dataframes = []
    # get the different times on the site
    interval = soup.find_all("nav", {"id": "intervals"})
    # if there is no times on the site then scrape once, else scrape all the times
    if (len(interval)<=0):
        url = url.encode('ascii', errors='ignore')
        url = url.decode('ascii', errors='ignore')
        dataframes = pd.read_html(url.replace(" ","%20"))
        for i in range(len(dataframes)):
            list_of_dataframes.append(dataframes[i])
    else:
        data = re.findall(r'(https?://[^\s]+)', str(interval[0]))
        for i in range(len(data)):
            urls.append(data[i].split(">", 1)[0])

        for i in range(len(urls)):
            
            urls[i] = urls[i].encode('ascii', errors='ignore')
            urls[i] = urls[i].decode('ascii', errors='ignore')
            dataframes = pd.read_html(urls[i].replace(" ","%20"))
            for i in range(len(dataframes)):
                list_of_dataframes.append(dataframes[i])
    
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

    url = "https://www.airports-worldwide.info/airport/"+departure_location+"/departures"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    list_of_dataframes = []
    
    # get the different times on the site
    interval = soup.find_all("nav", {"id": "intervals"})
    
    # if there is no times on the site then scrape once, else scrape all the times
    if (len(interval)<=0):
        url = url.encode('ascii', errors='ignore')
        url = url.decode('ascii', errors='ignore')
        dataframes = pd.read_html(url.replace(" ","%20"))
        for i in range(len(dataframes)):
            list_of_dataframes.append(dataframes[i])
    else:
        data = re.findall(r'(https?://[^\s]+)', str(interval[0]))
        for i in range(len(data)):
            urls.append(data[i].split(">", 1)[0])

        for i in range(len(urls)):
            
            urls[i] = urls[i].encode('ascii', errors='ignore')
            urls[i] = urls[i].decode('ascii', errors='ignore')
            dataframes = pd.read_html(urls[i].replace(" ","%20"))
            for i in range(len(dataframes)):
                list_of_dataframes.append(dataframes[i])
    
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
    
    # clean the scrapped data
    data = clean_data(df)

    return data


if __name__ == "__main__":
    
    # scrape departures from airport
    # airport flights depart from
    departure_airport = "calgary"
    initial_search = True
    # file out
    departures_file_out = f"./__data/{departure_airport}_airport_departures.csv"

    # scrape airport departures
    airport_dept_df = harvest_data_departures(departure_airport, initial_search)
    initial_search = False
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

    #scrape for prices from the departing airport
    prices_file_out = f"./__data/{departure_airport}_flight prices.csv"
    prices_df = price_scrape(departure_airport, arrival_airport, str(date.today()), 0)
    prices_df.to_csv(prices_file_out, index=False)
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
    


