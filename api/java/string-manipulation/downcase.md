---
layout: api-command
language: Java
permalink: api/java/downcase/
command: downcase
related_commands:
    upcase: upcase/
    match: match/
    split: split/
---

# Command syntax #

{% apibody %}
string.downcase() &rarr; string
{% endapibody %}

# Description #

Lowercase a string.

__Example:__

```java
r.expr("Sentence about LaTeX.").downcase().run(conn);
```

Result:

```java
"sentence about latex."
```

__Note:__ `upcase` and `downcase` only affect ASCII characters.
