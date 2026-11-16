import requests
import osmnx as ox
from pyhigh import get_elevation


def get_elevation(lat, lon, dataset="ned10m"):
    url = f"https://api.opentopodata.org/v1/{dataset}"
    params = {"locations": f"{lat},{lon}"}
    response = requests.get(url, params=params)
    data = response.json()
    return data["results"][0]["elevation"]


# Download a street network
place = "Stony Brook, New York, USA"
street_name = "Bentley Lane"
print(street_name, "\n")
G = ox.graph_from_place(place, network_type="drive")

# Print basic summary statistics (nodes, edges, average street length, etc.)
stats = ox.stats.basic_stats(G)
print(stats)
print("Total Edges", G.number_of_edges())
lat, lon = ox.geocode(place)
print(f"Latitude: {lat}, Longitude: {lon}")


nodes, edges = ox.graph_to_gdfs(G)
# gdf = ox.features_from_place(place, tags={"highway":True})
specific_street = edges[edges["name"] == street_name]
u, v, key = specific_street.index[0]
print(specific_street, "\n")
print(edges[["name", "highway", "length", "geometry"]].head())


print(specific_street[["name", "geometry"]])
print(get_elevation(lat, lon))
fig, ax = ox.plot_graph_route(G, route=[u,v])
