import sys
import os

sys.path.append(os.path.abspath("./gdb/"))
import connect_gdb as conGDB


def create_path_graph():
    """Creates a graph for use by the algorithm (graph named "pathGraph")"""

    gdb = conGDB.connect_gdb()

    drop_path_graph()

    cypher = """
             CALL gds.graph.project.cypher(
             'pathGraph',
             "MATCH (a:Airport) RETURN id(a) as id",
             "MATCH (a)-[f:Flight]-(a2:Airport) RETURN id(a) AS source, id(a2) AS target, id(f) as id"
             )"""

    gdb.run(cypher)

def drop_path_graph():
    """Removes the graph used for the algorithm (graph named "pathGraph")"""
    
    gdb = conGDB.connect_gdb()

    cypher = "CALL gds.graph.drop('pathGraph', false)"
    gdb.run(cypher)    



def get_path(departure, destination):
    gdb = conGDB.connect_gdb()

    cypher = """
             MATCH (source:Airport {City: $departure}), (target:Airport {City: $destination})
             CALL gds.shortestPath.yens.stream('pathGraph', {
                sourceNode: source,
                targetNode: target,
                k: 3
                
             })
             YIELD index, sourceNode, targetNode, nodeIds, path
             UNWIND relationships(path) as rel
             RETURN
                 index,
                 gds.util.asNode(sourceNode).City AS departureCity,
                 gds.util.asNode(targetNode).City AS destinationCity,
                 [nodeId IN nodeIds | gds.util.asNode(nodeId).City] AS connectingCities,
                 nodes(path) as path,
                 rel
             ORDER BY index
             """
    
    paths = gdb.run(cypher, parameters={"departure": departure, "destination": destination}).to_data_frame()
    
    return paths

# def check_path_validity():


if __name__ == "__main__":
    create_path_graph()

    departure = "Saskatoon"
    destination = "Toronto"

    paths = get_path(departure, destination)
    print(paths)
    paths.to_csv(f"./__data/test_paths/{departure}_to_{destination}.csv", index=False)
    
