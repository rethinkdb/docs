---
layout: api-command
language: JavaScript
permalink: api/javascript/intersects/
command: intersects
io:
    -   - geometry
        - bool
    -   - sequence
        - sequence
related_commands:
    includes: includes/
    getIntersecting: get_intersecting/
---
# Command syntax #

{% apibody %}
sequence.intersects(geometry) &rarr; sequence
geometry.intersects(geometry) &rarr; bool
r.intersects(sequence, geometry) &rarr; sequence
r.intersects(geometry, geometry) &rarr; bool
{% endapibody %}

# Description #

Tests whether two geometry objects intersect with one another. When applied to a sequence of geometry objects, `intersects` acts as a [filter](/api/javascript/filter), returning a sequence of objects from the sequence that intersect with the argument.

__Example:__ Is `point2` within a 2000-meter circle around `point1`?

```javascript
var point1 = r.point(-117.220406,32.719464);
var point2 = r.point(-117.206201,32.725186);
r.circle(point1, 2000).intersects(point2).run(conn, callback);
// result returned to callback 
true
```

__Example:__ Which of the locations in a list of parks intersect `circle1`?

```javascript
var circle1 = r.circle([-117.220406,32.719464], 10, {unit: 'mi'});
r.table('parks')('area').intersects(circle1).run(conn, callback);
```

{% infobox %}
The `intersects` command cannot take advantage of a geospatial [secondary index](/docs/secondary-indexes/javascript). If you're working with large data sets, you should consider using an index and the [getIntersecting](/api/javascript/get_intersecting) command instead of `intersects`.
{% endinfobox %}
