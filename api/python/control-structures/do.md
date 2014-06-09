---
layout: api-command
language: Python
permalink: api/python/do/
command: do
---

# Command syntax #

{% apibody %}
any.do(function) &rarr; any
r.do([args]*, function) &rarr; any
any.do(expr) &rarr; any
r.do([args]*, expr) &rarr; any
{% endapibody %}

# Description #

Evaluate an expression and pass its values as arguments to a function or to an expression.

The last argument to `do` (or, in some forms, the only argument) is an expression or an anonymous function which receives values from either the previous arguments or from prefixed commands chained before `do`. A common use, for example, would be to retrieve a document with `get` and pass it to a function via `do`. The type of `do`'s result is the type of the value returned from the function or last expression.

__Example:__ Compute a golfer's net score for a game.

```py
r.table('players').get('86be93eb-a112-48f5-a829-15b2cb49de1d').do(
    lambda player: player['gross_score'] - player['course_handicap']
).run(conn)
```

__Example:__ Return the name of the best scoring player in a two-player golf match.

```py
r.do(r.table('players').get(id1), r.table('players').get(id2),
    (lambda player1, player2:
        r.branch(player1['gross_score'].lt(player2['gross_score']),
        player1, player2))
).run(conn)

```

Note that `branch`, the ReQL conditional command, must be used instead of `if`. See the `branch` [documentation](/api/python/branch) for more.
