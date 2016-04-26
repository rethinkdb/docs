---
layout: api-command
language: Python
permalink: api/python/close-cursor/
command: close
---

# Command syntax #

{% apibody %}
cursor.close()
{% endapibody %}

# Description #


Close a cursor. Closing a cursor cancels the corresponding query and frees the memory
associated with the open request. It has both a callback and promise method of continuing when it is called.

__Example:__ Close a cursor.

```py
cursor.close()
```
