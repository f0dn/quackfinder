import folium
def create_map(lat: float, long: float , zoom: int): #Uses OpenStreetMap
    m = folium.Map(
        location = (lat, long),
        zoom_start = zoom,
        tiles = "OpenStreetMap"
    )
    return m
    
def add_marker(m: folium.Map , latitude: float , longitude: float):
    folium.Marker(
        location = [latitude , longitude]
    ).add_to(m)

def add_line(m: folium.Map , lat1: float , long1: float , lat2: float, long2: float , tip: str):
    coordinates = [
        [lat1 , long1],
        [lat2, long2],
    ]
    folium.PolyLine(
        locations = coordinates,
        color = "#000DFF",
        weight = 5, 
        tooltip = tip
    ).add_to(m)

def save_map(m:folium.Map, name: str):
    m.save(name + ".html")

def add_route(m: folium.Map , coords: list[list[float]]): #DOES NOT SMOOTH OUT ANY LINES
    folium.PolyLine(
        locations = coords,
        color = "#000DFF",
        weight = 5,
    ).add_to(m)

