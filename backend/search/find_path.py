import sys
import os

import pandas as pd
from datetime import date, datetime

sys.path.append(os.path.abspath("./gdb/"))
import connect_gdb as conGDB

def get_paths_from_dijkstra(departure, destination, number_of_paths=1, weight="Connections"):
    """gets flight paths from the gdb using the dijkstra algorithm

    Args:
        departure: String
            Code of the airport we are departing from
        destination: String
            Code of the destination airport
        number_of_paths: int
            number of paths to return
        weight: String
            property in the relationship we will use as the weight
    Returns:
        dataframe containing path data
    """

    gdb = conGDB.connect_gdb()

    defaultWeight = 1
    if weight == "Cost":
        # high default val so flights without price arent used
        defaultWeight = 99999
        

    cypher = """
             MATCH (start:Airport{Code: $departure}), (end:Airport{Code: $destination})
             CALL apoc.algo.dijkstra(start, end, "Flight>", $weight, 1, $numPaths)
             YIELD path, weight
             WITH apoc.path.elements(path) AS elements
             UNWIND range(0, size(elements)-2) AS index
             WITH elements, index
             WHERE index %2 = 0
             WITH elements[index] AS a1, elements[index+1] AS f, elements[index+2] AS a2
             RETURN a1.City as departFrom,
                a1.Code as departCode,
                f.FlightNum as FlightNum,
                f.Carrier as Carrier,
                f.DepartTime as DepartTime,
                f.ArrivalTime as ArrivalTime,
                f.Cost as Cost,
                a2.City as arriveAt,
                a2.Code as arriveCode
             
             """

    params ={"departure": departure, 
             "destination": destination, 
             "numPaths": number_of_paths,
             "weight": weight}

    paths_df = gdb.run(cypher, parameters=params).to_data_frame()
    
    if paths_df.empty:
        return None

    # label paths
    codes = paths_df["departCode"].tolist()
    path = []
    pathNum = 0
    for code in codes:
        if code == departure:
            pathNum +=1
        path.append(pathNum)

    paths_df["path"] = path
    return paths_df


def path_is_valid(path):
    """Checks if a path is valid
    
    path is valid if the arrival is before the departure of the next flight

    Args:
        path: dataframe
            dataframe containing info on a single path
    Returns:
        boolean indicating whether or not path is valid
    """

    # returns false if any DepartTimes or ArrivalTimes are null
    if path["DepartTime"].isnull().values.any() or path["ArrivalTime"].isnull().values.any():
        return False
    
    # convert DepartTimes and ArrivalTimes to datetime object
    # path["DepartTime"] = pd.to_datetime(path["DepartTime"], infer_datetime_format=True)
    # path["ArrivalTime"] = pd.to_datetime(path["ArrivalTime"], infer_datetime_format=True)

    # valid if the arrival is before the departure of the next flight for all flights, else returns false
    departTimes = path["DepartTime"].tolist()
    arrivalTimes = path["ArrivalTime"].tolist()

    numFlights = len(departTimes)

    for i in range(numFlights):
        if i == numFlights - 1:
            return True
        if arrivalTimes[i] >= departTimes[i+1]:
            return False 

    return True


def get_paths(departure, destination, number_of_paths=1, startTime=str(date.today()), weight="Connections"):
    """gets flight paths from departure to destination

    Args:
        departure: String
            Code of the airport we are departing from
        destination: String
            Code of the destination airport
        number_of_paths: int
            number of paths to return
        startTime: String
            flights departure must be after this time
        weight: String
            property in the flight relationship, in the gdb, we will use as the weight

    Returns:
        dataframe with path data, if there are no valid paths returns None
    """
    validPaths_df = pd.DataFrame()
    number_of_valid_paths = 0
    num_paths_to_query = number_of_paths
    num_paths_already_checked = 0

    # loops until the desired number of valid paths are found, if paths cant be found, breaks
    while number_of_valid_paths != number_of_paths:
        paths_df = get_paths_from_dijkstra(departure, destination, num_paths_to_query)

        if paths_df is None:
            return None

        # dataframe of paths that havent been checked
        pathCheck_df = paths_df[paths_df["path"] > num_paths_already_checked]

        #
        pathCheck_df

        # iterates through and checks paths for validity, if valid adds to validPaths_df
        paths = pathCheck_df["path"].unique().tolist()
        for path in paths:
            path_df = pathCheck_df[pathCheck_df["path"] == path]
            pathDepartureTime = path_df["DepartTime"].values[0]
            print(pathDepartureTime, ">=", startTime)
            if pathDepartureTime >= startTime:
                if path_is_valid(path_df):
                    validPaths_df = pd.concat([validPaths_df, path_df])
                    number_of_valid_paths +=1
                    
                    if number_of_valid_paths == number_of_paths:
                        break

        num_paths_already_checked = num_paths_to_query
        num_paths_to_query = num_paths_to_query * 2

        # checks if num_paths_already_checked is greater than maxPath, meaning
        # there are no more paths to check and breaks loop
        maxPath = paths_df["path"].max()
        if maxPath < num_paths_already_checked:
            break

    if validPaths_df.empty:
        return None

    return validPaths_df

def get_all_valid_paths(departure, destination):
    """gets all valid flight paths from departure to destination

    Args:
        departure: String
            Code of the airport we are departing from
        destination: String
            Code of the destination airport
    Returns:
        dataframe with data for all valid paths, if there are no valid paths returns None
    """
    validPaths_df = pd.DataFrame()
    num_paths_to_query = 100
    num_paths_already_checked = 0

    not_all_paths_found = True

    # loops until all paths have been found and checked for validity
    while not_all_paths_found:
        paths_df = get_paths_from_dijkstra(departure, destination, num_paths_to_query)

        if paths_df is None:
            return None

        # dataframe of paths that havent been checked
        pathCheck_df = paths_df[paths_df["path"] > num_paths_already_checked]

        # iterates through and checks paths for validity, if valid adds to validPaths_df
        paths = pathCheck_df["path"].unique().tolist()
        for path in paths:
            path_df = pathCheck_df[pathCheck_df["path"] == path]
            if path_is_valid(path_df):
                validPaths_df = pd.concat([validPaths_df, path_df])

        num_paths_already_checked = num_paths_to_query
        num_paths_to_query = num_paths_to_query * 2

        # checks if num_paths_already_checked is greater than maxPath, meaning
        # there are no more paths to check and breaks loop
        maxPath = paths_df["path"].max()
        if maxPath < num_paths_already_checked:
            not_all_paths_found = False

    if validPaths_df.empty:
        return None

    return validPaths_df


def convert_paths_to_json(paths_df):
    """converts the given dataframe of path data to a JSON

    Args:
        paths_df:
            dataframe with path data
    Returns:
        json with path data, if there are no valid paths returns None
    """
    if paths_df is None:
        return None

    paths = paths_df["path"].unique().tolist()

    path_jsons = []

    # formats each path
    for path in paths:
        path_df = paths_df[paths_df["path"] == path]

        flights = []
        # formats each flight
        for i in path_df.index:
            flight = {
                "departure": {
                    "location": path_df.loc[i, "departFrom"],
                    "time": path_df.loc[i, "DepartTime"],
                    "airport code": path_df.loc[i, "departCode"]
                },
                "arrival": {
                    "location": path_df.loc[i, "arriveAt"],
                    "time": path_df.loc[i, "ArrivalTime"],
                    "airport code": path_df.loc[i, "arriveCode"]
                },
                "cost": path_df.loc[i, "Cost"],
                "airline":  path_df.loc[i, "Carrier"],
                "flight number": path_df.loc[i, "FlightNum"]
            }
            flights.append(flight)


        path_json = {
            "flights": flights 
        }
        path_jsons.append(path_json)


    return path_jsons

if __name__ == "__main__":
    
    # departure = "Richmond"
    # destination = "Calgary"

    departure = "YTZ"
    destination = "YOW"

    paths = get_paths_from_dijkstra(departure, destination, 500)
    paths.to_csv(f"./__data/test_paths/{departure}_to_{destination}_test.csv", index=False)

    # paths = get_paths(departure, destination, 10)
    # paths.to_csv(f"./__data/test_paths/{departure}_to_{destination}.csv", index=False)

    # paths = get_all_valid_paths(departure, destination)
    # paths.to_csv(f"./__data/test_paths/{departure}_to_{destination}_all.csv", index=False)

    # pathsJSON = convert_paths_to_json(paths)
    # print(pathsJSON)
    # paths = get_paths_json(departure, destination, 10)
    # print(paths)

    