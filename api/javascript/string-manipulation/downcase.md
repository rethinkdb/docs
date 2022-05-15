---
layout: api-command
language: JavaScript
permalink: api/javascript/downcase/
command: downcase
io:
    -   - string
        - string
related_commands:
    upcase: upcase/
    match: match/
    split: split/
    fmt: fmt/
---

# Command syntax #

{% apibody %}
string.downcase() &rarr; string
{% endapibody %}

# Description #

Lowercases a string.

__Example:__

```js
r.expr("Sentence about LaTeX.").downcase().run(conn, callback)
```

Result:

```js
"sentence about latex."
```

__Note:__ `upcase` and `downcase` only affect ASCII characters.
