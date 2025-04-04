import requests
import json
import networkx as nx
from itertools import permutations, combinations

# Base URL for querying floatrates.com for currency exchange rates
url1 = "http://www.floatrates.com/daily/"
url2 = ".json"

# List of currencies to analyze (modify as needed)
currencies = ["usd", "eur", "gbp"]  # Example currencies

# Initialize a directed graph
g = nx.DiGraph()

# Step 1: Fetch exchange rates and populate the graph with edges
edges = []
for c1 in currencies:  # Loop through source currencies
    url = url1 + c1 + url2  # Construct API URL
    req = requests.get(url)  # Send GET request to the API
    if req.status_code == 200:  # Check if request was successful
        dct1 = json.loads(req.text)  # Parse JSON response
        for c2 in currencies:
            if c1 != c2 and c2 in dct1:  # Ensure target currency is valid and different
                rate = dct1[c2]['rate']  # Extract exchange rate
                edges.append((c1, c2, rate))  # Create an edge with weight (exchange rate)
    else:
        print(f"Failed to fetch data for {c1}, status code: {req.status_code}")

# Add edges to the graph
g.add_weighted_edges_from(edges)
print(f"Graph nodes: {g.nodes}")
print(f"Graph edges: {g.edges(data=True)}")

# Step 2: Calculate all paths and weights
results = []  # To store results for each currency pair

# Loop through all unique combinations of nodes (currency pairs)
for n1, n2 in combinations(g.nodes, 2):  # All combinations of two currencies
    print(f"Paths from {n1} to {n2} ----------------------------------")

    # Find all simple paths from n1 to n2
    for path in nx.all_simple_paths(g, source=n1, target=n2):
        print("Path To", path)

        # Calculate the forward path weight
        path_weight_to = 1.0
        for i in range(len(path) - 1):  # Iterate through edges in the path
            path_weight_to *= g[path[i]][path[i + 1]]['weight']  # Multiply edge weights
        print("Path weight to: ", path_weight_to)

        # Reverse the path to calculate the return path weight
        path.reverse()
        print("Path From", path)

        # Calculate the reverse path weight
        path_weight_from = 1.0
        for i in range(len(path) - 1):  # Iterate through edges in the reversed path
            path_weight_from *= g[path[i]][path[i + 1]]['weight']
        print("Path weight from: ", path_weight_from)

        # Compute the equilibrium factor
        factor = path_weight_to * path_weight_from
        results.append((path, path_weight_to, path_weight_from, factor))
        print(f"Equilibrium weight factor: {factor}\n")
    print("---------------\n")

# Step 3: Find smallest and largest path weight factors
if results:
    # Find the path with the smallest weight factor
    smallest = min(results, key=lambda x: x[3])  # Smallest factor
    greatest = max(results, key=lambda x: x[3])  # Greatest factor

    print(f"Smallest Path Weight Factor: {smallest[3]}")
    print(f"Paths: {smallest[0]}")

    print(f"Greatest Path Weight Factor: {greatest[3]}")
    print(f"Paths: {greatest[0]}")

# Wait for user input before exiting
input("Press enter to exit...")