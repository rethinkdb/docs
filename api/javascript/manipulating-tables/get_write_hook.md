---
layout: api-command
language: JavaScript
permalink: api/javascript/set_write_hook/
command: setWriteHook
io:
    -   - table
        - object
related_commands:
    setWriteHook: set_write_hook/
---

# Command syntax #

{% apibody %}
table.getWriteHook() &rarr; null/object
{% endapibody %}

# Description #

Get the write hook of this table. If a write hook exists the result is an object of the following form:

``` js
{
  "function": binary,
  "query": "setWriteHook(function(_var1, _var2, _var3) { return ...; })" ,
}
```

__Example:__ Get the write hook for the `comments` table.

```js
r.table('comments').getWriteHook().run(conn, callback)
```
