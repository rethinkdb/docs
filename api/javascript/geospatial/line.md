---
layout: api-command
language: JavaScript
permalink: api/javascript/line/
command: line
io:
    -   - r
        - line
related_commands:
    point: point/
    polygon: polygon/
    circle: circle/
---
# Command syntax #

{% apibody %}
r.line([lon1, lat1], [lon2, lat2], ...) &rarr; line
r.line(point1, point2, ...) &rarr; line
{% endapibody %}

# Description #

Construct a geometry object of type Line. The line can be specified in one of two ways:

* Two or more two-item arrays, specifying latitude and longitude numbers of the line's vertices;
* Two or more [Point](/api/javascript/point) objects specifying the line's vertices.

<!-- break -->

Longitude (&minus;180 to 180) and latitude (&minus;90 to 90) of vertices are plotted on a perfect sphere. See [Geospatial support](/docs/geo-support/) for more information on ReQL's coordinate system.

__Example:__ Define a line.

```javascript
r.table('geo').insert({
    id: 101,
    route: r.line([-122.423246,37.779388], [-121.886420,37.329898])
}).run(conn, callback);
```

__Example:__ Define a line using an array of points.

You can use the [args](/api/javascript/args) command to pass an array of Point objects (or latitude-longitude pairs) to `line`.

```javascript
var route = [
    [-122.423246,37.779388],
    [-121.886420,37.329898]
];
r.table('geo').insert({
    id: 102,
    route: r.line(r.args(route))
}).run(conn, callback);
```
