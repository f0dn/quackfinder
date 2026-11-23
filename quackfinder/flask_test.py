from flask import *
from quackfinder.map_functions import *

def test_distras(coords: list[list[float]]):
    start = coords[0]
    destination = coords[1]

    middle = [start[0], destination[1]]

    return [start, middle, destination]


def main():
    app = Flask(__name__)
    clicked_points  = []

    @app.route("/")
    def home():
        map = create_map(40.9153, -73.1231, 20)

        # draw the route right away if both points are already picked;
        # after this, the JavaScript keeps it updated using /calculate-route
        route = test_distras(clicked_points) if len(clicked_points) == 2 else []
        ClickReporter(points=clicked_points, route=route).add_to(map)
        map_html = map.get_root().render()
        return render_template("index.html", map_html=map_html)
        


    @app.post("/points")
    def add_point():
        data = request.get_json()
        point = [float(data["lat"]), float(data["lng"])]
        if len(clicked_points) < 2:
            clicked_points.append(point)   # start point, then end point
        else:
            clicked_points[1] = point      # replace the end point
        
        print_points(clicked_points)
        
        return jsonify(point), 201

    # Called when a marker is dragged: PUT /points/0 moves the start, PUT /points/1 moves the end
    @app.put("/points/<int:index>")
    def move_point(index):
        if index >= len(clicked_points):
            return jsonify(error = "no such point"), 404
        data = request.get_json()
        clicked_points[index] = [float(data["lat"]), float(data["lng"])]

        print_points(clicked_points)

        return jsonify(clicked_points[index]), 200

    @app.get("/points")
    def get_points():
        return jsonify(count = len(clicked_points) , points = clicked_points)

    @app.get("/calculate-route")
    def calculate_route():

        if len(clicked_points) < 2:
            return jsonify(
                error="Two points are required"
            ), 400

        route = test_distras(clicked_points)

        return jsonify({
            "route": route
        })
    return app
    app.run(debug = True)


if __name__ == "__main__":
    main()

