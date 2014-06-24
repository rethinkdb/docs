---
layout: api-command
language: Python
permalink: api/python/upcase/
command: upcase
related_commands:
    downcase: downcase/
    match: match/
    split: split/
---

# Command syntax #

{% apibody %}
string.upcase() &rarr; string
{% endapibody %}

# Description #

Upcases a string.

__Example:__

```py
r.expr("Sentence about LaTeX.").upcase().run(conn)
```

Result:

```py
"SENTENCE ABOUT LATEX."
```
