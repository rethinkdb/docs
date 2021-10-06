---
layout: api-command
language: Python
permalink: api/python/limit/
command: limit
related_commands:
    order_by: order_by/
    skip: skip/
    'slice, []': slice/
    'nth, []': nth/
---

# Command syntax #

{% apibody %}
sequence.limit(n) &rarr; stream
array.limit(n) &rarr; array
{% endapibody %}

# Description #


End the sequence after the given number of elements.

__Example:__ Only so many can fit in our Pantheon of heroes.

```py
r.table('marvel').order_by('belovedness').limit(10).run(conn)
```
