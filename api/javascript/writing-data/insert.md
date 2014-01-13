---
layout: api-command
language: JavaScript
permalink: api/javascript/insert/
command: insert
io:
    -   - table
        - object
    -   - selection
        - object
    -   - singleSelection
        - object
related_commands:
    update: update/
    replace: replace/
    delete: delete/
---

# Command syntax #

{% apibody %}
table.insert(json | [json][, {durability: "hard", returnVals: false, upsert: false}]) &rarr; object
{% endapibody %}

# Description #

Insert documents into a table. Accepts a single document or an array of
documents.

The optional arguments are:

- `durability`: possible values are `hard` and `soft`. This option will override the
table or query's durability setting (set in [run](/api/javascript/run/)).  
In soft durability mode RethinkDB will acknowledge the write immediately after
receiving it, but before the write has been committed to disk.
- `returnVals`: if set to `true` and in case of a single insert/upsert, the inserted/updated
document will be returned.
- `upsert`: when set to `true`, performs an update if a document with the same primary key
exists.

Insert returns an object that contains the following attributes:

- `inserted`: the number of documents that were succesfully inserted.
- `replaced`: the number of documents that were updated when upsert is used.
- `unchanged`: the number of documents that would have been modified, except that the
new value was the same as the old value when doing an upsert.
- `errors`: the number of errors encountered while performing the insert.
- `first_error`: If errors were encountered, contains the text of the first error.
- `deleted` and `skipped`: 0 for an insert operation.
- `generated_keys`: a list of generated primary keys in case the primary keys for some
documents were missing (capped to 100000).
- `warnings`: if the field `generated_keys` is truncated, you will get the warning _"Too
many generated keys (&lt;X&gt;), array truncated to 100000."_.
- `old_val`: if `returnVals` is set to `true`, contains `null`.
- `new_val`: if `returnVals` is set to `true`, contains the inserted/updated document.



__Example:__ Insert a document into the table `posts`.

```js
r.table("posts").insert({
    id: 1,
    title: "Lorem ipsum",
    content: "Dolor sit amet"
}).run(conn, callback)
```

The result will be:

```js
{
    deleted: 0,
    errors: 0,
    inserted: 1,
    replaced: 0,
    skipped: 0,
    unchanged: 0
}
```


__Example:__ Insert a document without a defined primary key into the table `posts` where the
primary key is `id`.

```js
r.table("posts").insert({
    title: "Lorem ipsum",
    content: "Dolor sit amet"
}).run(conn, callback)
```

RethinkDB will generate a primary key and return it in `generated_keys`.

```js
{
    deleted: 0,
    errors: 0,
    generated_keys: [
        "dd782b64-70a7-43e4-b65e-dd14ae61d947"
    ],
    inserted: 1,
    replaced: 0,
    skipped: 0,
    unchanged: 0
}
```

Retrieve the document you just inserted with:

```js
r.table("posts").get("dd782b64-70a7-43e4-b65e-dd14ae61d947").run(conn, callback)
```

And you will get back:

```js
{
    id: "dd782b64-70a7-43e4-b65e-dd14ae61d947",
    title: "Lorem ipsum",
    content: "Dolor sit amet",
}
```


__Example:__ Insert multiple documents into the table `users`.

```js
r.table("users").insert([
    {id: "william", email: "william@rethinkdb.com"},
    {id: "lara", email: "lara@rethinkdb.com"}
]).run(conn, callback)
```


__Example:__ Insert a document into the table `users`, replacing the document if the document
already exists.  
_Note_: If the document exists, the `insert` command will behave like [replace](../replace/), not like [update](../update/) 

```js
r.table("users").insert(
    {id: "william", email: "william@rethinkdb.com"},
    {upsert: true}
).run(conn, callback)
```


__Example:__ Copy the documents from `posts` to `postsBackup`.

```js
r.table("postsBackup").insert( r.table("posts") ).run(conn, callback)
```


__Example:__ Get back a copy of the inserted document (with its generated primary key).

```js
r.table("posts").insert(
    {title: "Lorem ipsum", content: "Dolor sit amet"},
    {returnVals: true}
).run(conn, callback)
```

The result will be

```js
{
    deleted: 0,
    errors: 0,
    generated_keys: [
        "dd782b64-70a7-43e4-b65e-dd14ae61d947"
    ],
    inserted: 1,
    replaced: 0,
    skipped: 0,
    unchanged: 0,
    old_val: null,
    new_val: {
        id: "dd782b64-70a7-43e4-b65e-dd14ae61d947",
        title: "Lorem ipsum",
        content: "Dolor sit amet"
    }
}
```
