import pandas as pd

import add_airports
import connect_gdb as conGDB
import misc_queries


def get_airport_data(code, gdb):
    
    cypher = """
             MATCH (a:Airport {Code: $code})
             RETURN a.City as City, a.Code as Code
             """

    results = gdb.run(cypher, parameters={"code": code}).to_ndarray()
    return results

if __name__ == "__main__":
    testgdb = conGDB.connect_test_gdb()

    # test add_airport function
    city = "A"
    code = "YYA"
    add_airports.add_airport(city, code, testgdb)
    results = get_airport_data(code, testgdb)[0]
    cityResult = results[0]
    if cityResult != "A":
        print("function add_airport failed, resulting City is", cityResult, "instead of", city)
    codeResult = results[1]
    if codeResult != "YYA":
        print("function add_airport failed, resulting Code is", codeResult, "instead of", code)

    misc_queries.remove_all_data(testgdb)

    # test add_airports_from_df function
    # tests 26 airports with city A-Z and code YYA-YYZ
    airport_df = pd.read_csv("./__data/test_data/Airports_test.csv")
    add_airports.add_airports_from_df(airport_df, testgdb)

    airport_codes = airport_df["Code"].tolist()
    # checks city and code of all 26 airports
    for code in airport_codes:
        answer_df = airport_df[airport_df["Code"] == code]
        city = answer_df["City"].values[0]

        results = get_airport_data(code, testgdb)[0]
        cityResult = results[0]
        if cityResult != city:
            print("function add_airports_from_df failed, resulting City is", cityResult, "instead of", city)
        codeResult = results[1]
        if codeResult != code:
            print("function add_airports_from_df failed, resulting Code is", codeResult, "instead of", code)

    misc_queries.remove_all_data(testgdb)
