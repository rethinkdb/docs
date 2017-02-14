---
layout: api-command
language: JavaScript
permalink: api/javascript/concat_map/
command: concatMap
io:
    -   - sequence
        - stream
    -   - array
        - array
related_commands:
    map: map/
---

# Command syntax #

{% apibody %}
stream.concatMap(function) &rarr; stream
array.concatMap(function) &rarr; array
{% endapibody %}

# Description #

Concatenate one or more elements into a single sequence using a mapping function.

`concatMap` works in a similar fashion to [map](/api/javascript/map/), applying the given function to each element in a sequence, but it will always return a single sequence. If the mapping function returns a sequence, `map` would produce a sequence of sequences:

```javascript
r.expr([1, 2, 3]).map(function(x) { return [x, x.mul(2)] }).run(conn, callback)
```

Result:

```javascript
[[1, 2], [2, 4], [3, 6]]
```

Whereas `concatMap` with the same mapping function would merge those sequences into one:

```javascript
r.expr([1, 2, 3]).concatMap(function(x) { return [x, x.mul(2)] }).run(conn, callback)
```

Result:

```javascript
[1, 2, 2, 4, 3, 6]
```

The return value, array or stream, will be the same type as the input.

__Example:__ Construct a sequence of all monsters defeated by Marvel heroes. The field "defeatedMonsters" is an array of one or more monster names.

```javascript
r.table('marvel').concatMap(function(hero) {
    return hero('defeatedMonsters')
}).run(conn, callback)
```

__Example:__ Simulate an [eqJoin](/api/javascript/eq_join/) using `concatMap`. (This is how ReQL joins are implemented internally.)

```javascript
r.table("posts").concatMap(function(post) {
	return r.table("comments").getAll(
		post("id"),
		{ index:"postId" }
	).map(function(comment) {
		return { left: post, right: comment }
	})
}).run(conn, callback)
```
