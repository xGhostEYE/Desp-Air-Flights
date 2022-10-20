import pandas as pd
from py2neo import Graph


gdb = Graph(scheme="http", host="172.19.0.3:7474", user="neo4j", password="password")

gdb.run("Merge (:test {id: 1})")

if __name__ == "__main__":
    print("done")   