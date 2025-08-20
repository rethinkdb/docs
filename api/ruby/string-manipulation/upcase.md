---
layout: api-command
language: Ruby
permalink: api/ruby/upcase/
command: upcase
related_commands:
    downcase: downcase/
    match: match/
    split: split/
    format: format/
---

# Command syntax #

{% apibody %}
string.upcase() &rarr; string
{% endapibody %}

# Description #

Uppercases a string.

__Example:__

```rb
> r.expr("Sentence about LaTeX.").upcase().run(conn)
"SENTENCE ABOUT LATEX."
```

__Note:__ `upcase` and `downcase` only affect ASCII characters.
