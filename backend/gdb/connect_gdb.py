import pandas as pd
from py2neo import Graph
import numpy as np

# gdb = Graph(scheme="http", host="cmpt370-db", port="7474", user="neo4j", password="password", name="neo4j", secure=True)
gdb = Graph("bolt://localhost:7687", user="neo4j", password="password")

gdb.run("MERGE (:Test {testNum:1})")
print(gdb)   

