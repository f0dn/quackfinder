import folium
from branca.element import MacroElement
from folium.elements import JSCSSMixin
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

class ClickReporter(JSCSSMixin, MacroElement):
    ##This keeps the first click, and the last click, so we have a starting/ending point;
    ##Doesn't keep any of the clicks in the middle

    ##The actual JavaScript is in static/JS_functions.js (setupClickReporter).
    ##default_js makes folium add <script src="/static/JS_functions.js"> to the page,
    ##and the template below just calls that function with our data.
    default_js = [("JS_functions", "/static/JS_functions.js")]

    _template = Template("""
        {% macro script(this, kwargs) %}
        setupClickReporter({{ this._parent.get_name() }}, {{ this.points|tojson }}, {{ this.url|tojson }});
        {% endmacro %}
    """)

    def __init__(self, url="/points", points=None):
        super().__init__()
        self._name = "ClickReporter"
        self.url = url
        self.points = points or []  # markers to draw when the page loads
