---
layout: api-command
language: JavaScript
permalink: api/javascript/sum/
command: sum
io:
    -   - sequence
        - number
related_commands:
    map: map/
    reduce: reduce/
    count: count/
    avg: avg/
    min: min/
    max: max/
    group: group/
---

# Command syntax #

{% apibody %}
sequence.sum([field | function]) &rarr; number
r.sum(sequence, [field | function]) &rarr; number
{% endapibody %}

# Description #

Sums all the elements of a sequence.  If called with a field name,
sums all the values of that field in the sequence, skipping elements
of the sequence that lack that field.  If called with a function,
calls that function on every element of the sequence and sums the
results, skipping elements of the sequence where that function returns
`null` or a non-existence error.

Returns `0` when called on an empty sequence.

__Example:__ What's 3 + 5 + 7?

```javascript
r.expr([3, 5, 7]).sum().run(conn, callback)
```

__Example:__ How many points have been scored across all games?

```javascript
r.table('games').sum('points').run(conn, callback)
```

__Example:__ How many points have been scored across all games,
counting bonus points?

```javascript
r.table('games').sum(function(game) {
    return game('points').add(game('bonus_points'))
}).run(conn, callback)
```
