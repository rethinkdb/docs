---
layout: api-command
language: Python
permalink: api/python/index_create/
command: index_create
related_commands:
    index_wait: index_wait/
    index_status: index_status/
    index_list: index_list/
    index_drop: index_drop/
---

# Command syntax #

{% apibody %}
table.index_create(index_name[, index_function][, multi=True]) &rarr; object
{% endapibody %}

# Description #

Create a new secondary index on this table.

RethinkDB supports different types of secondary indexes:

- Simple indexes based on the value of a single field.
- Compound indexes based on multiple fields.
- Multi indexes based on arrays of values.
- Indexes based on arbitrary expressions.

The function you give to `index_create` must be deterministic. In practice this means that
that you cannot use a function that contains a sub-query or the `r.js` command.

Read the [guide on secondary indexes](http://www.rethinkdb.com/docs/secondary-indexes/)
to learn more about how they work in RethinkDB.

__Example:__ Create a simple index based on the field `post_id`.

```py
r.table('comments').index_create('post_id').run(conn)
```

__Example:__ Create a simple index based on the nested field `author > name`.

```py
r.table('comments').index_create('author_name', r.row["author"]["name"]).run(conn)
```


__Example:__ Create a compound index based on the fields `post_id` and `date`.

```py
r.table('comments').index_create('post_and_date', [r.row["post_id"], r.row["date"]]).run(conn)
```

__Example:__ Create a multi index based on the field `authors`.

```py
r.table('posts').index_create('authors', multi=True).run(conn)
```

__Example:__ Create a multi index based on an arbitrary expression.

```py
r.table('posts').index_create('authors', lambda doc:
    r.branch(
        doc.has_fields("updated_at"),
        doc["updated_at"],
        doc["created_at"]
    )
).run(conn)
```
