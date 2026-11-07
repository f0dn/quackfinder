from flask import Flask, render_template, request, jsonify
import folium

app = Flask(__name__)
clicked_points = []

@app.route("/")
def home():
    # Create the map
    map = folium.Map(
        location=[40.9153, -73.1231],
        zoom_start=15
    )

    # Define route coordinates
    coordinates = [
        [40.9153, -73.1231],
        [40.917238, -73.124638],
        [40.9135, -73.1260]
    ]

    # Draw route using a PolyLine
    folium.PolyLine(
        locations=coordinates,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(map)

    # Add markers for previously clicked points
    for lat, lng in clicked_points:
        folium.Marker(
            location=[lat, lng],
            popup=f"Clicked Point: {lat}, {lng}",
            icon=folium.Icon(color="red")
        ).add_to(map)

    # Render map HTML
    map_html = map._repr_html_()

    return map.get_root().render()

@app.post("/points")
def add_point():
    data = request.get_json()

    if not data or "lat" not in data or "lng" not in data:
        return jsonify({"error": "Missing coordinates"}), 400

    try:
        lat = float(data["lat"])
        lng = float(data["lng"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid coordinates"}), 400

    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        return jsonify({"error": "Coordinates out of range"}), 400

    point = [lat, lng]
    clicked_points.append(point)

    return jsonify(point), 201

@app.get("/points")
def get_points():
    return jsonify(
        count=len(clicked_points),
        points=clicked_points
    )

if __name__ == "__main__":
    app.run(debug=True)