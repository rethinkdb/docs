---
layout: api-command
language: Java
permalink: api/java/limit/
command: limit
related_commands:
    skip: skip/
    slice: slice/
    nth: nth/
    orderBy: order_by/
---

# Command syntax #

{% apibody %}
sequence.limit(n) &rarr; stream
array.limit(n) &rarr; array
{% endapibody %}

# Description #


End the sequence after the given number of elements.

__Example:__ Only so many can fit in our Pantheon of heroes.

```java
r.table("marvel").orderBy("belovedness").limit(10).run(conn);
```


