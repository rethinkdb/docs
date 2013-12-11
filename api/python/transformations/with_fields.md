---
layout: api-command
language: Python
permalink: api/python/with_fields/
command: with_fields
related_commands:
    has_fields: has_fields/
    pluck: pluck/
    without: without/
---

# Command syntax #

{% apibody %}
sequence.with_fields([selector1, selector2...]) &rarr; stream
array.with_fields([selector1, selector2...]) &rarr; array
{% endapibody %}

# Description #

Takes a sequence of objects and a list of fields. If any objects in the sequence don't
have all of the specified fields, they're dropped from the sequence. The remaining
objects have the specified fields plucked out. (This is identical to `has_fields`
followed by `pluck` on a sequence.)

__Example:__ Get a list of heroes and their nemeses, excluding any heroes that lack one.

```py
r.table('marvel').with_fields('id', 'nemesis')
```

__Example:__ Get a list of heroes and their nemeses, excluding any heroes whose nemesis isn't in an evil organization.

```py
r.table('marvel').with_fields('id', {'nemesis' : {'evil_organization' : True}})
```


__Example:__ The nested syntax can quickly become overly verbose so there's a shorthand.

```py
r.table('marvel').with_fields('id', {'nemesis' : 'evil_organization'})
```

