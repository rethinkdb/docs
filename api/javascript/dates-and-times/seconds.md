---
layout: api-command
language: JavaScript
permalink: api/javascript/seconds/
command: seconds
io:
    -   - time
        - number
related_commands:
    now: now/
    time: time/
---

# Command syntax #

{% apibody %}
time.seconds() &rarr; number
{% endapibody %}

# Description #

Return the seconds in a time object as a number between 0 and 59.999 (double precision).

__Example:__ Return the post submitted during the first 30 seconds of every minute.

```javascript
r.table("posts").filter(function(post) {
    return post("date").seconds().lt(30)
})
```

