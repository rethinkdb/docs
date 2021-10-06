---
layout: api-command
language: Java
permalink: api/java/to_epoch_time/
command: toEpochTime
related_commands:
    now: now/
    time: time/
    toIso8601: to_iso8601/
---

# Command syntax #

{% apibody %}
time.toEpochTime() &rarr; number
{% endapibody %}

# Description #

Convert a time object to its epoch time.

__Example:__ Return the current time in seconds since the Unix Epoch with millisecond-precision.

```java
r.now().toEpochTime().run(conn);
```


