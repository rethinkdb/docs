---
layout: api-command
language: Java
permalink: api/java/to_array/
command: toList
related_commands:
    next: next/
    for: each/
    close (result): close-cursor/
---

# Command syntax #

{% apibody %}
result.toList() &rarr; List
{% endapibody %}

# Description #

Retrieve all results from a result as a list.

RethinkDB results can be iterated through via the Java [Iterable][i1] and [Iterator][i2] interfaces; to coerce a result into a list, use `toList`.

[i1]: https://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html
[i2]: https://docs.oracle.com/javase/8/docs/api/java/util/Iterator.html
[for]: /api/java/each
[toList]: /api/java/to_array

__Example:__ For small result sets it may be more convenient to process them at once as a list.

```java
processResults(r.table("users").run(conn).toList());
```

<!-- stop -->

The equivalent query with a `for` loop would be:

```java
try(Result<Object> result = r.table("users").run(conn)) {
    for (Object doc : result) {
        processResult(doc);
    }
}
```

__Note:__ Because a feed is a result that never terminates, using `list` with a feed will never return. Use [for](../each/) or [next](../next/) instead. See the [changes](/api/java/changes) command for more information on feeds.
