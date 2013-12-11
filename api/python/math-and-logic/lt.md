---
layout: api-command
language: Python
permalink: api/python/lt/
command: '<, lt'
related_commands:
    '>, gt': gt/
    '>=, ge': ge/
    '<=, le': le/
---

# Command syntax #

{% apibody %}
value < value &rarr; bool
value.lt(value) &rarr; bool
{% endapibody %}

# Description #

Test if the first value is less than other.

__Example:__ Is 2 less than 2?

```py
(r.expr(2) < 2).run(conn)
r.expr(2).lt(2).run(conn)
```

