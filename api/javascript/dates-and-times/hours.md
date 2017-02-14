---
layout: api-command
language: JavaScript
permalink: api/javascript/hours/
command: hours
io:
    -   - time
        - number
related_commands:
    now: now/
    time: time/
---

# Command syntax #

{% apibody %}
time.hours() &rarr; number
{% endapibody %}

# Description #

Return the hour in a time object as a number between 0 and 23.

__Example:__ Return all the posts submitted after midnight and before 4am.

```javascript
r.table("posts").filter(function(post) {
    return post("date").hours().lt(4)
})
```

