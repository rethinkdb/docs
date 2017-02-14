---
layout: api-command
language: JavaScript
permalink: api/javascript/get/
command: get
io:
    -   - table
        - singleSelection
related_commands:
    getAll: get_all/
    between: between/
---

# Command syntax #

{% apibody %}
table.get(key) &rarr; singleRowSelection
{% endapibody %}

# Description #

Get a document by primary key.

If no document exists with that primary key, `get` will return `null`.

__Example:__ Find a document by UUID.

```javascript
r.table('posts').get('a9849eef-7176-4411-935b-79a6e3c56a74').run(conn, callback);
```

__Example:__ Find a document and merge another document with it.

```javascript
r.table('heroes').get(3).merge(
    { powers: ['invisibility', 'speed'] }
).run(conn, callback);
```

___Example:__ Subscribe to a document's [changefeed](/docs/changefeeds/javascript).

```javascript
r.table('heroes').get(3).changes().run(conn, callback);
```