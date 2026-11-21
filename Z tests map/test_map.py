#uses folium for mapping
import folium
def testing_map_creation(): #NEEDS LOCALHOST python -m http.server 8000 , then http://localhost:8000/name_of_file.html
    m = folium.Map(
        location = (40.9153, -73.1231),
        zoom_start = 20,
        tiles = "OpenStreetMap"
    )
    m.save("testMap.html")

def test_add_lines(): #Adds lines from A --> B --> C, etc. 
    coordinates = [
        [40.91532, -73.123111],
        [40.92535, -73.123111],
        [40.93538, -73.123111],
    ]
    m = folium.Map(
        location = (40.9153, -73.1231),
        zoom_start = 20,
        tiles = "OpenStreetMap"
    )
    folium.PolyLine( # Adds lines to the map
        locations = coordinates,
        color="#000DFF",
        weight=5,
        tooltip = "Random Points in SBU.",
    ).add_to(m)

    m.save("testLinesMap.html")

def test_marker(): #Add a marker to a random point at SBU
    m = folium.Map(
            location = (40.9153, -73.1231),
            zoom_start = 20,
            tiles = "OpenStreetMap"
    )
    folium.Marker(
        location = [40.9153, -73.1231],
        popup = folium.Popup("Test Point at SBU", parse_html = True , max_width = 100),
    ).add_to(m)

    m.save("testMarkersMap.html")




