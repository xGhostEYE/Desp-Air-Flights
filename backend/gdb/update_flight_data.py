import pandas as pd
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath("./scraping/"))
import harvest_flights as harv

import connect_gdb as conGDB




def update_airport_departures(airport_code, gdb=None):
    airport_dept_df = harv.harvest_data_departures(airport_code)

    if gdb==None:
        gdb = conGDB.connect_gdb()

    # airport_cypher = f"""MERGE (:Airport {{City: "{airport}"}})"""
    # gdb.run(airport_cypher)
    
    flight_Nums = airport_dept_df["Flight"].unique().tolist()

    for flight_Num in flight_Nums:
        flight_df = airport_dept_df[airport_dept_df["Flight"] == flight_Num]
        
        destination = flight_df["Destination"].values[0]
        status = flight_df["Status"].values[0]
        carrier = flight_df["Carrier"].values[0]
        gate = flight_df["Gate"].values[0]

        # update destination to airport code instead of city
        props = {
            "Departure": str(airport_code),
            "Destination": str(destination),
            "FlightNum": str(flight_Num),
            "Status": str(status),
            "Carrier": str(carrier),
            "Gate": str(gate)
        }

        print(props)

        flight_cypher = """
                        With $flt as flt
                        MATCH (a1:Airport {Code: flt["Departure"]})
                        MERGE (a2:Airport {City: flt["Destination"]})
                        MERGE (a1)-[f:Flight {FlightNum: flt["FlightNum"]}]->(a2)
                        SET f = flt
                        SET a1.depUpdated = date()
                        """
        gdb.run(flight_cypher, parameters={"flt": props})

    print("Finished added departing flights from", airport_code)

def update_departures():
    gdb = conGDB.connect_gdb()

    cypher = """
             MATCH (a:Airport)
             WHERE EXISTS(a.Code) AND
             NOT EXISTS(a.depUpdated) OR 
             a.depUpdated < date() 
             RETURN a.Code as Code
             """

    airport_codes = gdb.run(cypher).to_ndarray()

    # converts the array of airport_codes to a list
    airport_codes = [x[0] for x in airport_codes]

    for code in airport_codes:
        # print(code)
        update_airport_departures(airport_code=code, gdb=gdb)

if __name__ == "__main__":
    # dep_airport = "YEG"
    # update_airport_departures(dep_airport)
    update_departures()
