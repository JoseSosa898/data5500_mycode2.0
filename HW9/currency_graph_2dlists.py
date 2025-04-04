import requests 
import json  
import time  
from datetime import datetime, timedelta  
from itertools import combinations

import networkx as nx  # Library for creating and analyzing graphs
from networkx.classes.function import path_weight  # Function for calculating path weights in graphs

# List of cryptocurrency symbols (nodes for the graph)
currencies = ('xrp', 'ada', 'eos', 'ltc', 'eth', 'btc')

# Exchange rate matrix: each inner list represents rates from one currency to others
# Example: rates[i][j] is the rate of converting currencies[i] to currencies[j]
rates = [
    [1, 0.23, 0.25, 16.43, 18.21, 4.94],  
    [4.34, 1, 1.11, 71.40, 79.09, 21.44],  
    [3.93, 0.90, 1, 64.52, 71.48, 19.37],  
    [0.061, 0.014, 0.015, 1, 1.11, 0.30],  
    [0.055, 0.013, 0.014, 0.90, 1, 0.27],  
    [0.20, 0.047, 0.052, 3.33, 3.69, 1],  
]

# Create a directed graph to represent the currency exchange network
g = nx.DiGraph()  
edges = []  # List to store graph edges (connections between currencies)

# Loop through each currency pair to populate the graph with edges
i = 0  
for c1 in currencies:
    j = 0  
    for c2 in currencies:
        if c1 != c2:  # Skip adding edges where source and target are the same
            edges.append((c1, c2, rates[i][j]))  # Add edge with weight (exchange rate)
            print("Adding edge: ", c1, c2, rates[i][j])  # Log the edge being added
        j += 1  
    i += 1  

# Add all edges with weights to the graph
g.add_weighted_edges_from(edges)


print(g.nodes)

###########################################
# Traversing the graph and analyzing paths
# Compute paths and their weights for each pair of currencies

# Loop through all unique combinations of nodes (currency pairs)
for n1, n2 in combinations(g.nodes, 2):  
    print("All paths from ", n1, "to", n2, "---------------")

   
    for path in nx.all_simple_paths(g, source=n1, target=n2):
        print("Path To", path) 

        path_weight_to = 1.0
        
        for i in range(len(path) - 1):  
            path_weight_to *= g[path[i]][path[i + 1]]['weight']  
        print("Path weight: ", path_weight_to)  

       
        path.reverse()
        print("Path From", path)  

        path_weight_from = 1.0
        
        for i in range(len(path) - 1):  
            path_weight_from *= g[path[i]][path[i + 1]]['weight']  # Multiply edge weights
        print("Path weight: ", path_weight_from)  # Print the calculated weight of the reversed path

    print("---------------\n")  # Add a divider for readability of output


input("Press enter to exit...")