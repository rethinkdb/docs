---
layout: api-command
language: Python
permalink: api/python/le/
command: '<=, le'
related_commands:
    '>, gt': gt/
    '<, lt': lt/
    '<=, le': le/
    '==, eq': eq/
    '!=, ne': ne/
---

# Command syntax #

{% apibody %}
value.le(value[, value, ...]) &rarr; bool
value <= value &rarr; bool
{% endapibody %}

# Description #

Compare values, testing if the left-hand value is less than or equal to the right-hand.

__Example:__ Test if a player has scored 10 points or less.

```py
r.table('players').get(1)['score'].le(10).run(conn)
# alternative syntax
(r.table('players').get(1)['score'] <= 10).run(conn)
```

__Example:__ Test if variables are ordered from highest to lowest.

```py
a = 20
b = 10
c = 15
r.le(a, b, c).run(conn)
```

This is the equivalent of the following:

```py
r.le(a, b).and(r.le(b, c)).run(conn)
```
