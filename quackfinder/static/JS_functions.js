// JavaScript for the QuackFinder map. Flask serves this file at /static/JS_functions.js,
// and ClickReporter (in map_functions.py) adds it to the map page.
//
// Lets the user pick a start and end point by clicking the map.
// The first click places the start marker; every later click moves the end marker,
// so there are never more than 2 markers. Each click is also sent to Flask.
// Both markers can be dragged to a new spot, which is sent to Flask too.
// A dashed line connects the start and end markers and follows them as they move.
// A solid blue line shows the route between them. Python draws the first route when the
// page loads; after every click or drag, the route is fetched again from Flask.
//
// How the functions fit together:
//   setupClickReporter is the only function Python calls. It creates a "state" object
//   that holds everything the other functions need, then passes it to them:
//     state.map      - the Leaflet map object that folium created
//     state.url      - where to send points (Flask's "/points" routes)
//     state.routeUrl - where to get the route (Flask's "/calculate-route" route)
//     state.markers  - the marker objects; index 0 = start, index 1 = end
//     state.line     - the dashed line from the start marker to the end marker
//     state.route    - the solid route line


// Called from Python (ClickReporter). Sets everything up when the page loads.
//   map      - the Leaflet map object that folium created
//   points   - the points Flask already has saved, e.g. [[40.91, -73.12], [40.93, -73.14]]
//   url      - where to send each click (Flask's add_point route, "/points")
//   route    - the route Python already calculated, or [] if there isn't one yet
//   routeUrl - where to get a new route (Flask's calculate_route route, "/calculate-route")
function setupClickReporter(map, points, url, route, routeUrl) {
    const state = {
        map: map,
        url: url,
        routeUrl: routeUrl,
        markers: [],
        line: makeLine(map),
        route: makeRoute(map, route),
    };

    // draw the points Flask already has, and the line between them
    for (const point of points) {
        addMarker(state, point);
    }
    updateLine(state);

    // run handleClick every time the map is clicked
    map.on("click", function (e) {
        handleClick(state, e);
    });
}


// Runs on every map click.
// First or second click: add a new marker. After that: move the end marker.
function handleClick(state, e) {
    const point = e.latlng.wrap();

    if (state.markers.length < 2) {
        addMarker(state, point);
    } else {
        state.markers[1].setLatLng(point);
    }

    updateLine(state);
    // tell Flask about the click (handled by add_point in flask_test.py),
    // then get the new route once Flask has saved the point
    sendPoint(state.url, "POST", point).then(function () {
        drawRoute(state);
    });
}


// Creates a draggable marker and adds it to the map and to state.markers.
// The first marker made is the start (index 0), the second is the end (index 1).
function addMarker(state, latlng) {
    const index = state.markers.length;
    const marker = L.marker(latlng, {draggable: true})
        .bindTooltip(index === 0 ? "Start" : "End")
        .addTo(state.map);

    // runs over and over while the marker is being dragged, so the line follows it
    marker.on("drag", function () {
        updateLine(state);
    });

    // runs when the user lets go of the marker after dragging it
    marker.on("dragend", function () {
        // tell Flask this point moved (handled by move_point in flask_test.py),
        // then get the new route once Flask has saved the point
        sendPoint(state.url + "/" + index, "PUT", marker.getLatLng().wrap()).then(function () {
            drawRoute(state);
        });
    });

    state.markers.push(marker);
}


// Creates the start-to-end line. It starts empty, so nothing shows until there are 2 markers.
function makeLine(map) {
    return L.polyline([], {color: "#E4572E", weight: 4, dashArray: "8 8"}).addTo(map);
}


// Moves the line so it goes through the current marker positions.
function updateLine(state) {
    const positions = state.markers.map(function (marker) {
        return marker.getLatLng();
    });
    state.line.setLatLngs(positions);
}


// Creates the route line, starting with the route Python calculated (may be empty).
function makeRoute(map, route) {
    return L.polyline(route, {color: "#000DFF", weight: 5}).addTo(map);
}


// Asks Flask for the route (calculate_route in flask_test.py) and redraws the route line.
// Flask returns {"route": [[lat, lng], ...]}, which Leaflet can draw directly.
function drawRoute(state) {
    if (state.markers.length < 2) {
        return;
    }
    fetch(state.routeUrl)
        .then(function (res) {
            return res.ok ? res.json() : null;  // Flask sends 400 if it has fewer than 2 points
        })
        .then(function (data) {
            if (data) {
                state.route.setLatLngs(data.route);
            }
        })
        .catch(console.error);
}


// Sends a point to Flask as JSON, e.g. {"lat": 40.91, "lng": -73.12}.
// Returns a promise that finishes once Flask has answered.
//   url    - the Flask route to send it to
//   method - "POST" for a new click, "PUT" for a dragged marker
//   point  - a Leaflet LatLng (has .lat and .lng)
function sendPoint(url, method, point) {
    return fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({lat: point.lat, lng: point.lng}),
    }).catch(console.error);
}
