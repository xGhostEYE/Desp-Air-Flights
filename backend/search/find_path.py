import sys
import os

sys.path.append(os.path.abspath("./gdb/"))
import connect_gdb as conGDB

def get_path(departure, destination):

    gdb = conGDB.connect_gdb()

    cypher = """
             MATCH (start:Airport{City: $departure}), (end:Airport{City: $destination})
             CALL apoc.algo.dijkstra(start, end, "Flight>", "Price", 1, 2)
             YIELD path, weight
             WITH apoc.path.elements(path) AS elements
             UNWIND range(0, size(elements)-2) AS index
             WITH elements, index
             WHERE index %2 = 0
             WITH elements[index] AS a1, elements[index+1] AS f, elements[index+2] AS a2
             RETURN a1.City as departFrom,
                f.FlightNum as FlightNum,
                f.DepartTime as DepartTime,
                f.ArrivalTime as ArrivalTime,
                a2.City as arriveAt
             
             """
    paths = gdb.run(cypher, parameters={"departure": departure, "destination": destination}).to_data_frame()
    

    
    return paths

if __name__ == "__main__":
    

    departure = "Saskatoon"
    destination = "Toronto"

    paths = get_path(departure, destination)
    print(paths)
    paths.to_csv(f"./__data/test_paths/{departure}_to_{destination}.csv", index=False)