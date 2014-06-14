---
layout: api-command
language: Python
permalink: api/python/args/
command: args
---

# Command syntax #

{% apibody %}
r.args(array) &rarr; special
{% endapibody %}

# Description #

`r.args` is a special term that's used to splice an array of arguments
into another term.  This is useful when you want to call a variadic
term such as `get_all` with a set of arguments produced at runtime.

This is analagous to unpacking argument lists in Python.

__Example:__ Get Alice and Bob from the table `people`.

```py
r.table('people').get_all('Alice', 'Bob').run(conn)
# or
r.table('people').get_all(r.args(['Alice', 'Bob'])).run(conn)
```

__Example:__ Get all of Alice's children from the table `people`.

```py
# r.table('people').get('Alice') returns {'id': 'Alice', 'children': ['Bob', 'Carol']}
r.table('people').get_all(r.args(r.table('people').get('Alice')['children'])).run(conn)
```
