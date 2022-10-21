from py2neo import Graph

def connect_gdb():
    gdb = Graph("bolt://cmpt370-db:7687", user="neo4j", password="password")
    return gdb

   

