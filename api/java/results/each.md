---
layout: api-command
language: Java
permalink: api/java/each/
command: forEach
related_commands:
    next: next/
    toList: to_array/
    close (result): close-cursor/
---

# Command syntax #

{% apibody %}
result.forEach(doc -> { ... })
{% endapibody %}

# Description #

Lazily iterate over a result set one element at a time.

RethinkDB results can be iterated through via the Java [Iterable][i1] and [Iterator][i2] interfaces; use standard Java commands like `for` loops to access each item in the sequence.

[i1]: https://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html
[i2]: https://docs.oracle.com/javase/8/docs/api/java/util/Iterator.html


__Example:__ Let's process all the elements!

```java
try (Result<Object> result = r.table("users").run(conn)) {
    result.forEach(doc -> { System.out.println(doc); });
}
```

__Example:__ Stop the iteration prematurely.

```java
try (Result<Object> result = r.table("users").run(conn)) {
    for (Object doc: result) {
        if (!processRow(doc)) {
            break;
        }
    }
}
```
