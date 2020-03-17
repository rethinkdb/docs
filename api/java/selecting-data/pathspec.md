---
layout: api-command
language: Java
permalink: api/java/pathspec/
command: pathspec
related_commands:
    object: object/
    filter: filter/
py: false
js: false
rb: false
---

# Command syntax #

{% apibody %}
r.pathspec(key[, keys...], value) &rarr; object
{% endapibody %}

# Description #

Creates an object with the multiple keys as a stacked structure, where the keys must
be strings.  `r.pathspec(A, B, C, D)` is equivalent to
`r.expr({ A: { B: { C: D } } })`.

__Example:__ Create a stacked structure.

```java
r.pathspec("x", "y", "z", "bar")

// Result:
{ "x": { "y": { "z": "bar" } }}
```

__Example:__ Filter table by a really deep structure.

```java
r.table("match_victories").filter(
    r.pathspec("stats", "blue_team", "points", 10)
)

// Filter argument:
{ "stats": { "blue_team": { "points": 10 } } }
```

__Example:__ Filter table by a structure that is deep both in depth and breadth.

```java
r.table("shows").filter(
    r.pathspec("available_on", r.object(
        "broadcast", r.pathspec("global", "ESPN"),
        "online", r.pathspec("free", "YouTube")
    ))
)

// Filter argument:
{ "available_on": { "broadcast": { "global": "ESPN" }, "online": { "free": "YouTube" } } }
```


