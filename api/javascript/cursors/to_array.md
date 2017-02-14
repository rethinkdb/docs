---
layout: api-command
language: JavaScript
permalink: api/javascript/to_array/
command: toArray
io:
    -   - cursor
        - undefined
related_commands:
    next: next/
    each: each/
    close (cursor): close-cursor/
---

# Command syntax #

{% apibody %}
cursor.toArray(callback)
array.toArray(callback)
cursor.toArray() &rarr; promise
array.toArray() &rarr; promise
{% endapibody %}

# Description #

Retrieve all results and pass them as an array to the given callback.

_Note:_ Because a feed is a cursor that never terminates, calling `toArray` on a feed
will throw an error. See the [changes](/api/javascript/changes) command for more
information on feeds.

__Example:__ For small result sets it may be more convenient to process them at once as
an array.

```javascript
cursor.toArray(function(err, results) {
    if (err) throw err;
    processResults(results);
});
```

<!-- stop -->

The equivalent query with the `each` command would be:

```javascript
var results = []
cursor.each(function(err, row) {
    if (err) throw err;
    results.push(row);
}, function(err, results) {
    if (err) throw err;
    processResults(results);
});
```

An equivalent query using promises.

```javascript
cursor.toArray().then(function(results) {
    processResults(results);
}).error(console.log);
```

