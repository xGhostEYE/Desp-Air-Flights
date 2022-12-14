import os
from bs4 import BeautifulSoup
import pandas as pd
from os.path import exists
import requests
import re
import random
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import date, datetime
import time
from os.path import exists

def price_link_scrape(origin, destination, startdate):

    df = pd.DataFrame()

    url = "https://www.kayak.com/flights/" + origin + "-" + destination + "/" + startdate + "?sort=depart_a&fs=stops=0"

    chrome_options = webdriver.ChromeOptions()
    agents = ["Firefox/66.0.3","Chrome/73.0.3683.68","Edge/16.16299"]
    print("User agent: " + agents[(0%len(agents))])
    chrome_options.add_argument('--user-agent=' + agents[(0%len(agents))] + '"')
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
    data = soup.find_all('div', attrs={'class': 'inner-grid keel-grid'})
    urls = []
    for link in soup.find_all('a', href=True):
        urls.append(link['href'])
    data_seperated = []
    for div in data:
        data_seperated.append(str(div.getText().replace("\n",'')))
    departure_time = []
    arrival_time = []
    airlines = []
    prices = []
    for i in range(len(data_seperated)):
        booking_info = data_seperated[i].split('$')[0]
        time_departure = booking_info.split('???')[0]
        time_departure = time_departure.replace(' ','')
        in_time = datetime.strptime(time_departure, "%I:%M%p")
        out_time = datetime.strftime(in_time, "%H:%M")
        departure_time.append(out_time)
        time_arrival = booking_info.split(' ')[1]
        time_arrival_remaining = booking_info.split(' ')[2]
        timething = time_arrival[3:]+time_arrival_remaining[:2]
        in_time = datetime.strptime(timething, "%I:%M%p")
        out_time = datetime.strftime(in_time, "%H:%M")
        arrival_time.append(out_time)
        price = data_seperated[i].split('$')[1]
        price = price.split(' ')[0]
        prices.append('$'+price)
        airline = booking_info.split('nonstop')[0]
        airline_remaining = airline.split(":", 2)[2]
        airlines.append(airline_remaining[5:])

    urls = soup.select(".above-button")

    urls_clean = []
    urls_clean_no_duplicates = []
    final_urls = []
    final_urls = []
    urls_clean = urls[::2]
    urls_clean_no_duplicates = []
    for i in range(len(urls_clean)):
        for link in urls_clean[i].findAll('a'):
            urls_clean_no_duplicates.append("https://www.kayak.com"+link.get('href'))

    for i in range(len(urls_clean_no_duplicates)):
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(urls_clean_no_duplicates[i])
        driver.implicitly_wait(10)
        time.sleep(random.randint(3,8))
        final_urls.append(driver.current_url)

        
    df['Departure'] = departure_time
    df['Arrival'] = arrival_time
    df['Carrier'] = airlines
    df['Cost'] = prices
    df['Link'] = final_urls
    return df

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
    url = "https://www.airports-worldwide.info/airport/"+arrival_location+"/arrivals"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    list_of_dataframes = []
    interval = soup.find_all("nav", {"id": "intervals"})
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
    
    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]
    data = clean_data(df)
    new_row = {"City":"above data from: "+arrival_location}
    #append row to the dataframe
    data = data.append(new_row, ignore_index=True)
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
    interval = soup.find_all("nav", {"id": "intervals"})
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
    #remove cargo flights
    # discard = ["cargo"]
    # df = df[df["Carrier"].str.contains('|'.join(discard))==False]
    data = clean_data(df)
    new_row = {"City":"above data from: "+departure_location}
    #append row to the dataframe
    data = data.append(new_row, ignore_index=True)
    return data



# def harvest_prices(df){
#     return df
# }
                

if __name__ == "__main__":

    # file out
    # forward scrape
    # get user location
    initial_search = True
    user_location = "YYC"
    # need user requested destination
    user_airport_timetable_data = harvest_data_departures(user_location,initial_search)
    user_airport_timetable_data.to_csv(os.path.abspath("origin_airport_departures.csv"), index=False)
    separator = '('
    departures = user_airport_timetable_data['Airport Code'].unique().tolist()
    
    file_output_origin_departures = os.path.abspath("connections_to_destination.csv")
    initial_search = False
    for i in range(len(departures)):
        time.sleep(1)
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
            print(f"skipping url for {departure} at time do to an exception:",e)
            print("line:",i)

    

        


    #backward scrape
    user_requested_destination = "YVR"
    user_requested_airport_departures = harvest_data_arrivals(user_requested_destination)
    
    user_requested_airport_departures.to_csv(os.path.abspath("destination_airport_arrivals.csv"), index=False)
    separator = '('
    departures = user_requested_airport_departures['Airport Code'].unique().tolist()
    file_output_arrival=os.path.abspath("connections_from_destination.csv")
    # replace 5 with len(departures)
    for i in range(len(departures)):
        departures[i] = departures[i].split(separator, 1)[0]
        departures[i] = departures[i].rstrip()
        departure = departures[i]
        try:
            ap_dep_df = harvest_data_departures(departure,user_requested_destination)
            if not exists(file_output_arrival):
                ap_dep_df.to_csv(file_output_arrival, index=False)
            else:
                ap_dep_df.to_csv(file_output_arrival, mode='a', header=False, index=False)
        except Exception as e:
            print(f"skipping url for {departure} do to an exception:",e)