---
layout: api-command
language: Python
permalink: api/python/index_create/
command: index_create
related_commands:
    index_drop: index_drop/
    index_list: index_list/
---

# Command syntax #

{% apibody %}
table.index_create(index_name[, index_function]) &rarr; object
{% endapibody %}

# Description #

Create a new secondary index on this table.

__Example:__ To efficiently query our heroes by code name we have to create a secondary
index.

```py
r.table('dc').index_create('code_name').run(conn)
```


__Example:__ You can also create a secondary index based on an arbitrary function on the document.

```py
r.table('dc').index_create('power_rating',
    lambda hero: hero['combat_power'] + (2 * hero['compassion_power'])
    ).run(conn)
```


__Example:__ A compound index can be created by returning an array of values to use as
the secondary index key.

```py
r.table('dc').index_create('parental_planets',
    lambda hero: [hero['mothers_home_planet'], hero['fathers_home_planet']]
    ).run(conn)
```


__Example:__ A multi index can be created by passing an optional multi argument. Multi
index functions should return arrays and allow you to query based on whether a value
is present in the returned array. The example would allow us to get heroes who possess a
specific ability (the field 'abilities' is an array).

```py
r.table('dc').index_create('abilities', multi=True).run(conn)
```

__Example:__ The above can be combined to create a multi index on a function that
returns an array of values.

```py
r.table('dc').index_create('parental_planets',
    lambda hero: [hero['mothers_home_planet'], hero['fathers_home_planet']],
    multi=True).run(conn)
```
