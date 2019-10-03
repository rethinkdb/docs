---
layout: api-command
language: JavaScript
permalink: api/javascript/set_write_hook/
command: setWriteHook
io:
    -   - table
        - object
related_commands:
    getWriteHook: get_write_hook/
---

# Command syntax #

{% apibody %}
table.setWriteHook(function) &rarr; object
table.setWriteHook(binary) &rarr; object
table.setWriteHook(null) &rarr; object
{% endapibody %}

# Description #

Sets the write hook on a table or overwrites it if one already exists.

The `function` can be an anonymous function with the signature `(context: object, oldVal: object, newVal: object) -> object` or a binary representation obtained from the `function` field of [getWriteHook](/api/javascript/get_write_hook). The function must be deterministic, and so cannot use a subquery or the `r.js` command.

The first argument, `context`, is a ReQL object containing the following properties:

- `primary_key`: primary key of the document being deleted, inserted, or modified
- `timestamp`: a ReQL `time` object representing the current query execution time

{% infobox %}
As is the case when creating secondary index functions using [indexCreate](/api/javascript/index_create), `r.now()` is considered non-deterministic and is thus not allowed in the context of write hooks. If you need to reference the current timestamp, `context('timestamp')` should be used instead.
{% endinfobox %}

Whenever a write operation on the table inserts, deletes or modifies a given document, the write hook function will be called with the context parameter, the old value of the document (or `null` on inserts) and the new value of the document (or `null` on deletes). It then returns the value that should actually be inserted and/or replaced instead of `newVal`. It can also return `r.error(...)` to abort the write.

For simplicity, the write hook function is allowed to return `null` exactly if and only if `newVal` is `null`. This is just a safeguard to ensure you don't accidentally turn an insert/update into a deletion, or a deletion into an update.

If successful, `setWriteHook` returns an object of the following form:

```js
{
  "function": <binary>,
  "query": "setWriteHook(function(_var1, _var2, _var3) { return ...; })",
}
```

__Example:__ Create a write hook that sets `modified_at` to the current time on each write operation.

```js
r.table('comments').setWriteHook(function(context, oldVal, newVal) {
  return newVal.merge({
    modified_at: context('timestamp')
  });
}).run(conn, callback)
```

__Example:__ Delete the write hook associated with the `comments` table.

```js
r.table('comments').setWriteHook(null).run(conn, callback)
```

__Example:__ Recreate an outdated write hook on a table.

```js
r.table('posts').getWriteHook().do(function(writeHook) {
  return r.table('posts').setWriteHook(writeHook('function'));
}).run(conn, callback)
```
