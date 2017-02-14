---
layout: api-command
language: JavaScript
permalink: api/javascript/day_of_year/
command: dayOfYear
io:
    -   - time
        - number
related_commands:
    now: now/
    time: time/
---

# Command syntax #

{% apibody %}
time.dayOfYear() &rarr; number
{% endapibody %}

# Description #

Return the day of the year of a time object as a number between 1 and 366 (following ISO 8601 standard).

__Example:__ Retrieve all the users who were born the first day of a year.

```javascript
r.table("users").filter(
    r.row("birthdate").dayOfYear().eq(1)
)
```


