---
layout: api-command
language: JavaScript
permalink: api/javascript/do/
command: do
io:
    -   - any
        - any
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

```js
r.table('players').get('f19b5f16-ef14-468f-bd48-e194761df255').do(
    function (player) {
        return player('gross_score').sub(player('course_handicap'));
    }
).run(conn, callback);
```

__Example:__ Return the best scoring player in a two-player golf match.

```js
r.do(r.table('players').get(id1), r.table('players').get(id2),
    function (player1, player2) {
        return r.branch(player1('gross_score').lt(player2('gross_score')),
            player1, player2);
    }
).run(conn, callback);
```

Note that `branch`, the ReQL conditional command, must be used instead of `if`. See the `branch` [documentation](/api/javascript/branch) for more.
