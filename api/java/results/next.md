---
layout: api-command
language: Java
permalink: api/java/next/
command: next
related_commands:
    for: each/
    toList: to_array/
    close (result): close-cursor/
---

# Command syntax #

{% apibody %}
result.next([timeout, unit])
{% endapibody %}

# Description #

Get the next element in the result.

If the optional arguments are supplied, waits up to the specified number of seconds for data to be available before raising `TimeoutException`.

Calling `next` the first time on a result provides the first element of the result. If the data set is exhausted (e.g., you have retrieved all the documents in a table), a `NoSuchElementException` error will be raised when `next` is called.

__Example:__ Retrieve the next element.

```java
Result<Object> result = r.table("superheroes").run(conn);
Object doc = result.next();
```

__Example:__ Retrieve the next element on a [changefeed](/docs/changefeeds/java), waiting up to five seconds.

```java
Result<Object> result = r.table("superheroes").changes().run(conn);
Object doc = result.next(5L, TimeUnit.SECONDS);
```

__Note:__ RethinkDB results can be iterated through via the Java [Iterable][i1] and [Iterator][i2] interfaces. The canonical way to retrieve all the results is to use a [for][] loop or [toList][].

[i1]: https://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html
[i2]: https://docs.oracle.com/javase/8/docs/api/java/util/Iterator.html
[for]: /api/java/each
[toList]: /api/java/to_array
