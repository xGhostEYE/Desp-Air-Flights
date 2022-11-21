import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import add_airports
import update_flight_data
import connect_gdb as conGDB
import misc_queries

def check_departure_flights(departure_df, gdb):
    """checks flight data in given dataframe to data in the gdb"""
    flightNums = departure_df["Flight"].unique().tolist()
    for flightNum in flightNums:
        
        cypher = """
                MATCH (a1:Airport)-[f:Flight {FlightNum: $flightNum}]->(a2:Airport)
                RETURN a1.Code as Departure,
                        f.DepartTime as DepartTime,
                        f.Status as Status,
                        f.Carrier as Carrier,
                        f.FlightNum as FlightNum,
                        f.Gate as Gate,
                        a2.Code as DestinationCode
                """
        
        results_df = gdb.run(cypher, parameters={"flightNum": flightNum}).to_data_frame()

        # check departure Code
        departureCode = departure_df["Departure Code"].values[0]
        departureCode_result = results_df["Departure"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", departure codes did not match: ")
            print("Input:", departureCode, "\nOutput:", departureCode_result)

        # check departure time
        departureTime = departure_df["Departure"].values[0]
        departureTime_result = results_df["DepartTime"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", departure times did not match: ")
            print("Input:", departureTime, "\nOutput:", departureTime_result)

        # check Status
        status = departure_df["Status"].values[0]
        status_result = results_df["Status"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", flight status did not match: ")
            print("Input:", status, "\nOutput:", status_result)
        
        # check Carrier
        carrier = departure_df["Carrier"].values[0]
        carrier_result = results_df["Carrier"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", flight carrier did not match: ")
            print("Input:", carrier, "\nOutput:", carrier_result)

        # check flightNum
        flightNum = departure_df["Flight"].values[0]
        flightNum_result = results_df["FlightNum"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", flight number did not match: ")
            print("Input:", flightNum, "\nOutput:", flightNum_result)
        
        # check gate
        gate = departure_df["Gate"].values[0]
        gate_result = results_df["Gate"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", flight gate did not match: ")
            print("Input:", gate, "\nOutput:", gate_result)
        
        # check destination Code
        destinationCode = departure_df["Airport Code"].values[0]
        destinationCode_result = results_df["DestinationCode"].values[0]
        if departureCode != departureCode_result:
            print("\nupdate_airport_departures function failed for flight", flightNum, ", destination codes did not match: ")
            print("Input:", destinationCode, "\nOutput:", destinationCode_result)



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
    
    check_departure_flights(departure_df, testgdb)
    
    
    