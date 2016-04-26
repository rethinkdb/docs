---
layout: api-command
language: Java
permalink: api/java/close-cursor/
command: close
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

```java
cursor.close();
```
