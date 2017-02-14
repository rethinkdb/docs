---
layout: api-command
language: JavaScript
permalink: api/javascript/change_at/
command: changeAt
io:
    -   - array
        - array
related_commands:
    insertAt: insert_at/
    spliceAt: splice_at/
    deleteAt: delete_at/
---

# Command syntax #

{% apibody %}
array.changeAt(offset, value) &rarr; array
{% endapibody %}

# Description #

Change a value in an array at a given index. Returns the modified array.

__Example:__ Bruce Banner hulks out.

```javascript
r.expr(["Iron Man", "Bruce", "Spider-Man"]).changeAt(1, "Hulk").run(conn, callback)
```
