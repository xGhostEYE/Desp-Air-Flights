import pandas as pd

import add_airports
import update_flight_data

def add_initial_data(airport_file="./__data/airports_in_gdb/Airports.csv"):
    """Adds flight data and airport data to the gdb (presumed empty)

    Args:
        airport_file: String of filepath
            csv containing airports City and Code
    """
    airport_df = pd.read_csv(airport_file)
    add_airports.add_airports_from_df(airport_df)

    update_flight_data.update_flight_data()

if __name__ == "__main__":
    add_initial_data()
