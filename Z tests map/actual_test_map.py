import folium
from map_functions import *
import http.server
import socketserver
import webbrowser
import threading
def main():
    coordinates = [
        [40.9153, -73.1231],
        [40.917238, -73.124638],
        [40.9135, -73.1260]
    ]
    map = create_map(40.9153, -73.1231, 20)

    add_route(map, coordinates)
    User_Markers(map)
    save_map(map, "test") #saved as test.html

    
    port = 8000

    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer(("", port), handler)

    threading.Thread(
        target=server.serve_forever,
        daemon=True
    ).start()

    # Open the map automatically
    webbrowser.open(f"http://localhost:{port}/test.html")

    input("Press Enter to stop the server...")
    server.shutdown()
    server.server_close()


main()


