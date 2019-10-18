---
layout: api-command
language: Python
permalink: api/python/sample/
command: sample
---

# Command syntax #

{% apibody %}
sequence.sample(number) &rarr; selection
stream.sample(number) &rarr; array
array.sample(number) &rarr; array
{% endapibody %}

# Description #

Select a given number of elements from a sequence with uniform random distribution. Selection is done without replacement.

If the sequence has less than the requested number of elements (i.e., calling `sample(10)` on a sequence with only five elements), `sample` will return the entire sequence in a random order.

__Example:__ Select 3 random heroes.

```py
r.table('marvel').sample(3).run(conn)
```

__Example:__ Select and stratify 3 random heroes by belovedness.

```py
r.table('marvel').group('belovedness').sample(3).run(conn)
```
