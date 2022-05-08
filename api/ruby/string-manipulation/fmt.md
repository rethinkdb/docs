---
layout: api-command
language: Ruby
permalink: api/ruby/fmt/
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

```rb
r.fmt("{name} loves {candy}.", {
    "name" => "Bob",
    "candy" => "candy floss",
}).run(conn, callback)
```

Result:

```rb
"Bob loves candy floss."
```
