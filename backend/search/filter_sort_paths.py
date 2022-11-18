import find_path
import pandas as pd

def filter_by_time(path_df, startTime=None, endTime=None):
    """filters paths based on DepartureTimes and ArrivalTimes
    
    filters out paths with a DepartTime after startTime and an ArrivalTime before endtime

    Args:
        path_df:
            dataframe with path data
        startTime:
            earliest departure time
        endTime:
            latest arrival time
    
    Returns:
        dataframe containing the paths that made it through the filters
    """

    filteredPath_df = path_df.copy()

    if startTime != None:
        filteredPath_df = filteredPath_df[filteredPath_df["DepartTime"] >= startTime]

    if endTime != None:
        filteredPath_df = filteredPath_df[filteredPath_df["ArrivalTime"] < endTime]


    return filteredPath_df


def sort_by_time(path_df):
    return None

if __name__ == "__main__":
    departure = "Richmond"
    destination = "Calgary"

    path_df = find_path.get_all_valid_paths(departure, destination)

    filteredPath_df = filter_by_time(path_df, "10:00")
    print(filteredPath_df)