---
layout: api-command
language: JavaScript
permalink: api/javascript/order_by/
command: orderBy
io:
    -   - sequence
        - stream
    -   - array
        - array
related_commands:
    skip: skip/
    limit: limit/
    slice: slice/
---

# Command syntax #

{% apibody %}
table.orderBy([key1...], {index: index_name}) &rarr; selection<stream>
selection.orderBy(key1, [key2...]) &rarr; selection<array>
sequence.orderBy(key1, [key2...]) &rarr; array
{% endapibody %}

# Description #

Sort the sequence by document values of the given key(s). To specify
the ordering, wrap the attribute with either `r.asc` or `r.desc`
(defaults to ascending).

Sorting without an index requires the server to hold the sequence in
memory, and is limited to 100,000 documents. Sorting with an index can
be done on arbitrarily large tables, or after a `between` command
using the same index.

__Example:__ Order all the posts using the index `date`.   

```js
r.table('posts').orderBy({index: 'date'}).run(conn, callback)
```

The index must have been previously created with [indexCreate](/api/javascript/index_create/).

```js
r.table('posts').indexCreate('date').run(conn, callback)
```

You can also select a descending ordering:

```js
r.table('posts').orderBy({index: r.desc('date')}).run(conn, callback)
```

__Example:__ If you have a sequence with less than 100,000 documents, you can order it
without an index.

```js
r.table('posts').get(1)('comments').orderBy('date')
```

You can also select a descending ordering:

```js
r.table('posts').get(1)('comments').orderBy(r.desc('date'))
```

If you're doing ad-hoc analysis and know your table won't have more then 100,000
elements you can run `orderBy` without an index:

```js
r.table('small_table').orderBy('date')
```

__Example:__ You can efficiently order using multiple fields by using a
[compound index](http://www.rethinkdb.com/docs/secondary-indexes/javascript/).

Order by date and title.

```js
r.table('posts').orderBy({index: 'dateAndTitle'}).run(conn, callback)
```

The index must have been previously created with [indexCreate](/api/javascript/index_create/).

```js
r.table('posts').indexCreate('dateAndTitle', [r.row('date'), r.row('title')]).run(conn, callback)
```

_Note_: You cannot specify multiple orders in a compound index. See [issue #2306](https://github.com/rethinkdb/rethinkdb/issues/2306)
to track progress.

__Example:__ If you have a sequence with less than 100,000 documents, you can order it
by multiple fields without an index.

```js
r.table('small_table').orderBy('date', r.desc('title'))
```

__Example:__ Notice that an index ordering always has highest
precedence. The following query orders posts by date, and if multiple
posts were published on the same date, they will be ordered by title.

```js
r.table('post').orderBy('title', {index: 'date'}).run(conn, callback)
```

__Example:__ You can efficiently order data on arbitrary expressions using indexes.

```js
r.table('posts').orderBy({index: 'votes'}).run(conn, callback)
```

The index must have been previously created with [indexCreate](/api/javascript/index_create/).

```js
r.table('posts').indexCreate('votes', function(post) {
    return post('upvotes').sub(post('downvotes'))
}).run(conn, callback)
```

__Example:__ If you have a sequence with less than 100,000 documents, you can order it with an arbitrary function directly.

```js
r.table('small_table').orderBy(function(doc) {
    return doc('upvotes').sub(doc('downvotes'))
});
```

You can also select a descending ordering:

```js
r.table('small_table').orderBy(r.desc(function(doc) {
    return doc('upvotes').sub(doc('downvotes'))
}));
```

__Example:__ Ordering after a `between` command can be done as long as the same index is being used.

```js
r.table('posts').between(r.time(2013, 1, 1, '+00:00'), r.time(2013, 1, 1, '+00:00'), {index: 'date'})
    .orderBy({index: 'date'}).run(conn, callback);
```

