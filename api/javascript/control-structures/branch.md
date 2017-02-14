---
layout: api-command
language: JavaScript
permalink: api/javascript/branch/
command: branch
io:
    -   - r
        - any
related_commands:
    do: do/
---

# Command syntax #

{% apibody %}
r.branch(test, true_action[, test2, test2_action, ...], false_action) &rarr; any
test.branch(true_action[, test2, test2_action, ...], false_action) &rarr; any
{% endapibody %}

# Description #

Perform a branching conditional equivalent to `if-then-else`.

The `branch` command takes 2n+1 arguments: pairs of conditional expressions and commands to be executed if the conditionals return any value but `false` or `null` (i.e., "truthy" values), with a final "else" command to be evaluated if all of the conditionals are `false` or `null`.

<!-- break -->

You may call `branch` infix style on the first test. (See the second example for an illustration.)

```javascript
r.branch(test1, val1, test2, val2, elseval)
```

is the equivalent of the JavaScript statement

```javascript
if (test1) {
    return val1;
} else if (test2) {
    return val2;
} else {
    return elseval;
}
```

__Example:__ Test the value of x.

```javascript
var x = 10;
r.branch(r.expr(x).gt(5), 'big', 'small').run(conn, callback);
// Result passed to callback
"big"
```

__Example:__ As above, infix-style.

```javascript
var x = 10;
r.expr(x).gt(5).branch('big', 'small').run(conn, callback);
// Result passed to callback
"big"
```

__Example:__ Categorize heroes by victory counts.

```javascript
r.table('marvel').map(
    r.branch(
        r.row('victories').gt(100),
        r.row('name').add(' is a superhero'),
        r.row('victories').gt(10),
        r.row('name').add(' is a hero'),
        r.row('name').add(' is very nice')
    )
).run(conn, callback);
```

If the documents in the table `marvel` are:

```javascript
[
    { name: "Iron Man", victories: 214 },
    { name: "Jubilee", victories: 49 },
    { name: "Slava", victories: 5 }
]
```

The results will be:

```javascript
[
    "Iron Man is a superhero",
    "Jubilee is a hero",
    "Slava is very nice"
]
```
