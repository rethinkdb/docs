---
layout: api-command
language: Ruby
permalink: api/ruby/get_write_hook/
command: get_write_hook
related_commands:
    set_write_hook: set_write_hook/
---

# Command syntax #

{% apibody %}
table.get_write_hook() &rarr; null/object
{% endapibody %}

# Description #

Get the write hook of this table. If a write hook exists the result is an object of the following form:

```rb
{
  :function => <binary>,
  :query => "setWriteHook(function(_var1, _var2, _var3) { return ...; })"
}
```

__Example:__ Get the write hook for the `comments` table.

```py
r.table('comments').get_write_hook().run(conn)
```
