---
layout: api-command
language: Ruby
permalink: api/ruby/ge/
command: '>=, ge'
related_commands:
    '>, gt': gt/
    '<, lt' : lt/
    '<=, le': le/
    '==, eq': eq/
    '!=, ne': ne/
---

# Command syntax #

{% apibody %}
value.ge(value[, value, ...]) &rarr; bool
value >= value &rarr; bool
{% endapibody %}

# Description #

Compare values, testing if the left-hand value is greater than or equal to the right-hand.

__Example:__ Test if a player has scored 10 points or more.

```rb
r.table('players').get(1)['score'].ge(10).run(conn)
# alternative syntax
(r.table('players').get(1)['score'] >= 10).run(conn)
```

__Example:__ Test if variables are ordered from lowest to highest.

```rb
a = 10
b = 20
c = 15
r.ge(a, b, c).run(conn)
```

This is the equivalent of the following:

```rb
r.ge(a, b).and(r.ge(b, c)).run(conn)
```
