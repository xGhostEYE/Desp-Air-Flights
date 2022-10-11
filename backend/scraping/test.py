#currently only removes the second time
from __future__ import print_function
from cgi import print_exception
# from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
from urllib.request import urlopen
from numpy import NaN
import pandas as pd
import os
from os.path import exists



def clean_data(file):
    cleanedflights = []
    flights = []
    df = pd.read_csv(file, encoding='utf8')
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
            cleanedflights.append(flights[i])

    print(cleanedflights)
clean_data(r"C:\Users\melvi\OneDrive\Usask\Year 4\Term 1\CMPT 370\comp370fall2022\connecting_airport_departures.csv")