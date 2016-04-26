---
layout: api-command
language: JavaScript
permalink: api/javascript/close-cursor/
command: close
io:
    -   - cursor
        - undefined
related_commands:
    next: next/
    toArray: to_array/
    each: each/
---

# Command syntax #

{% apibody %}
cursor.close()
{% endapibody %}

# Description #


Close a cursor. Closing a cursor cancels the corresponding query and frees the memory
associated with the open request. It has both a callback and promise method of continuing when it is called.

__Example:__ Close a cursor.

```js
cursor.close()
```
