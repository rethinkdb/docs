---
layout: api-command
language: Python
permalink: api/python/close-cursor/
command: close
related_commands:
    next: next/
    list: to_array/
    each: each/
---

# Command syntax #

{% apibody %}
cursor.close()
{% endapibody %}

# Description #


Close a cursor. Closing a cursor cancels the corresponding query and frees the memory
associated with the open request.

__Example:__ Close a cursor.

```py
cursor.close()
```
