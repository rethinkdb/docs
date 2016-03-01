---
layout: api-command
language: Python
permalink: api/python/delete/
command: delete
related_commands:
    insert: insert/
    update: update/
    replace: replace/
---

# Command syntax #

{% apibody %}
table.delete([durability="hard", return_changes=False])
    &rarr; object
selection.delete([durability="hard", return_changes=False])
    &rarr; object
singleSelection.delete([durability="hard", return_changes=False])
    &rarr; object
{% endapibody %}

<img src="/assets/images/docs/api_illustrations/delete-vector.png" class="api_command_illustration" />

# Description #

Delete one or more documents from a table.

The optional arguments are:

- `durability`: possible values are `hard` and `soft`. This option will override the
table or query's durability setting (set in [run](/api/python/run/)).  
In soft durability mode RethinkDB will acknowledge the write immediately after
receiving it, but before the write has been committed to disk.
- `return_changes`:
    - `True`: return a `changes` array consisting of `old_val`/`new_val` objects describing the changes made, only including the documents actually updated.
    - `False`: do not return a `changes` array (the default).
    - `"always"`: behave as `True`, but include all documents the command tried to update whether or not the update was successful. (This was the behavior of `True` pre-2.0.)

Delete returns an object that contains the following attributes:

- `deleted`: the number of documents that were deleted.
- `skipped`: the number of documents that were skipped.  
For example, if you attempt to delete a batch of documents, and another concurrent query
deletes some of those documents first, they will be counted as skipped.
- `errors`: the number of errors encountered while performing the delete.
- `first_error`: If errors were encountered, contains the text of the first error.
- `inserted`, `replaced`, and `unchanged`: all 0 for a delete operation.
- `changes`: if `return_changes` is set to `True`, this will be an array of objects, one for each objected affected by the `delete` operation. Each object will have two keys: `{"new_val": None, "old_val": <old value>}`.

{% infobox alert %}
RethinkDB write operations will only throw exceptions if errors occur before any writes. Other errors will be listed in `first_error`, and `errors` will be set to a non-zero count. To properly handle errors with this term, code must both handle exceptions and check the `errors` return value!
{% endinfobox %}

__Example:__ Delete a single document from the table `comments`.

```py
r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete().run(conn)
```

__Example:__ Delete all documents from the table `comments`.

```py
r.table("comments").delete().run(conn)
```

__Example:__ Delete all comments where the field `id_post` is `3`.

```py
r.table("comments").filter({"id_post": 3}).delete().run(conn)
```

__Example:__ Delete a single document from the table `comments` and return its value.

```py
r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete(return_changes=True).run(conn)
```

The result will look like:

```py
{
    "deleted": 1,
    "errors": 0,
    "inserted": 0,
    "changes": [
        {
            "new_val": None,
            "old_val": {
                "id": "7eab9e63-73f1-4f33-8ce4-95cbea626f59",
                "author": "William",
                "comment": "Great post",
                "id_post": 3
            }
        }
    ],
    "replaced": 0,
    "skipped": 0,
    "unchanged": 0
}
```


__Example:__ Delete all documents from the table `comments` without waiting for the
operation to be flushed to disk.

```py
r.table("comments").delete({durability="soft"}).run(conn)
```
