import pandas as pd
from py2neo import Graph
import numpy as np

gdb = Graph("bolt://localhost:7474", auth=("neo4j", "neo4j"))
