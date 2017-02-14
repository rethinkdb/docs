---
layout: api-command
language: JavaScript
permalink: api/javascript/get_intersecting/
command: getIntersecting
io:
    -   - table
        - stream
related_commands:
    getNearest: get_nearest/
---

# Command syntax #

{% apibody %}
table.getIntersecting(geometry, {index: 'indexname'}) &rarr; selection<stream>
{% endapibody %}

# Description #

Get all documents where the given geometry object intersects the geometry object of the requested geospatial index.

The `index` argument is mandatory. This command returns the same results as `table.filter(r.row('index').intersects(geometry))`. The total number of results is limited to the array size limit which defaults to 100,000, but can be changed with the `arrayLimit` option to [run](/api/javascript/run).

__Example:__ Which of the locations in a list of parks intersect `circle1`?

```javascript
var circle1 = r.circle([-117.220406,32.719464], 10, {unit: 'mi'});
r.table('parks').getIntersecting(circle1, {index: 'area'}).run(conn, callback);
```
