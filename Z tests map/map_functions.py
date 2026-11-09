import folium
from branca.element import MacroElement
from jinja2 import Template
#All these functions are based on folium; all of them create/interact a static html map
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

def User_Markers(m:folium.Map):
    folium.ClickForMarker().add_to(m)

def add_layer(m:folium.Map, name: str):
    layer = folium.FeatureGroup(
        name = name , 
        overlay = True
        )
    layer.add_to(m)
    return layer

def print_points(points: list[list[float]]):
    for lat,lng in points:
        print(lat,lng)

class ClickReporter(MacroElement):
    ##This keeps the first click, and the last click, so we have a starting/ending point;
    ##Doesn't keep any of the clicks in the middle
    
    ##THIS IS MOSTLY JavaScript AND I DON'T KNOW HOW IT WORKS
    ##SINCE I DON'T KNOW JAVASCRIPT
    _template = Template("""
        {% macro script(this, kwargs) %}
        // Draw the saved points (at most 2) and remember the marker objects
        const markers = {{ this.points|tojson }}.map(
            p => L.marker(p).addTo({{ this._parent.get_name() }})
        );

        {{ this._parent.get_name() }}.on("click", function (e) {
            const point = e.latlng.wrap();
            if (markers.length < 2) {
                // first or second click: add a new marker
                markers.push(L.marker(point).addTo({{ this._parent.get_name() }}));
            } else {
                // already 2 markers: move the end marker instead of adding one
                markers[1].setLatLng(point);
            }
            fetch({{ this.url|tojson }}, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({lat: point.lat, lng: point.lng}),
            }).catch(console.error);
        });
        {% endmacro %}
    """)

    def __init__(self, url="/points", points=None):
        super().__init__()
        self._name = "ClickReporter"
        self.url = url
        self.points = points or []  # markers to draw when the page loads
