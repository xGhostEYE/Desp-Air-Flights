import pandas as pd

import connect_gdb as conGDB

def add_airport(city, airport_code, gdb=None):
    """Adds an airport node to the gdb.

    Creates an Airport node in the neo4j database. The Airport is created with 
    the properties: "City" and "Code"

    Args:
        city: String
            city the airport is in
        airport_code: String
            airport code of the airport we are adding
        gdb: py2neo Graph
            connection to the neo4j database
    """

    if gdb==None:
        gdb = conGDB.connect_gdb()
    
    cypher = """
             MERGE (a:Airport {Code: $code})
             SET a.City = $city
             """
    
    gdb.run(cypher, parameters={"code": airport_code, "city": city})


def add_airports_from_df(airport_df, gdb=None):
    """Adds airport nodes to the gdb.

    Creates Airport nodes in the neo4j database. The Airports are created with 
    the properties: "City" and "Code"

    Args:
        airport_df: pandas Dataframe
            Dataframe with airports to add to the gdb. Needed columns are "Code"
            and "City"
        gdb: py2neo Graph
            connection to the neo4j database
    """

    if gdb==None:
        gdb = conGDB.connect_gdb()

    # converts the airport_df into a numpy array. [0] = City, [1] = Code
    airport_df = airport_df[["City", "Code"]]
    airport_array = airport_df.to_numpy()
    
    # iterates through the airport array calling add_airport()
    for airport in airport_array:
        city = airport[0]
        code = airport[1]

        add_airport(city=city, airport_code=code, gdb=gdb)

if __name__ == "__main__":
    airport_df = pd.read_csv("./__data/airports_in_gdb/Airports.csv")
    add_airports_from_df(airport_df)



