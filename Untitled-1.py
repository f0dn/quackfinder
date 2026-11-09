
import folium

# Example coordinates (latitude, longitude)
route1 = [
    [40.7580, -73.9855],
    [40.7550, -73.9820],
    [40.7527, -73.9772]
]

route2 = [
    [40.7580, -73.9855],
    [40.7570, -73.9800],
    [40.7527, -73.9772]
]

# Create the map
m = folium.Map(location=[40.755, -73.982], zoom_start=15)

# Draw two possible routes
folium.PolyLine(
    route1, color="blue", weight=6,
    tooltip="Route 1"
).add_to(m)

folium.PolyLine(
    route2, color="red", weight=6,
    tooltip="Route 2"
).add_to(m)

# Starting and ending locations
folium.Marker(route1[0], popup="Start").add_to(m)
folium.Marker(route1[-1], popup="Destination").add_to(m)

# Save to HTML
m.save("map.html")
