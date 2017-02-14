---
layout: api-command
language: JavaScript
permalink: api/javascript/max/
command: max
io:
    -   - sequence
        - value
related_commands:
    map: map/
    reduce: reduce/
    count: count/
    sum: sum/
    avg: avg/
    min: min/
    group: group/
---

# Command syntax #

{% apibody %}
sequence.max(field | function) &rarr; element
sequence.max({index: <indexname>}) &rarr; element
r.max(sequence, field | function) &rarr; element
r.max(sequence, {index: <indexname>}) &rarr; element
{% endapibody %}

# Description #

Finds the maximum element of a sequence.

The `max` command can be called with:

* a **field name**, to return the element of the sequence with the largest value in that field;
* an **index** (the primary key or a secondary index), to return the element of the sequence with the largest value in that index;
* a **function**, to apply the function to every element within the sequence and return the element which returns the largest value from the function, ignoring any elements where the function produces a non-existence error.

For more information on RethinkDB's sorting order, read the section in [ReQL data types](/docs/data-types/#sorting-order).

Calling `max` on an empty sequence will throw a non-existence error; this can be handled using the [default](/api/javascript/default/) command.

__Example:__ Return the maximum value in the list `[3, 5, 7]`.

```javascript
r.expr([3, 5, 7]).max().run(conn, callback);
```

__Example:__ Return the user who has scored the most points.

```javascript
r.table('users').max('points').run(conn, callback);
```

__Example:__ The same as above, but using a secondary index on the `points` field.

```javascript
r.table('users').max({index: 'points'}).run(conn, callback);
```

__Example:__ Return the user who has scored the most points, adding in bonus points from a separate field using a function.

```javascript
r.table('users').max(function(user) {
    return user('points').add(user('bonusPoints'));
}).run(conn, callback);
```

__Example:__ Return the highest number of points any user has ever scored. This returns the value of that `points` field, not a document.

```javascript
r.table('users').max('points')('points').run(conn, callback);
```

__Example:__ Return the user who has scored the most points, but add a default `null` return value to prevent an error if no user has ever scored points.

```javascript
r.table('users').max('points').default(null).run(conn, callback);
```
