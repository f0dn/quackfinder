import osmnx as ox

# Download a street network
G = ox.graph_from_place("Queens, New York, USA", network_type="drive")

# Print basic summary statistics (nodes, edges, average street length, etc.)
stats = ox.stats.basic_stats(G)
print(stats)
print("Total Edges", G.number_of_edges())


nodes, edges = ox.graph_to_gdfs(G)
street_name = "2nd Street"
specific_street = edges[edges["name"] == street_name]

print(specific_street[["name", "geometry"]])
ox.plot_graph_route(G, routes=[list(specific_street.index)[0]])
