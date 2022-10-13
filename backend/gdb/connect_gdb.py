import pandas as pd
from py2neo import Graph

gdb = Graph("bolt://localhost:7474", auth=("neo4j", "neo4j"))
