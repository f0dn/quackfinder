// JavaScript for the QuackFinder map. Flask serves this file at /static/JS_functions.js,
// and ClickReporter (in map_functions.py) adds it to the map page.

// Lets the user pick a start and end point by clicking the map.
// The first click places the start marker; every later click moves the end marker,
// so there are never more than 2 markers. Each click is also sent to Flask.
// Both markers can be dragged to a new spot, which is sent to Flask too.
//
//   map    - the Leaflet map object that folium created
//   points - the points Flask already has saved, e.g. [[40.91, -73.12], [40.93, -73.14]]
//   url    - where to send each click (Flask's add_point route, "/points")
function setupClickReporter(map, points, url) {
    // Creates a draggable marker. index 0 = start, index 1 = end.
    function makeMarker(latlng, index) {
        const marker = L.marker(latlng, {draggable: true})
            .bindTooltip(index === 0 ? "Start" : "End")
            .addTo(map);

        // runs when the user lets go of the marker after dragging it
        marker.on("dragend", function () {
            const p = marker.getLatLng().wrap();
            // tell Flask this point moved (handled by move_point in flask_test.py)
            fetch(url + "/" + index, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({lat: p.lat, lng: p.lng}),
            }).catch(console.error);
        });

        return marker;
    }

    // Draw the saved points and remember the marker objects so we can move them later
    const markers = points.map((p, i) => makeMarker(p, i));

    map.on("click", function (e) {
        const point = e.latlng.wrap();
        if (markers.length < 2) {
            // first or second click: add a new marker
            markers.push(makeMarker(point, markers.length));
        } else {
            // already 2 markers: move the end marker instead of adding one
            markers[1].setLatLng(point);
        }

        // send the clicked point to Flask (handled by add_point in flask_test.py)
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({lat: point.lat, lng: point.lng}),
        }).catch(console.error);
    });
}
