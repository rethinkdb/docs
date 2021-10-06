---
layout: api-command
language: Java
permalink: api/java/seconds/
command: seconds
related_commands:
    now: now/
    time: time/
    inTimezone: in_timezone/
---

# Command syntax #

{% apibody %}
time.seconds() &rarr; number
{% endapibody %}

# Description #

Return the seconds in a time object as a number between 0 and 59.999 (double precision).

__Example:__ Return the post submitted during the first 30 seconds of every minute.

```java
r.table("posts").filter(post -> post.g("date").seconds().lt(30)).run(conn);
```

