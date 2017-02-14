---
layout: api-command
language: JavaScript
permalink: api/javascript/avg/
command: avg
io:
    -   - sequence
        - number
related_commands:
    map: map/
    reduce: reduce/
    count: count/
    sum: sum/
    min: min/
    max: max/
    group: group/
---

# Command syntax #

{% apibody %}
sequence.avg([field | function]) &rarr; number
r.avg(sequence, [field | function]) &rarr; number
{% endapibody %}

# Description #

Averages all the elements of a sequence.  If called with a field name,
averages all the values of that field in the sequence, skipping
elements of the sequence that lack that field.  If called with a
function, calls that function on every element of the sequence and
averages the results, skipping elements of the sequence where that
function returns `null` or a non-existence error.

Produces a non-existence error when called on an empty sequence.  You
can handle this case with `default`.

__Example:__ What's the average of 3, 5, and 7?

```javascript
r.expr([3, 5, 7]).avg().run(conn, callback)
```

__Example:__ What's the average number of points scored in a game?

```javascript
r.table('games').avg('points').run(conn, callback)
```

__Example:__ What's the average number of points scored in a game,
counting bonus points?

```javascript
r.table('games').avg(function(game) {
    return game('points').add(game('bonus_points'))
}).run(conn, callback)
```

__Example:__ What's the average number of points scored in a game?
(But return `null` instead of raising an error if there are no games where
points have been scored.)

```javascript
r.table('games').avg('points').default(null).run(conn, callback)
```
