---
layout: api-command
language: JavaScript
permalink: api/javascript/reduce/
command: reduce
io:
    -   - sequence
        - value
related_commands:
    group: group/
    map: map/
    concat_map: concat_map/
    sum: sum/
    avg: avg/
    min: min/
    max: max/
---

# Command syntax #

{% apibody %}
sequence.reduce(function) &rarr; value
r.reduce(sequence, function) &rarr; value
{% endapibody %}

# Description #

Produce a single value from a sequence through repeated application of a reduction function.

The reduction function can be called on:

- two elements of the sequence
- one element of the sequence and one result of a previous reduction
- two results of previous reductions

The reduction function can be called on the results of two previous reductions because the
`reduce` command is distributed and parallelized across shards and CPU cores. A common
mistaken when using the `reduce` command is to suppose that the reduction is executed
from left to right. Read the [map-reduce in RethinkDB](/docs/map-reduce/) article to
see an example.

If the sequence is empty, the server will produce a `ReqlRuntimeError` that can be
caught with `default`.  
If the sequence has only one element, the first element will be returned.

__Example:__ Return the number of documents in the table `posts`.

```javascript
r.table("posts").map(function(doc) {
    return 1;
}).reduce(function(left, right) {
    return left.add(right);
}).default(0).run(conn, callback);
```

A shorter way to execute this query is to use [count](/api/javascript/count).


__Example:__ Suppose that each `post` has a field `comments` that is an array of
comments.  
Return the number of comments for all posts.

```javascript
r.table("posts").map(function(doc) {
    return doc("comments").count();
}).reduce(function(left, right) {
    return left.add(right);
}).default(0).run(conn, callback);
```



__Example:__ Suppose that each `post` has a field `comments` that is an array of
comments.  
Return the maximum number comments per post.

```javascript
r.table("posts").map(function(doc) {
    return doc("comments").count();
}).reduce(function(left, right) {
    return r.branch(
        left.gt(right),
        left,
        right
    );
}).default(0).run(conn, callback);
```

A shorter way to execute this query is to use [max](/api/javascript/max).
