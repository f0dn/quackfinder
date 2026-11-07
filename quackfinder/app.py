from flask import Flask
from map_utils import create_map, add_marker, add_line, add_route

app = Flask(__name__)

@app.route("/")
def display_map():
    # Create the map
    m = create_map(40.7128, -74.0060, 13)

    # Add markers
    add_marker(m, 40.7128, -74.0060)
    add_marker(m, 40.7306, -73.9352)

    # Add a line
    add_line(
        m,
        40.7128, -74.0060,
        40.7306, -73.9352,
        "Example Route"
    )

    # Flask directly returns the map
    return m.get_root().render()

if __name__ == "__main__":
    app.run(debug=True)