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
result.close()
{% endapibody %}

# Description #


Close a result. Closing a result cancels the corresponding query and frees the memory
associated with the open request.

__Example:__ Close a result.

```java
result.close();
```
