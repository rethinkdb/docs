---
layout: api-command
language: Python
permalink: api/python/inner_join/
command: inner_join
related_commands:
    eq_join: eq_join/
    outer_join: outer_join/
    zip: zip/
---

# Command syntax #

{% apibody %}
sequence.inner_join(other_sequence, predicate) &rarr; stream
array.inner_join(other_sequence, predicate) &rarr; array
{% endapibody %}

# Description #

Returns the inner product of two sequences (e.g. a table, a filter result) filtered by
the predicate. The query compares each row of the left sequence with each row of the
right sequence to find all pairs of rows which satisfy the predicate. When the predicate
is satisfied, each matched pair of rows of both sequences are combined into a result row.

__Example:__ Construct a sequence of documents containing all cross-universe matchups where a marvel hero would lose.

```py
r.table('marvel').inner_join(
    r.table('dc'),
    lambda marvelRow, dcRow: marvelRow['strength'] < dcRow['strength']
).run(conn)
```
