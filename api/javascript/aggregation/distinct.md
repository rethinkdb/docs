---
layout: api-command
language: JavaScript
permalink: api/javascript/distinct/
command: distinct
io:
    -   - sequence
        - array
    -   - table
        - stream
related_commands:
    map: map/
    concat_map: concat_map/
    group: group/
---

# Command syntax #

{% apibody %}
sequence.distinct() &rarr; array
table.distinct([{index: <indexname>}]) &rarr; stream
r.distinct(sequence) &rarr; array
r.distinct(table, [{index: <indexname>}]) &rarr; stream
{% endapibody %}

# Description #

Removes duplicates from elements in a sequence.

The `distinct` command can be called on any sequence or table with an index.

{% infobox %}
While `distinct` can be called on a table without an index, the only effect will be to convert the table into a stream; the content of the stream will not be affected.
{% endinfobox %}

__Example:__ Which unique villains have been vanquished by Marvel heroes?

```javascript
r.table('marvel').concatMap(function(hero) {
    return hero('villainList')
}).distinct().run(conn, callback)
```

__Example:__ Topics in a table of messages have a secondary index on them, and more than one message can have the same topic. What are the unique topics in the table?

```javascript
r.table('messages').distinct({index: 'topics'}).run(conn, callback)
```

The above structure is functionally identical to:

```javascript
r.table('messages')('topics').distinct().run(conn, callback)
```

However, the first form (passing the index as an argument to `distinct`) is faster, and won't run into array limit issues since it's returning a stream.
