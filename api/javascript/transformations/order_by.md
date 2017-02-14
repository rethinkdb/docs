---
layout: api-command
language: JavaScript
permalink: api/javascript/order_by/
alias:
    - api/javascript/asc/
    - api/javascript/desc/
command: orderBy
io:
    -   - table
        - table_slice
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
table.orderBy([key | function...], {index: index_name}) &rarr; table_slice
selection.orderBy(key | function[, ...]) &rarr; selection<array>
sequence.orderBy(key | function[, ...]) &rarr; array
{% endapibody %}

# Description #

Sort the sequence by document values of the given key(s). To specify
the ordering, wrap the attribute with either `r.asc` or `r.desc`
(defaults to ascending).

__Note:__ RethinkDB uses byte-wise ordering for `orderBy` and does not support Unicode collations; non-ASCII characters will be sorted by UTF-8 codepoint. For more information on RethinkDB's sorting order, read the section in [ReQL data types](/docs/data-types/#sorting-order).

Sorting without an index requires the server to hold the sequence in
memory, and is limited to 100,000 documents (or the setting of the `arrayLimit` option for [run](/api/javascript/run)). Sorting with an index can
be done on arbitrarily large tables, or after a [between](/api/javascript/between/) command
using the same index. This applies to both secondary indexes and the primary key (e.g., `{index: 'id'}`).

Sorting functions passed to `orderBy` must be deterministic. You cannot, for instance, order rows using the [random](/api/javascript/random/) command. Using a non-deterministic function with `orderBy` will raise a `ReqlQueryLogicError`.

__Example:__ Order all the posts using the index `date`.   

```javascript
r.table('posts').orderBy({index: 'date'}).run(conn, callback);
```

<!-- stop -->

The index must either be the primary key or have been previously created with [indexCreate](/api/javascript/index_create/).

```javascript
r.table('posts').indexCreate('date').run(conn, callback);
```

You can also select a descending ordering:

```javascript
r.table('posts').orderBy({index: r.desc('date')}).run(conn, callback);
```

__Example:__ Order a sequence without an index.

```javascript
r.table('posts').get(1)('comments').orderBy('date').run(conn, callback);
```

You can also select a descending ordering:

```javascript
r.table('posts').get(1)('comments').orderBy(r.desc('date')).run(conn, callback);
```

If you're doing ad-hoc analysis and know your table won't have more then 100,000
elements (or you've changed the setting of the `array_limit` option for [run](/api/javascript/run)) you can run `orderBy` without an index:

```javascript
r.table('small_table').orderBy('date').run(conn, callback);
```

__Example:__ You can efficiently order using multiple fields by using a
[compound index](http://www.rethinkdb.com/docs/secondary-indexes/javascript/).

Order by date and title.

```javascript
r.table('posts').orderBy({index: 'dateAndTitle'}).run(conn, callback);
```

The index must either be the primary key or have been previously created with [indexCreate](/api/javascript/index_create/).

```javascript
r.table('posts').indexCreate('dateAndTitle', [r.row('date'), r.row('title')]).run(conn, callback);
```

_Note_: You cannot specify multiple orders in a compound index. See [issue #2306](https://github.com/rethinkdb/rethinkdb/issues/2306)
to track progress.

__Example:__ If you have a sequence with fewer documents than the `arrayLimit`, you can order it
by multiple fields without an index.

```javascript
r.table('small_table').orderBy('date', r.desc('title')).run(conn, callback);
```

__Example:__ Notice that an index ordering always has highest
precedence. The following query orders posts by date, and if multiple
posts were published on the same date, they will be ordered by title.

```javascript
r.table('post').orderBy('title', {index: 'date'}).run(conn, callback);
```

__Example:__ Use [nested field](/docs/cookbook/javascript/#filtering-based-on-nested-fields) syntax to sort on fields from subdocuments. (You can also create indexes on nested fields using this syntax with `indexCreate`.)

```javascript
r.table('user').orderBy(r.row('group')('id')).run(conn, callback);
```

__Example:__ You can efficiently order data on arbitrary expressions using indexes.

```javascript
r.table('posts').orderBy({index: 'votes'}).run(conn, callback);
```

The index must have been previously created with [indexCreate](/api/javascript/index_create/).

```javascript
r.table('posts').indexCreate('votes', function(post) {
    return post('upvotes').sub(post('downvotes'))
}).run(conn, callback);
```

__Example:__ If you have a sequence with fewer documents than the `arrayLimit`, you can order it with an arbitrary function directly.

```javascript
r.table('small_table').orderBy(function(doc) {
    return doc('upvotes').sub(doc('downvotes'))
}).run(conn, callback);
```

You can also select a descending ordering:

```javascript
r.table('small_table').orderBy(r.desc(function(doc) {
    return doc('upvotes').sub(doc('downvotes'))
})).run(conn, callback);
```

__Example:__ Ordering after a `between` command can be done as long as the same index is being used.

```javascript
r.table('posts').between(r.time(2013, 1, 1, '+00:00'), r.time(2013, 1, 1, '+00:00'), {index: 'date'})
    .orderBy({index: 'date'}).run(conn, callback);
```

