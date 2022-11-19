def remove_all_data(gdb):
    """deletes all nodes and relationships in the given gdb
    
    args:
        gdb: py2neo Graph
            connection to the neo4j database
    """

    cypher = """
             MATCH (n)
             DETACH DELETE n
             """

    gdb.run(cypher)

