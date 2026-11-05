from flask import *
from map_functions import *

def main():
    app = Flask(__name__)
    clicked_points  = []

    @app.route("/")
    def home():
        map = create_map(40.9153, -73.1231, 20)
        coordinates = [
            [40.9153, -73.1231],
            [40.917238, -73.124638],
            [40.9135, -73.1260]
        ]
        add_route(map, coordinates)

        for lat,long in clicked_points:
            add_marker(map, lat, long)

        ClickReporter().add_to(map)
        map_html = map.get_root().render()
        return render_template("index.html", map_html=map_html)

    @app.post("/points")
    def add_point():
        data = request.get_json()
        point = [float(data["lat"]), float(data["lng"])]
        clicked_points.append(point)
        return jsonify(point), 201

    @app.get("/points")
    def get_points():
        return jsonify(count = len(clicked_points) , points = clicked_points)
    
    app.run(debug = True)

main()

