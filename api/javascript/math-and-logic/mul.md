---
layout: api-command
language: JavaScript
permalink: api/javascript/mul/
command: mul
io:
    -   - number
        - number
    -   - array
        - array
related_commands:
    add: add/
    sub: sub/
    div: div/
    mod: mod/
---

# Command syntax #

{% apibody %}
number.mul(number[, number, ...]) &rarr; number
array.mul(number[, number, ...]) &rarr; array
{% endapibody %}

# Description #

Multiply two numbers, or make a periodic array.

__Example:__ It's as easy as 2 * 2 = 4.

```javascript
r.expr(2).mul(2).run(conn, callback)
```

__Example:__ Arrays can be multiplied by numbers as well.

```javascript
r.expr(["This", "is", "the", "song", "that", "never", "ends."]).mul(100).run(conn, callback)
```

