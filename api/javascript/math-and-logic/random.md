---
layout: api-command
language: JavaScript
permalink: api/javascript/random/
command: random
related_commands:
    'sample': sample/
---

# Command syntax #

{% apibody %}
r.random() &rarr number
r.random(integer) &rarr integer
r.random(integer, integer) &rarr integer
r.random(number, number, {float: true}) &rarr number
{% endapibody %}

# Description #

Generate a random number between the given bounds. If no arguments are given, the result
will be a floating-point number in the range `[0,1)`.

When passing a single argument, `r.random(x)`, the result will be in the range `[0,x)`,
and when passing two arguments, `r.random(x,y)`, the range is `[x,y)`. If `x` and `y` are
equal, an error will occur, unless generating a floating-point number, for which `x` will
be returned.

Note: The last argument given will always be the 'open' side of the range, but when
generating a floating-point number, the 'open' side may be less than the 'closed' side.

__Example:__ Generate a random number in the range `[0,1)`

```js
r.random().run(conn, callback)
```


__Example:__ Generate a random integer in the range `[0,100)`

```js
r.random(100).run(conn, callback)
r.random(0, 100).run(conn, callback)
```


__Example:__ Generate a random number in the range `(-2.24,1.59]`

```js
r.random(1.59, -2.24, {float: true}).run(conn, callback)
```

