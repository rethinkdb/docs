---
layout: api-command
language: Java
permalink: api/java/hours/
command: hours
related_commands:
    now: now/
    time: time/
    inTimezone: in_timezone/
---

# Command syntax #

{% apibody %}
time.hours() &rarr; number
{% endapibody %}

# Description #

Return the hour in a time object as a number between 0 and 23.

__Example:__ Return all the posts submitted after midnight and before 4am.

```java
r.table("posts").filter(post -> post.g("date").hours().lt(4)).run(conn);
```

