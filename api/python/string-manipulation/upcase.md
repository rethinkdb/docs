---
layout: api-command
language: Python
permalink: api/python/upcase/
command: upcase
related_commands:
    downcase: downcase/
    match: match/
    split: split/
    fmt: fmt/
---

# Command syntax #

{% apibody %}
string.upcase() &rarr; string
{% endapibody %}

# Description #

Uppercases a string.

__Example:__

```py
> r.expr("Sentence about LaTeX.").upcase().run(conn)
"SENTENCE ABOUT LATEX."
```

__Note:__ `upcase` and `downcase` only affect ASCII characters.
