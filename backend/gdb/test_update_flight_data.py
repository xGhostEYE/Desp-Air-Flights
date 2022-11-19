import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import add_airports
import update_flight_data
import connect_gdb as conGDB
import misc_queries


if __name__ == "__main__":
    testgdb = conGDB.connect_test_gdb()
    misc_queries.remove_all_data(testgdb)

    airport_df = pd.read_csv("./__data/test_data/Airports_test.csv")
    add_airports.add_airports_from_df(airport_df=airport_df, gdb=testgdb)

    # test update_airport_departures function
    departure_df = pd.read_csv("./__data/test_data/Departures_test.csv")
    departureCodes = departure_df["Departure Code"].unique().tolist()

    print(departureCodes)
    
    for departureCode in departureCodes:
        airportDeparture_df = departure_df[departure_df["Departure Code"] == departureCode]
        airportDeparture_df.drop(columns=["Departure Code"], inplace=True)
        update_flight_data.update_airport_departures(airport_code=departureCode, gdb=testgdb, airport_dept_df=airportDeparture_df)
    