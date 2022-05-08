---
layout: api-command
language: Java
permalink: api/java/fmt/
command: fmt
io:
    -   - r
        - string
related_commands:
    match: match/
    split: split/
    upcase: upcase/
    downcase: downcase/
---

# Command syntax #

{% apibody %}
r.fmt(string, object) &rarr; string
{% endapibody %}

# Description #

Formats a template string based on a string-string key-value object.

__Example:__

```java
r.fmt("{name} loves {candy}.",
    r.hashMap("name", "Bob").with("candy", "candy floss")
).run(conn, callback)
```

Result:

```java
"Bob loves candy floss."
```
