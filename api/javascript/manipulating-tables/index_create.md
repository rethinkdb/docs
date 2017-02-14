---
layout: api-command
language: JavaScript
permalink: api/javascript/index_create/
command: indexCreate
io:
    -   - table
        - object
related_commands:
    indexWait: index_wait/
    indexStatus: index_status/
    indexList: index_list/
    indexDrop: index_drop/

---

# Command syntax #

{% apibody %}
table.indexCreate(indexName[, indexFunction][, {multi: false, geo: false}]) &rarr; object
{% endapibody %}

# Description #

Create a new secondary index on a table. Secondary indexes improve the speed of many read queries at the slight cost of increased storage space and decreased write performance. For more information about secondary indexes, read the article "[Using secondary indexes in RethinkDB](/docs/secondary-indexes/)."

RethinkDB supports different types of secondary indexes:

- *Simple indexes* based on the value of a single field.
- *Compound indexes* based on multiple fields.
- *Multi indexes* based on arrays of values, created when the `multi` optional argument is `true`.
- *Geospatial indexes* based on indexes of geometry objects, created when the `geo` optional argument is true.
- Indexes based on *arbitrary expressions*.

The `indexFunction` can be an anonymous function or a binary representation obtained from the `function` field of [indexStatus](/api/javascript/index_status). The function must be deterministic, and so cannot use a subquery or the `r.js` command.

If successful, `createIndex` will return an object of the form `{"created": 1}`. If an index by that name already exists on the table, a `ReqlRuntimeError` will be thrown.

{% infobox %}
Note that an index may not be immediately available after creation. If your application needs to use indexes immediately after creation, use the [indexWait](/api/javascript/index_wait) command to ensure the indexes are ready before use.
{% endinfobox %}

__Example:__ Create a simple index based on the field `postId`.

```javascript
r.table('comments').indexCreate('postId').run(conn, callback)
```

__Example:__ Create a geospatial index based on the field `location`.

```javascript
r.table('places').indexCreate('location', {geo: true}).run(conn, callback)
```

A geospatial index field should contain only geometry objects. It will work with geometry ReQL terms ([getIntersecting](/api/javascript/get_intersecting/) and [getNearest](/api/javascript/get_nearest/)) as well as index-specific terms ([indexStatus](/api/javascript/index_status), [indexWait](/api/javascript/index_wait), [indexDrop](/api/javascript/index_drop) and [indexList](/api/javascript/index_list)). Using terms that rely on non-geometric ordering such as [getAll](/api/javascript/get_all/), [orderBy](/api/javascript/order_by/) and [between](/api/javascript/between/) will result in an error.

__Example:__ Create a simple index based on the nested field `author > name`.

```javascript
r.table('comments').indexCreate('authorName', r.row("author")("name")).run(conn, callback)
```


__Example:__ Create a compound index based on the fields `postId` and `date`.

```javascript
r.table('comments').indexCreate('postAndDate', [r.row("postId"), r.row("date")]).run(conn, callback)
```

__Example:__ Create a multi index based on the field `authors`.

```javascript
r.table('posts').indexCreate('authors', {multi: true}).run(conn, callback)
```

__Example:__ Create a geospatial multi index based on the field `towers`.

```javascript
r.table('networks').indexCreate('towers', {multi: true, geo: true}).run(conn, callback)
```

__Example:__ Create an index based on an arbitrary expression.

```javascript
r.table('posts').indexCreate('authors', function(doc) {
    return r.branch(
        doc.hasFields("updatedAt"),
        doc("updatedAt"),
        doc("createdAt")
    )
}).run(conn, callback)
```

__Example:__ Create a new secondary index based on an existing one.

```javascript
r.table('posts').indexStatus('authors').nth(0)('function').run(conn, function (func) {
    r.table('newPosts').indexCreate('authors', func).run(conn, callback);
});
```

__Example:__ Rebuild an outdated secondary index on a table.

```javascript
r.table('posts').indexStatus('oldIndex').nth(0).do(function(oldIndex) {
  return r.table('posts').indexCreate('newIndex', oldIndex("function")).do(function() {
    return r.table('posts').indexWait('newIndex').do(function() {
      return r.table('posts').indexRename('newIndex', 'oldIndex', {overwrite: true})
    })
  })
})
```
