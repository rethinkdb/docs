---
layout: api-command
language: JavaScript
permalink: api/javascript/index_status/
command: indexStatus
io:
    -   - table
        - array
related_commands:
    indexWait: index_wait/

---

# Command syntax #

{% apibody %}
table.indexStatus([, index...]) &rarr; array
{% endapibody %}

# Description #

Get the status of the specified indexes on this table, or the status
of all indexes on this table if no indexes are specified.

The result is an array where for each index, there will be an object like this one:

```js
{
    index: <indexName>,
    ready: true
}
```

or this one:

```js
{
    index: <indexName>,
    ready: false,
    blocks_processed: <int>,
    blocks_total: <int>
}
```

__Example:__ Get the status of all the indexes on `test`:

```js
r.table('test').indexStatus().run(conn, callback)
```

__Example:__ Get the status of the `timestamp` index:

```js
r.table('test').indexStatus('timestamp').run(conn, callback)
```
