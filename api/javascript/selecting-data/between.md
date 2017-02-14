---
layout: api-command
language: JavaScript
permalink: api/javascript/between/
command: between
alias:
    - api/javascript/minval/
    - api/javascript/maxval/
io:
    -   - table
        - table_slice
related_commands:
    get: get/
    getAll: get_all/
---

# Command syntax #

{% apibody %}
table.between(lowerKey, upperKey[, options]) &rarr; table_slice
table_slice.between(lowerKey, upperKey[, options]) &rarr; table_slice
{% endapibody %}

# Description #

Get all documents between two keys. Accepts three optional arguments: `index`, `leftBound`, and `rightBound`. If `index` is set to the name of a secondary index, `between` will return all documents where that index's value is in the specified range (it uses the primary key by default). `leftBound` or `rightBound` may be set to `open` or `closed` to indicate whether or not to include that endpoint of the range (by default, `leftBound` is closed and `rightBound` is open).

You may also use the special constants `r.minval` and `r.maxval` for boundaries, which represent "less than any index key" and "more than any index key" respectively. For instance, if you use `r.minval` as the lower key, then `between` will return all documents whose primary keys (or indexes) are less than the specified upper key.

If you use arrays as indexes (compound indexes), they will be sorted using [lexicographical order][lo]. Take the following range as an example:

```text
[[1, "c"] ... [5, "e"]]
```

This range includes all compound keys:

* whose first item is 1 and second item is equal or greater than "c";
* whose first item is between 1 and 5, *regardless of the value of the second item*;
* whose first item is 5 and second item is less than or equal to "e".

[lo]: https://en.wikipedia.org/wiki/Lexicographical_order

__Example:__ Find all users with primary key >= 10 and < 20 (a normal half-open interval).

```javascript
r.table('marvel').between(10, 20).run(conn, callback);
```

__Example:__ Find all users with primary key >= 10 and <= 20 (an interval closed on both sides).

```javascript
r.table('marvel').between(10, 20, {rightBound: 'closed'}).run(conn, callback);
```

__Example:__ Find all users with primary key < 20.

```javascript
r.table('marvel').between(r.minval, 20).run(conn, callback);
```

__Example:__ Find all users with primary key > 10.

```javascript
r.table('marvel').between(10, r.maxval, {leftBound: 'open'}).run(conn, callback);
```

__Example:__ Between can be used on secondary indexes too. Just pass an optional index argument giving the secondary index to query.

```javascript
r.table('dc').between('dark_knight', 'man_of_steel', {index: 'code_name'}).run(conn, callback);
```

__Example:__ Get all users whose full name is between "John Smith" and "Wade Welles."

```javascript
r.table("users").between(["Smith", "John"], ["Welles", "Wade"],
  {index: "full_name"}).run(conn, callback);
```

__Example:__ Get the top 10 ranked teams in order.

```javascript
r.table("teams").orderBy({index: "rank"}).between(1, 11).run(conn, callback);
```

__Note:__ When `between` is chained after [orderBy](/api/javascript/order_by), both commands must use the same index; `between` will default to the index `orderBy` is using, so in this example `"rank"` is automatically being used by `between`. Trying to specify another index will result in a `ReqlRuntimeError`.

__Example:__ Subscribe to a [changefeed](/docs/changefeeds/javascript) of teams ranked in the top 10.

```javascript
r.table("teams").between(1, 11, {index: "rank"}).changes().run(conn, callback);
```

{% infobox %}
The `between` command works with secondary indexes on date fields, but will not work with unindexed date fields. To test whether a date value is between two other dates, use the [during](/api/javascript/during) command, not `between`.

Secondary indexes can be used in extremely powerful ways with `between` and other commands; read the full article on [secondary indexes](/docs/secondary-indexes) for examples using boolean operations, `contains` and more.

RethinkDB uses byte-wise ordering for `between` and does not support Unicode collations; non-ASCII characters will be sorted by UTF-8 codepoint.
{% endinfobox %}
