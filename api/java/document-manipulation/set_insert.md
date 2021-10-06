---
layout: api-command
language: Java
permalink: api/java/set_insert/
command: setInsert
related_commands:
    difference: difference/
    setUnion: set_union/
    setIntersection: set_intersection/
    setDifference: set_difference/
    union: union/
---

# Command syntax #

{% apibody %}
array.setInsert(value) &rarr; array
{% endapibody %}

# Description #

Add a value to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```java
r.table("marvel").get("IronMan").g("equipment").setInsert("newBoots").run(conn);
```


