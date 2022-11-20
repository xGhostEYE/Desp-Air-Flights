import pandas as pd
from datetime import date, datetime

import sys
import os

sys.path.append(os.path.abspath("./scraping/"))
import harvest_flights as harv

def get_flight_prices(departure_airport, destination_airport):
    price_df = harv.price_link_scrape(departure_airport, destination_airport, str(date.today()))
    return price_df


if __name__ == "__main__":
    departure_airport = ""
    destination_airport = ""

    df = add_flight_prices(departure_airport, destination_airport)
    df.to_csv(f"./__data/test/{departure_airport}_to_{destination_airport}_prices.csv", index=False)