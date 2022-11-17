import connect_gdb as conGDB

def get_airports():
    """Gets airport data from the gdb
    
    Returns:
        numpy array containing airport data in the order City Column"""
    gdb = conGDB.connect_gdb()

    cypher = """
             MATCH (a:Airport)
             RETURN a.City as City, a.Code as Code
             """

    airportData = gdb.run(cypher).to_ndarray()
    return airportData


if __name__ == "__main__":
    airport_data = get_airports()
    print(airport_data)