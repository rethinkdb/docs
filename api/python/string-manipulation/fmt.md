---
layout: api-command
language: Python
permalink: api/python/fmt/
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

```py
r.fmt("{name} loves {candy}.", {
    "name": "Bob",
    "candy": "candy floss",
}).run(conn, callback)
```

Result:

```py
"Bob loves candy floss."
```
