#currently only removes the second time
from __future__ import print_function
# from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
from urllib.request import urlopen
from numpy import NaN
import pandas as pd
import os
from os.path import exists



def clean_data(file):
    cleanedflights = []
    df = pd.read_csv(file)
    for name, values in df[['Flight']].items():
        data = values.str.split()
        for i in range(len(data)):
            if data[i] is NaN or (str(data[i][0][0]).isalpha() == False or str(data[i][0][1]).isalpha() == False) :
                continue
            else:
                print(data[i][0])
                if len(str(data[i])) == 1:
                    cleanedflights[i] = str(data[i][0])
                if len(str(data[i])) >= 2:
                    cleanedflights[i] = str.join(str(data[i][0]) + str(data[i][1]))
                print(cleanedflights[i])

clean_data("/student/mel196/Documents/comp370/comp370fall2022/connecting_airport_departures.csv")