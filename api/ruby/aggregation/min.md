---
layout: api-command
language: Ruby
permalink: api/ruby/min/
command: min
related_commands:
    map: map/
    reduce: reduce/
    count: count/
    sum: sum/
    avg: avg/
    max: max/
    group: group/
---

# Command syntax #

{% apibody %}
sequence.min(field | function) &rarr; element
sequence.min({:index => <indexname>}) &rarr; element
r.min(sequence, field | function) &rarr; element
r.min(sequence, {:index => <indexname>}) &rarr; element
{% endapibody %}

# Description #

Finds the minimum element of a sequence.

The `min` command can be called with:

* a **field name**, to return the element of the sequence with the smallest value in that field;
* an **index** (the primary key or a secondary index), to return the element of the sequence with the smallest value in that index;
* a **function**, to apply the function to every element within the sequence and return the element which returns the smallest value from the function, ignoring any elements where the function produces a non-existence error.

For more information on RethinkDB's sorting order, read the section in [ReQL data types](/docs/data-types/#sorting-order).

Calling `min` on an empty sequence will throw a non-existence error; this can be handled using the [default](/api/ruby/default/) command.

__Example:__ Return the minimum value in the list `[3, 5, 7]`.

```rb
r([3, 5, 7]).min().run(conn)
```

__Example:__ Return the user who has scored the fewest points.

```rb
r.table('users').min('points').run(conn)
```

__Example:__ The same as above, but using a secondary index on the `points` field.

```rb
r.table('users').min({:index => 'points'}).run(conn)
```

__Example:__ Return the user who has scored the fewest points, adding in bonus points from a separate field using a function.

```rb
r.table('users').min{|user| user['points'] + user['bonus_points']}.run(conn)
```

__Example:__ Return the smallest number of points any user has ever scored. This returns the value of that `points` field, not a document.

```rb
r.table('users').min('points')['points'].run(conn)
```

__Example:__ Return the user who has scored the fewest points, but add a default `nil` return value to prevent an error if no user has ever scored points.

```rb
r.table('users').min('points').default(nil).run(conn)
```
