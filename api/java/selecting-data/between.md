---
layout: api-command
language: Java
permalink: api/java/between/
command: between
alias:
    - api/java/minval/
    - api/java/maxval/
related_commands:
    get: get/
    getAll: get_all/
    filter: filter/
---

# Command syntax #

{% apibody %}
table.between(lowerKey, upperKey) &rarr; selection
{% endapibody %}

# Description #

Get all documents between two keys. Accepts three [optArgs](/api/java/optarg): `index`, `left_bound`, and `right_bound`. If `index` is set to the name of a secondary index, `between` will return all documents where that index's value is in the specified range (it uses the primary key by default). `left_bound` or `right_bound` may be set to `open` or `closed` to indicate whether or not to include that endpoint of the range (by default, `left_bound` is closed and `right_bound` is open).

You may also use the special constants `r.minval` and `r.maxval` for boundaries, which represent "less than any index key" and "more than any index key" respectively. For instance, if you use `r.minval` as the lower key, then `between` will return all documents whose primary keys (or indexes) are less than the specified upper key.

If you use arrays as indexes (compound indexes), they will be sorted using [lexicographical order][lo]. Take the following range as an example:

	[[1, "c"] ... [5, "e"]]

This range includes all compound keys:

* whose first item is 1 and second item is equal or greater than "c";
* whose first item is between 1 and 5, *regardless of the value of the second item*;
* whose first item is 5 and second item is less than or equal to "e".

[lo]: https://en.wikipedia.org/wiki/Lexicographical_order

__Example:__ Find all users with primary key >= 10 and < 20 (a normal half-open interval).

```java
r.table("marvel").between(10, 20).run(conn);
```

__Example:__ Find all users with primary key >= 10 and <= 20 (an interval closed on both sides).

```py
r.table("marvel").between(10, 20).optArg("right_bound", "closed").run(conn);
```

__Example:__ Find all users with primary key < 20.

```py
r.table("marvel").between(r.minval(), 20).run(conn);
```

__Example:__ Find all users with primary key > 10.

```py
r.table("marvel").between(10, r.maxval()).optArg("left_bound", "open").run(conn);
```

__Example:__ Between can be used on secondary indexes too. Just pass an optional index argument giving the secondary index to query.

```py
r.table("dc").between("dark_knight", "man_of_steel").optArg("index", "code_name").run(conn);
```

__Example:__ Get all users whose full name is between "John Smith" and "Wade Welles."

```py
r.table("users").between(r.array("Smith", "John"), r.array("Welles", "Wade")).optArg("index", "full_name").run(conn);
```

__Note:__ Between works with secondary indexes on date fields, but will not work with unindexed date fields. To test whether a date value is between two other dates, use the [during](/api/java/during) command, not `between`.

Secondary indexes can be used in extremely powerful ways with `between` and other commands; read the full article on [secondary indexes](/docs/secondary-indexes) for examples using boolean operations, `contains` and more.

__Note:__ RethinkDB uses byte-wise ordering for `between` and does not support Unicode collations; non-ASCII characters will be sorted by UTF-8 codepoint.

__Note:__ If you chain `between` after [orderBy](/api/java/order_by), the `between` command must use the index specified in `orderBy`, and will default to that index. Trying to specify another index will result in a `ReqlRuntimeError`.
