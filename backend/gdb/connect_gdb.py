from py2neo import Graph

def connect_gdb():
    """Connects to the neo4j database in the docker container"""
    gdb = Graph("bolt://cmpt370-db:7687", user="neo4j", password="password")
    return gdb

def connect_test_gdb():
    """Connects to a test neo4j database"""
    gdb = Graph("bolt://cmpt370-testdb:7687", auth=("neo4j", "password"))
    return gdb
   
