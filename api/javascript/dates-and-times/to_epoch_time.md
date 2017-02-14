---
layout: api-command
language: JavaScript
permalink: api/javascript/to_epoch_time/
command: toEpochTime
io:
    -   - time
        - number
related_commands:
    now: now/
    time: time/
---

# Command syntax #

{% apibody %}
time.toEpochTime() &rarr; number
{% endapibody %}

# Description #

Convert a time object to its epoch time.

__Example:__ Return the current time in seconds since the Unix Epoch with millisecond-precision.

```javascript
r.now().toEpochTime()
```


