---
layout: api-command 
language: Python
permalink: api/python/zip/
command: zip 
related_commands:
    eq_join: eq_join/
    inner_join: inner_join/
    outer_join: outer_join/
---

# Command syntax #

{% apibody %}
stream.zip() &rarr; stream
array.zip() &rarr; array
{% endapibody %}

# Description #

Used to 'zip' up the result of a join by merging the 'right' fields into 'left' fields of each member of the sequence.

__Example:__ 'zips up' the sequence by merging the left and right fields produced by a join.

```py
r.table('marvel').eq_join('main_dc_collaborator', r.table('dc')).zip().run(conn)
```
