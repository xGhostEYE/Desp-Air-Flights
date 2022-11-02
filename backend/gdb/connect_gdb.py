from py2neo import Graph

def connect_gdb():
    """Connects to the neo4j database in the docker container"""
    gdb = Graph("bolt://cmpt370-db:7687", user="neo4j", password="password")
    return gdb

   

