---
layout: api
title: "ReQL command reference"
active: api
no_footer: true
permalink: api/javascript/
alias: api/
language: JavaScript
---

{% apisection Accessing ReQL%}
All ReQL queries begin from the top-level module.

## [r](r/) ##

{% apibody %}
r &rarr; r
{% endapibody %}

The top-level ReQL namespace.

__Example:__ Set up your top-level namespace.

```js
var r = require('rethinkdb');
```

## [connect](connect/) ##

{% apibody %}
r.connect(options, callback)
r.connect(host, callback)
{% endapibody %}

Create a new connection to the database server.  Accepts the following
options:

- `host`: the host to connect to (default `localhost`).
- `port`: the port to connect on (default `28015`).
- `db`: the default database (default `test`).
- `authKey`: the authentication key (default none).

If the connection cannot be established, a `RqlDriverError` will be
passed to the callback instead of a connection.

__Example:__ Opens a new connection to the database.

```js
r.connect({host:'localhost', port:28015, db:'marvel', authKey:'hunter2'},
          function(err, conn) { ... })
```

## [close](close/) ##

{% apibody %}
conn.close([opts, ]callback)
{% endapibody %}

Close an open connection.  Accepts the following options:

- `noreplyWait`: whether to wait for noreply writes to complete
  before closing (default `true`).  If this is set to `false`, some
  outstanding noreply writes may be aborted.

Closing a connection waits until all outstanding requests have
finished and then frees any open resources associated with the
connection.  If `noreplyWait` is set to `false`, all outstanding
requests are canceled immediately.

__Example:__ Close an open connection, waiting for noreply writes to finish.

```js
conn.close(function(err) { if (err) throw err; })
```

__Example:__ Close an open connection immediately.

```js
conn.close({noreplyWait: false}, function(err) { if (err) throw err; })
```

## [reconnect](reconnect/) ##

{% apibody %}
conn.reconnect([opts, ]callback)
{% endapibody %}

Close and reopen a connection.  Accepts the following options:

- `noreplyWait`: whether to wait for noreply writes to complete
  before closing (default `true`).  If this is set to `false`, some
  outstanding noreply writes may be aborted.

Closing a connection waits until all outstanding requests have
finished.  If `noreplyWait` is set to `false`, all outstanding
requests are canceled immediately.

__Example:__ Cancel outstanding requests/queries that are no longer needed.

```js
conn.reconnect({noreplyWait: false}, function(errror, connection) { ... })
```

## [use](use/) ##

{% apibody %}
conn.use(dbName)
{% endapibody %}

Change the default database on this connection.

__Example:__ Change the default database so that we don't need to
specify the database when referencing a table.

```js
conn.use('marvel')
r.table('heroes').run(conn, ...) // refers to r.db('marvel').table('heroes')
```

## [run](run/) ##

{% apibody %}
query.run(conn[, options], callback)
{% endapibody %}

Run a query on a connection. 

The callback will get either an error, a single JSON result, or a
cursor, depending on the query.

__Example:__ Run a query on the connection `conn` and log each row in
the result to the console.

```js
r.table('marvel').run(conn, function(err, cursor) { cursor.each(console.log); })
```

[Read more about this command &rarr;](run/)

## [noreplyWait](noreply_wait/) ##

{% apibody %}
conn.noreplyWait(callback)
{% endapibody %}

`noreplyWait` ensures that previous queries with the `noreply` flag have been processed
by the server. Note that this guarantee only applies to queries run on the given connection.

__Example:__ We have previously run queries with the `noreply` argument set to `true`. Now
wait until the server has processed them.

```js
conn.noreplyWait(function(err) { ... })
```


## [next](next/) ##

{% apibody %}
cursor.next(callback)
array.next(callback)
{% endapibody %}

Get the next element in the cursor.

__Example:__ Let's grab the next element!

```js
cursor.next(function(err, row) {
    if (err) throw err;
    processRow(row);
});
```

[Read more about this command &rarr;](next/)


## [hasNext](has_next/) ##

{% apibody %}
cursor.hasNext() &rarr; bool
array.hasNext() &rarr; bool
{% endapibody %}

Check if there are more elements in the cursor.

__Example:__ Are there more elements in the cursor?

```js
var hasMore = cursor.hasNext();
```

[Read more about this command &rarr;](has_next/)


## [each](each/) ##

{% apibody %}
cursor.each(callback[, onFinishedCallback])
array.each(callback[, onFinishedCallback])
{% endapibody %}

Lazily iterate over the result set one element at a time.

__Example:__ Let's process all the elements!

```js
cursor.each(function(err, row) {
    if (err) throw err;
    processRow(row);
});
```

[Read more about this command &rarr;](each/)

## [toArray](to_array/) ##

{% apibody %}
cursor.toArray(callback)
array.toArray(callback)
{% endapibody %}

Retrieve all results and pass them as an array to the given callback.

__Example:__ For small result sets it may be more convenient to process them at once as
an array.

```js
cursor.toArray(function(err, results) {
    if (err) throw err;
    processResults(results);
});
```

[Read more about this command &rarr;](to_array/)


## [close (cursor)](close-cursor/) ##

{% apibody %}
cursor.close()
{% endapibody %}


Close a cursor. Closing a cursor cancels the corresponding query and frees the memory
associated with the open request.

__Example:__ Close a cursor.

```js
cursor.close()
```


## [addListener](add_listener/) ##

{% apibody %}
conn.addListener(event, listener)
{% endapibody %}

The connection object also supports the event emitter interface so you can listen for
changes in connection state.

__Example:__ Monitor connection state with events 'connect', 'close', and 'error'.


```js
r.connect({}, function(err, conn) {
    if (err) throw err;

    conn.addListener('error', function(e) {
        processNetworkError(e);
    });

    conn.addListener('close', function() {
        cleanup();
    });

    runQueries(conn);
});

```

[Read more about this command &rarr;](add_listener/)


{% endapisection %}

{% apisection Manipulating databases%}
## [dbCreate](db_create/) ##

{% apibody %}
r.dbCreate(dbName) &rarr; object
{% endapibody %}

Create a database. A RethinkDB database is a collection of tables, similar to
relational databases.

If successful, the operation returns an object: `{created: 1}`. If a database with the
same name already exists the operation throws `RqlRuntimeError`.

Note: that you can only use alphanumeric characters and underscores for the database name.

__Example:__ Create a database named 'superheroes'.

```js
r.dbCreate('superheroes').run(conn, callback)
```


## [dbDrop](db_drop/) ##

{% apibody %}
r.dbDrop(dbName) &rarr; object
{% endapibody %}

Drop a database. The database, all its tables, and corresponding data will be deleted.

If successful, the operation returns the object `{dropped: 1}`. If the specified database
doesn't exist a `RqlRuntimeError` is thrown.

__Example:__ Drop a database named 'superheroes'.

```js
r.dbDrop('superheroes').run(conn, callback)
```


## [dbList](db_list/) ##

{% apibody %}
r.dbList() &rarr; array
{% endapibody %}

List all database names in the system. The result is a list of strings.

__Example:__ List all databases.

```js
r.dbList().run(conn, callback)
```

{% endapisection %}




{% apisection Manipulating tables%}
## [tableCreate](table_create/) ##

{% apibody %}
db.tableCreate(tableName[, options]) &rarr; object
{% endapibody %}

Create a table. A RethinkDB table is a collection of JSON documents.

If successful, the operation returns an object: `{created: 1}`. If a table with the same
name already exists, the operation throws `RqlRuntimeError`.

Note: that you can only use alphanumeric characters and underscores for the table name.

When creating a table you can specify the following options:

- `primaryKey`: the name of the primary key. The default primary key is id;
- `durability`: if set to `'soft'`, this enables _soft durability_ on this table:
writes will be acknowledged by the server immediately and flushed to disk in the
background. Default is `'hard'` (acknowledgement of writes happens after data has been
written to disk);
- `datacenter`: the name of the datacenter this table should be assigned to.


__Example:__ Create a table named 'dc_universe' with the default settings.

```js
r.db('test').tableCreate('dc_universe').run(conn, callback)
```

[Read more about this command &rarr;](table_create/)

## [tableDrop](table_drop/) ##

{% apibody %}
db.tableDrop(tableName) &rarr; object
{% endapibody %}

Drop a table. The table and all its data will be deleted.

If succesful, the operation returns an object: {dropped: 1}. If the specified table
doesn't exist a `RqlRuntimeError` is thrown.

__Example:__ Drop a table named 'dc_universe'.

```js
r.db('test').tableDrop('dc_universe').run(conn, callback)
```

## [tableList](table_list/) ##

{% apibody %}
db.tableList() &rarr; array
{% endapibody %}

List all table names in a database. The result is a list of strings.

__Example:__ List all tables of the 'test' database.

```js
r.db('test').tableList().run(conn, callback)
```

## [indexCreate](index_create/) ##

{% apibody %}
table.indexCreate(indexName[, indexFunction]) &rarr; object
{% endapibody %}

Create a new secondary index on this table.

__Example:__ To efficiently query our heros by code name we have to create a secondary
index.

```js
r.table('dc').indexCreate('code_name').run(conn, callback)
```

[Read more about this command &rarr;](index_create/)

## [indexDrop](index_drop/) ##

{% apibody %}
table.indexDrop(indexName) &rarr; object
{% endapibody %}

Delete a previously created secondary index of this table.

__Example:__ Drop a secondary index named 'code_name'.

```js
r.table('dc').indexDrop('code_name').run(conn, callback)
```

## [indexList](index_list/) ##

{% apibody %}
table.indexList() &rarr; array
{% endapibody %}

List all the secondary indexes of this table.

__Example:__ List the available secondary indexes for this table.

```js
r.table('marvel').indexList().run(conn, callback)
```

## [indexStatus](index_status/) ##

{% apibody %}
table.indexStatus([, index...]) &rarr; array
{% endapibody %}

Get the status of the specified indexes on this table, or the status
of all indexes on this table if no indexes are specified.

__Example:__ Get the status of all the indexes on `test`:

```js
r.table('test').indexStatus().run(conn, callback)
```

__Example:__ Get the status of the `timestamp` index:

```js
r.table('test').indexStatus('timestamp').run(conn, callback)
```

## [indexWait](index_wait/) ##

{% apibody %}
table.indexWait([, index...]) &rarr; array
{% endapibody %}

Wait for the specified indexes on this table to be ready, or for all
indexes on this table to be ready if no indexes are specified.

__Example:__ Wait for all indexes on the table `test` to be ready:

```js
r.table('test').indexWait().run(conn, callback)
```

__Example:__ Wait for the index `timestamp` to be ready:

```js
r.table('test').indexWait('timestamp').run(conn, callback)
```

{% endapisection %}


{% apisection Writing data%}

## [insert](insert/) ##

{% apibody %}
table.insert(json | [json]
    [, {durability: "hard", returnVals: false, upsert: false}])
        &rarr; object
{% endapibody %}

Insert JSON documents into a table. Accepts a single JSON document or an array of
documents.

__Example:__ Insert a document into the table `posts`.

```js
r.table("posts").insert({
    id: 1,
    title: "Lorem ipsum",
    content: "Dolor sit amet"
}).run(conn, callback)
```


[Read more about this command &rarr;](insert/)

## [update](update/) ##

{% apibody %}
table.update(json | expr
    [, {durability: "hard", returnVals: false, nonAtomic: false}])
        &rarr; object
selection.update(json | expr
    [, {durability: "hard", returnVals: false, nonAtomic: false}])
        &rarr; object
singleSelection.update(json | expr
    [, {durability: "hard", returnVals: false, nonAtomic: false}])
        &rarr; object
{% endapibody %}

Update JSON documents in a table. Accepts a JSON document, a ReQL expression, or a
combination of the two. You can pass options like `returnVals` that will return the old
and new values of the row you have modified.

__Example:__ Update Superman's age to 30. If attribute 'age' doesn't exist, adds it to
the document.

__Example:__ Update the status of the post with `id` of `1` to `published`.

```js
r.table("posts").get(1).update({status: "published"}).run(conn, callback)
```


[Read more about this command &rarr;](update/)


## [replace](replace/) ##

{% apibody %}
table.replace(json | expr
    [, {durability: "hard", returnVals: false, nonAtomic: false}])
        &rarr; object
selection.replace(json | expr
    [, {durability: "hard", returnVals: false, nonAtomic: false}])
        &rarr; object
singleSelection.replace(json | expr
    [, {durability: "hard", returnVals: false, nonAtomic: false}])
        &rarr; object

{% endapibody %}

Replace documents in a table. Accepts a JSON document or a ReQL expression, and replaces
the original document with the new one. The new document must have the same primary key
as the original document.

__Example:__ Replace the document with the primary key `1`.

```js
r.table("posts").get(1).replace({
    id: 1,
    title: "Lorem ipsum",
    content: "Aleas jacta est",
    status: "draft"
}).run(conn, callback)
```

[Read more about this command &rarr;](replace/)

## [delete](delete/) ##

{% apibody %}
table.delete([{durability: "hard", returnVals: false}])
    &rarr; object
selection.delete([{durability: "hard", returnVals: false}])
    &rarr; object
singleSelection.delete([{durability: "hard", returnVals: false}])
    &rarr; object
{% endapibody %}

Delete one or more documents from a table.

__Example:__ Delete a single document from the table `comments`.

```js
r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete().run(conn, callback)
```

[Read more about this command &rarr;](delete/)

## [sync](sync/) ##

{% apibody %}
table.sync()
    &rarr; object
{% endapibody %}

`sync` ensures that writes on a given table are written to permanent storage. Queries
that specify soft durability (`{durability: 'soft'}`) do not give such guarantees, so
`sync` can be used to ensure the state of these queries. A call to `sync` does not return
until all previous writes to the table are persisted.


__Example:__ After having updated multiple heroes with soft durability, we now want to wait
until these changes are persisted.

```js
r.table('marvel').sync().run(conn, callback)
```

{% endapisection %}


{% apisection Selecting data%}

## [db](db/) ##

{% apibody %}
r.db(dbName) &rarr; db
{% endapibody %}

Reference a database.

__Example:__ Before we can query a table we have to select the correct database.

```js
r.db('heroes').table('marvel').run(conn, callback)
```


## [table](table/) ##

{% apibody %}
db.table(name[, {useOutdated: false}]) &rarr; table
{% endapibody %}

Select all documents in a table. This command can be chained with other commands to do
further processing on the data.

__Example:__ Return all documents in the table 'marvel' of the default database.

```js
r.table('marvel').run(conn, callback)
```

[Read more about this command &rarr;](table/)

## [get](get/) ##

{% apibody %}
table.get(key) &rarr; singleRowSelection
{% endapibody %}

Get a document by primary key.

__Example:__ Find a document with the primary key 'superman'.

```js
r.table('marvel').get('superman').run(conn, callback)
```


## [getAll](get_all/) ##

{% apibody %}
table.getAll(key[, key2...], [, {index:'id'}]) &rarr; selection
{% endapibody %}

Get all documents where the given value matches the value of the requested index.

__Example:__ Secondary index keys are not guaranteed to be unique so we cannot query via
"get" when using a secondary index.

```js
r.table('marvel').getAll('man_of_steel', {index:'code_name'}).run(conn, callback)
```

[Read more about this command &rarr;](get_all/)


## [between](between/) ##

{% apibody %}
table.between(lowerKey, upperKey
    [, {index:'id', left_bound:'closed', right_bound:'open'}])
        &rarr; selection
{% endapibody %}

Get all documents between two keys. Accepts three optional arguments: `index`,
`left_bound`, and `right_bound`. If `index` is set to the name of a secondary index,
`between` will return all documents where that index's value is in the specified range
(it uses the primary key by default). `left_bound` or `right_bound` may be set to `open`
or `closed` to indicate whether or not to include that endpoint of the range (by default,
`left_bound` is closed and `right_bound` is open).

__Example:__ Find all users with primary key >= 10 and < 20 (a normal half-open interval).

```js
r.table('marvel').between(10, 20).run(conn, callback)
```

[Read more about this command &rarr;](between/)

## [filter](filter/) ##

{% apibody %}
sequence.filter(predicate[, {default: false}]) &rarr; selection
stream.filter(predicate[, {default: false}]) &rarr; stream
array.filter(predicate[, {default: false}]) &rarr; array
{% endapibody %}

Get all the documents for which the given predicate is true.

`filter` can be called on a sequence, selection, or a field containing an array of
elements. The return type is the same as the type on which the function was called on.

The body of every filter is wrapped in an implicit `.default(false)`, which means that
if a non-existence errors is thrown (when you try to access a field that does not exist
in a document), RethinkDB will just ignore the document.
The `default` value can be changed by passing an object with a `default` field.
Setting this optional argument to `r.error()` will cause any non-existence errors to
return a `RqlRuntimeError`.

__Example:__ Get all the users that are 30 years old.

```js
r.table('users').filter({age: 30}).run(conn, callback)
```

[Read more about this command &rarr;](filter/)

{% endapisection %}


{% apisection Joins%}
These commands allow the combination of multiple sequences into a single sequence

## [innerJoin](inner_join/) ##

{% apibody %}
sequence.innerJoin(otherSequence, predicate) &rarr; stream
array.innerJoin(otherSequence, predicate) &rarr; array
{% endapibody %}

Returns the inner product of two sequences (e.g. a table, a filter result) filtered by
the predicate. The query compares each row of the left sequence with each row of the
right sequence to find all pairs of rows which satisfy the predicate. When the predicate
is satisfied, each matched pair of rows of both sequences are combined into a result row.

__Example:__ Construct a sequence of documents containing all cross-universe matchups where a marvel hero would lose.

```js
r.table('marvel').innerJoin(r.table('dc'), function(marvelRow, dcRow) {
    return marvelRow('strength').lt(dcRow('strength'))
}).run(conn, callback)
```


## [outerJoin](outer_join/) ##

{% apibody %}
sequence.outerJoin(otherSequence, predicate) &rarr; stream
array.outerJoin(otherSequence, predicate) &rarr; array
{% endapibody %}

Computes a left outer join by retaining each row in the left table even if no match was
found in the right table.

__Example:__ Construct a sequence of documents containing all cross-universe matchups
where a marvel hero would lose, but keep marvel heroes who would never lose a matchup in
the sequence.

```js
r.table('marvel').outerJoin(r.table('dc'), function(marvelRow, dcRow) {
    return marvelRow('strength').lt(dcRow('strength'))
}).run(conn, callback)
```


## [eqJoin](eq_join/) ##

{% apibody %}
sequence.eqJoin(leftAttr, otherTable[, {index:'id'}]) &rarr; stream
array.eqJoin(leftAttr, otherTable[, {index:'id'}]) &rarr; array
{% endapibody %}

An efficient join that looks up elements in the right table by primary key.

__Example:__ Let our heroes join forces to battle evil!

```js
r.table('marvel').eqJoin('main_dc_collaborator', r.table('dc')).run(conn, callback)
```

[Read more about this command &rarr;](eq_join/)


## [zip](zip/) ##

{% apibody %}
stream.zip() &rarr; stream
array.zip() &rarr; array
{% endapibody %}

Used to 'zip' up the result of a join by merging the 'right' fields into 'left' fields of each member of the sequence.

__Example:__ 'zips up' the sequence by merging the left and right fields produced by a join.

```
r.table('marvel').eqJoin('main_dc_collaborator', r.table('dc'))
    .zip().run(conn, callback)
```



{% endapisection %}

{% apisection Transformations%}
These commands are used to transform data in a sequence.

## [map](map/) ##

{% apibody %}
sequence.map(mappingFunction) &rarr; stream
array.map(mappingFunction) &rarr; array
{% endapibody %}

Transform each element of the sequence by applying the given mapping function.

__Example:__ Construct a sequence of hero power ratings.

```js
r.table('marvel').map(function(hero) {
    return hero('combatPower').add(hero('compassionPower').mul(2))
}).run(conn, callback)
```


## [withFields](with_fields/) ##

{% apibody %}
sequence.withFields([selector1, selector2...]) &rarr; stream
array.withFields([selector1, selector2...]) &rarr; array
{% endapibody %}

Takes a sequence of objects and a list of fields. If any objects in the sequence don't
have all of the specified fields, they're dropped from the sequence. The remaining
objects have the specified fields plucked out. (This is identical to `has_fields`
followed by `pluck` on a sequence.)

__Example:__ Get a list of heroes and their nemeses, excluding any heroes that lack one.

```js
r.table('marvel').withFields('id', 'nemesis')
```

[Read more about this command &rarr;](with_fields/)

## [concatMap](concat_map/) ##

{% apibody %}
sequence.concatMap(mappingFunction) &rarr; stream
array.concatMap(mappingFunction) &rarr; array
{% endapibody %}

Flattens a sequence of arrays returned by the mappingFunction into a single sequence.

__Example:__ Construct a sequence of all monsters defeated by Marvel heroes. Here the field
'defeatedMonsters' is a list that is concatenated to the sequence.

```js
r.table('marvel').concatMap(function(hero) {
    return hero('defeatedMonsters')
}).run(conn, callback)
```


## [orderBy](order_by/) ##

{% apibody %}
table.orderBy([key1...], {index: index_name}) -> selection<stream>
selection.orderBy(key1, [key2...]) -> selection<array>
sequence.orderBy(key1, [key2...]) -> array
{% endapibody %}

Sort the sequence by document values of the given key(s). `orderBy` defaults to ascending
ordering. To explicitly specify the ordering, wrap the attribute with either `r.asc` or
`r.desc`.

__Example:__ Order our heroes by a series of performance metrics.

```js
r.table('marvel').orderBy('enemiesVanquished', 'damselsSaved').run(conn, callback)
```

[Read more about this command &rarr;](order_by/)

## [skip](skip/) ##

{% apibody %}
sequence.skip(n) &rarr; stream
array.skip(n) &rarr; array
{% endapibody %}

Skip a number of elements from the head of the sequence.

__Example:__ Here in conjunction with `order_by` we choose to ignore the most successful heroes.

```js
r.table('marvel').orderBy('successMetric').skip(10).run(conn, callback)
```


## [limit](limit/) ##

{% apibody %}
sequence.limit(n) &rarr; stream
array.limit(n) &rarr; array
{% endapibody %}


End the sequence after the given number of elements.

__Example:__ Only so many can fit in our Pantheon of heroes.

```js
r.table('marvel').orderBy('belovedness').limit(10).run(conn, callback)
```

## [slice](slice/) ##

{% apibody %}
sequence.slice(startIndex[, endIndex]) &rarr; stream
array.slice(startIndex[, endIndex]) &rarr; array
{% endapibody %}

Trim the sequence to within the bounds provided.

__Example:__ For this fight, we need heroes with a good mix of strength and agility.

```js
r.table('marvel').orderBy('strength').slice(5, 10).run(conn, callback)
```

## [nth](nth/) ##

{% apibody %}
sequence.nth(index) &rarr; object
{% endapibody %}

Get the nth element of a sequence.

__Example:__ Select the second element in the array.

```js
r.expr([1,2,3]).nth(1).run(conn, callback)
```


## [indexesOf](indexes_of/) ##

{% apibody %}
sequence.indexesOf(datum | predicate) &rarr; array
{% endapibody %}

Get the indexes of an element in a sequence. If the argument is a predicate, get the indexes of all elements matching it.

__Example:__ Find the position of the letter 'c'.

```js
r.expr(['a','b','c']).indexesOf('c').run(conn, callback)
```

[Read more about this command &rarr;](indexes_of/)


## [isEmpty](is_empty/) ##

{% apibody %}
sequence.isEmpty() &rarr; bool
{% endapibody %}

Test if a sequence is empty.

__Example:__ Are there any documents in the marvel table?

```js
r.table('marvel').isEmpty().run(conn, callback)
```

## [union](union/) ##

{% apibody %}
sequence.union(sequence) &rarr; array
{% endapibody %}

Concatenate two sequences.

__Example:__ Construct a stream of all heroes.

```js
r.table('marvel').union(r.table('dc')).run(conn, callback)
```


## [sample](sample/) ##

{% apibody %}
sequence.sample(number) &rarr; selection
stream.sample(number) &rarr; array
array.sample(number) &rarr; array
{% endapibody %}

Select a given number of elements from a sequence with uniform random distribution. Selection is done without replacement.

__Example:__ Select 3 random heroes.

```js
r.table('marvel').sample(3).run(conn, callback)
```


{% endapisection %}


{% apisection Aggregation%}
These commands are used to compute smaller values from large sequences.


## [group](group/) ##

{% apibody %}
sequence.group(fieldOrFunction..., [{index: "indexName"}) &rarr; grouped_stream
{% endapibody %}

Takes a stream and partitions it into multiple groups based on the
fields or functions provided.  Commands chained after `group` will be
called on each of these grouped sub-streams, producing grouped data.

__Example:__ What is each player's best game?

```js
r.table('games').group('player').max('points').run(conn, callback)
```

[Read more about this command &rarr;](group/)


## [ungroup](ungroup/) ##

{% apibody %}
grouped_stream.ungroup() &rarr; array
grouped_data.ungroup() &rarr; array
{% endapibody %}

Takes a grouped stream or grouped data and turns it into an array of
objects representing the groups.  Any commands chained after `ungroup`
will operate on this array, rather than operating on each group
individually.  This is useful if you want to e.g. order the groups by
the value of their reduction.

__Example:__ What is the maximum number of points scored by each
player, with the highest scorers first?

```js
r.table('games')
    .group('player').max('points')['points']
    .ungroup().order_by(r.desc('reduction')).run(conn)
```

[Read more about this command &rarr;](ungroup/)




## [reduce](reduce/) ##

{% apibody %}
sequence.reduce(reductionFunction) &rarr; value
{% endapibody %}

Produce a single value from a sequence through repeated application of a reduction
function.

__Example:__ Return the number of documents in the table `posts.

```js
r.table("posts").map(function(doc) {
    return 1
}).reduce(function(left, right) {
    return left.add(right)
}).run(conn, callback);
```

[Read more about this command &rarr;](reduce/)

## [count](count/) ##

{% apibody %}
sequence.count([filter]) &rarr; number
{% endapibody %}

Count the number of elements in the sequence. With a single argument, count the number
of elements equal to it. If the argument is a function, it is equivalent to calling
filter before count.

__Example:__ Just how many super heroes are there?

```js
r.table('marvel').count().add(r.table('dc').count()).run(conn, callback)
```

[Read more about this command &rarr;](count/)



## [sum](sum/) ##

{% apibody %}
sequence.sum([fieldOrFunction]) &rarr; number
{% endapibody %}

Sums all the elements of a sequence.  If called with a field name,
sums all the values of that field in the sequence, skipping elements
of the sequence that lack that field.  If called with a function,
calls that function on every element of the sequence and sums the
results, skipping elements of the sequence where that function returns
`null` or a non-existence error.

__Example:__ What's 3 + 5 + 7?

```js
r.expr([3, 5, 7]).sum().run(conn, callback)
```

[Read more about this command &rarr;](sum/)


## [avg](avg/) ##

{% apibody %}
sequence.avg([fieldOrFunction]) &rarr; number
{% endapibody %}

Averages all the elements of a sequence.  If called with a field name,
averages all the values of that field in the sequence, skipping
elements of the sequence that lack that field.  If called with a
function, calls that function on every element of the sequence and
averages the results, skipping elements of the sequence where that
function returns `null` or a non-existence error.


__Example:__ What's the average of 3, 5, and 7?

```js
r.expr([3, 5, 7]).avg().run(conn, callback)
```

[Read more about this command &rarr;](avg/)


## [min](min/) ##

{% apibody %}
sequence.min([fieldOrFunction]) &rarr; element
{% endapibody %}

Finds the minimum of a sequence.  If called with a field name, finds
the element of that sequence with the smallest value in that field.
If called with a function, calls that function on every element of the
sequence and returns the element which produced the smallest value,
ignoring any elements where the function returns `null` or produces a
non-existence error.

__Example:__ What's the minimum of 3, 5, and 7?

```js
r.expr([3, 5, 7]).min().run(conn, callback)
```


[Read more about this command &rarr;](min/)



## [max](max/) ##

{% apibody %}
sequence.max([fieldOrFunction]) &rarr; element
{% endapibody %}

Finds the maximum of a sequence.  If called with a field name, finds
the element of that sequence with the largest value in that field.  If
called with a function, calls that function on every element of the
sequence and returns the element which produced the largest value,
ignoring any elements where the function returns `null` or produces a
non-existence error.


__Example:__ What's the maximum of 3, 5, and 7?

```js
r.expr([3, 5, 7]).max().run(conn, callback)
```

[Read more about this command &rarr;](max/)



## [distinct](distinct/) ##

{% apibody %}
sequence.distinct() &rarr; array
{% endapibody %}

Remove duplicate elements from the sequence.

__Example:__ Which unique villains have been vanquished by marvel heroes?

```js
r.table('marvel').concatMap(function(hero) {return hero('villainList')}).distinct()
    .run(conn, callback)
```

[Read more about this command &rarr;](distinct/)


## [contains](contains/) ##

{% apibody %}
sequence.contains(value1[, value2...]) &rarr; bool
{% endapibody %}

Returns whether or not a sequence contains all the specified values, or if functions are
provided instead, returns whether or not a sequence contains values matching all the
specified functions.

__Example:__ Has Iron Man ever fought Superman?

```js
r.table('marvel').get('ironman')('opponents').contains('superman').run(conn, callback)
```

[Read more about this command &rarr;](contains/)



{% endapisection %}


{% apisection Document manipulation%}

## [row](row/) ##

{% apibody %}
r.row &rarr; value
{% endapibody %}

Returns the currently visited document.

__Example:__ Get all users whose age is greater than 5.

```js
r.table('users').filter(r.row('age').gt(5)).run(conn, callback)
```

[Read more about this command &rarr;](row/)


## [pluck](pluck/) ##

{% apibody %}
sequence.pluck([selector1, selector2...]) &rarr; stream
array.pluck([selector1, selector2...]) &rarr; array
object.pluck([selector1, selector2...]) &rarr; object
singleSelection.pluck([selector1, selector2...]) &rarr; object
{% endapibody %}

Plucks out one or more attributes from either an object or a sequence of objects
(projection).

__Example:__ We just need information about IronMan's reactor and not the rest of the
document.

```js
r.table('marvel').get('IronMan').pluck('reactorState', 'reactorPower').run(conn, callback)
```

[Read more about this command &rarr;](pluck/)

## [without](without/) ##

{% apibody %}
sequence.without([selector1, selector2...]) &rarr; stream
array.without([selector1, selector2...]) &rarr; array
singleSelection.without([selector1, selector2...]) &rarr; object
object.without([selector1, selector2...]) &rarr; object
{% endapibody %}

The opposite of pluck; takes an object or a sequence of objects, and returns them with
the specified paths removed.

__Example:__ Since we don't need it for this computation we'll save bandwidth and leave
out the list of IronMan's romantic conquests.

```js
r.table('marvel').get('IronMan').without('personalVictoriesList').run(conn, callback)
```

[Read more about this command &rarr;](without/)

## [merge](merge/) ##

{% apibody %}
singleSelection.merge(object) &rarr; object
object.merge(object) &rarr; object
sequence.merge(object) &rarr; stream
array.merge(object) &rarr; array
{% endapibody %}

Merge two objects together to construct a new object with properties from both. Gives preference to attributes from other when there is a conflict.

__Example:__ Equip IronMan for battle.

```js
r.table('marvel').get('IronMan').merge(
    r.table('loadouts').get('alienInvasionKit')
).run(conn, callback)
```

[Read more about this command &rarr;](merge/)


## [append](append/) ##

{% apibody %}
array.append(value) &rarr; array
{% endapibody %}

Append a value to an array.

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```js
r.table('marvel').get('IronMan')('equipment').append('newBoots').run(conn, callback)
```


## [prepend](prepend/) ##

{% apibody %}
array.prepend(value) &rarr; array
{% endapibody %}

Prepend a value to an array.

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```js
r.table('marvel').get('IronMan')('equipment').prepend('newBoots').run(conn, callback)
```


## [difference](difference/) ##

{% apibody %}
array.difference(array) &rarr; array
{% endapibody %}

Remove the elements of one array from another array.

__Example:__ Retrieve Iron Man's equipment list without boots.

```js
r.table('marvel').get('IronMan')('equipment').difference(['Boots']).run(conn, callback)
```


## [setInsert](set_insert/) ##

{% apibody %}
array.setInsert(value) &rarr; array
{% endapibody %}

Add a value to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```js
r.table('marvel').get('IronMan')('equipment').setInsert('newBoots').run(conn, callback)
```


## [setUnion](set_union/) ##

{% apibody %}
array.setUnion(array) &rarr; array
{% endapibody %}

Add a several values to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots and an arc reactor.

```js
r.table('marvel').get('IronMan')('equipment').setUnion(['newBoots', 'arc_reactor']).run(conn, callback)
```


## [setIntersection](set_intersection/) ##

{% apibody %}
array.setIntersection(array) &rarr; array
{% endapibody %}

Intersect two arrays returning values that occur in both of them as a set (an array with
distinct values).

__Example:__ Check which pieces of equipment Iron Man has from a fixed list.

```js
r.table('marvel').get('IronMan')('equipment').setIntersection(['newBoots', 'arc_reactor']).run(conn, callback)
```


## [setDifference](set_difference/) ##

{% apibody %}
array.setDifference(array) &rarr; array
{% endapibody %}

Remove the elements of one array from another and return them as a set (an array with
distinct values).

__Example:__ Check which pieces of equipment Iron Man has, excluding a fixed list.

```js
r.table('marvel').get('IronMan')('equipment').setDifference(['newBoots', 'arc_reactor']).run(conn, callback)
```


## [()](get_field/) ##

{% apibody %}
sequence(attr) &rarr; sequence
singleSelection(attr) &rarr; value
object(attr) &rarr; value
{% endapibody %}

Get a single field from an object. If called on a sequence, gets that field from every
object in the sequence, skipping objects that lack it.

__Example:__ What was Iron Man's first appearance in a comic?

```js
r.table('marvel').get('IronMan')('firstAppearance').run(conn, callback)
```


## [hasFields](has_fields/) ##

{% apibody %}
sequence.hasFields([selector1, selector2...]) &rarr; stream
array.hasFields([selector1, selector2...]) &rarr; array
singleSelection.hasFields([selector1, selector2...]) &rarr; boolean
object.hasFields([selector1, selector2...]) &rarr; boolean
{% endapibody %}

Test if an object has all of the specified fields. An object has a field if it has the
specified key and that key maps to a non-null value. For instance, the object
`{'a':1,'b':2,'c':null}` has the fields `a` and `b`.

__Example:__ Which heroes are married?

```js
r.table('marvel').hasFields('spouse')
```

[Read more about this command &rarr;](has_fields/)


## [insertAt](insert_at/) ##

{% apibody %}
array.insertAt(index, value) &rarr; array
{% endapibody %}

Insert a value in to an array at a given index. Returns the modified array.

__Example:__ Hulk decides to join the avengers.

```js
r.expr(["Iron Man", "Spider-Man"]).insertAt(1, "Hulk").run(conn, callback)
```


## [spliceAt](splice_at/) ##

{% apibody %}
array.spliceAt(index, array) &rarr; array
{% endapibody %}

Insert several values in to an array at a given index. Returns the modified array.

__Example:__ Hulk and Thor decide to join the avengers.

```js
r.expr(["Iron Man", "Spider-Man"]).spliceAt(1, ["Hulk", "Thor"]).run(conn, callback)
```


## [deleteAt](delete_at/) ##

{% apibody %}
array.deleteAt(index [,endIndex]) &rarr; array
{% endapibody %}

Remove an element from an array at a given index. Returns the modified array.

__Example:__ Hulk decides to leave the avengers.

```js
r.expr(["Iron Man", "Hulk", "Spider-Man"]).deleteAt(1).run(conn, callback)
```

[Read more about this command &rarr;](delete_at/)

## [changeAt](change_at/) ##

{% apibody %}
array.changeAt(index, value) &rarr; array
{% endapibody %}

Change a value in an array at a given index. Returns the modified array.

__Example:__ Bruce Banner hulks out.

```js
r.expr(["Iron Man", "Bruce", "Spider-Man"]).changeAt(1, "Hulk").run(conn, callback)
```

## [keys](keys/) ##

{% apibody %}
singleSelection.keys() &rarr; array
object.keys() &rarr; array
{% endapibody %}

Return an array containing all of the object's keys.

__Example:__ Get all the keys of a row.

```js
r.table('marvel').get('ironman').keys().run(conn, callback)
```

## [object](object/) ##

{% apibody %}
r.object([key, value,]...) &rarr; object
{% endapibody %}

Creates an object from a list of key-value pairs, where the keys must
be strings.  `r.object(A, B, C, D)` is equivalent to
`r.expr([[A, B], [C, D]]).coerce_to('OBJECT')`.

__Example:__ Create a simple object.

```js
r.object('id', 5, 'data', ['foo', 'bar']).run(conn, callback)
```

{% endapisection %}


{% apisection String manipulation%}
These commands provide string operators.

## [match](match/) ##

{% apibody %}
string.match(regexp) &rarr; null/object
{% endapibody %}

Matches against a regular expression. If there is a match, returns an object with the fields:

- `str`: The matched string
- `start`: The matched string's start
- `end`: The matched string's end
- `groups`: The capture groups defined with parentheses

If no match is found, returns `null`.

__Example:__ Get all users whose name starts with "A". 

```js
r.table('users').filter(function(doc){
    return doc('name').match("^A")
}).run(conn, callback)
```



[Read more about this command &rarr;](match/)

## [split](split/) ##

{% apibody %}
string.split([separator, [max_splits]]) &rarr; array
{% endapibody %}

Splits a string into substrings.  Splits on whitespace when called
with no arguments.  When called with a separator, splits on that
separator.  When called with a separator and a maximum number of
splits, splits on that separator at most `max_splits` times.  (Can be
called with `null` as the separator if you want to split on whitespace
while still specifying `max_splits`.)

Mimics the behavior of Python's `string.split` in edge cases, except
for splitting on the empty string, which instead produces an array of
single-character strings.

__Example:__ Split on whitespace.

```js
r.expr("foo  bar bax").split().run(conn, callback)
```

[Read more about this command &rarr;](split/)

## [upcase](upcase/) ##

{% apibody %}
string.upcase() &rarr; string
{% endapibody %}


Upcases a string.

__Example:__

```js
r.expr("Sentence about LaTeX.").upcase().run(conn, callback)
```

## [downcase](downcase/) ##

{% apibody %}
string.downcase() &rarr; string
{% endapibody %}

Downcases a string.

__Example:__

```js
r.expr("Sentence about LaTeX.").downcase().run(conn, callback)
```

{% endapisection %}


{% apisection Math and logic%}

## [add](add/) ##

{% apibody %}
number.add(number) &rarr; number
string.add(string) &rarr; string
array.add(array) &rarr; array
time.add(number) &rarr; time
{% endapibody %}

Sum two numbers, concatenate two strings, or concatenate 2 arrays.

__Example:__ It's as easy as 2 + 2 = 4.

```js
r.expr(2).add(2).run(conn, callback)
```


[Read more about this command &rarr;](add/)

## [sub](sub/) ##

{% apibody %}
number.sub(number) &rarr; number
time.sub(time) &rarr; number
time.sub(number) &rarr; time
{% endapibody %}

Subtract two numbers.

__Example:__ It's as easy as 2 - 2 = 0.

```js
r.expr(2).sub(2).run(conn, callback)
```

[Read more about this command &rarr;](sub/)


## [mul](mul/) ##

{% apibody %}
number.mul(number) &rarr; number
array.mul(number) &rarr; array
{% endapibody %}

Multiply two numbers, or make a periodic array.

__Example:__ It's as easy as 2 * 2 = 4.

```js
r.expr(2).mul(2).run(conn, callback)
```

[Read more about this command &rarr;](mul/)


## [div](div/) ##

{% apibody %}
number.div(number) &rarr; number
{% endapibody %}

Divide two numbers.

__Example:__ It's as easy as 2 / 2 = 1.

```js
r.expr(2).div(2).run(conn, callback)
```



## [mod](mod/) ##

{% apibody %}
number.mod(number) &rarr; number
{% endapibody %}

Find the remainder when dividing two numbers.

__Example:__ It's as easy as 2 % 2 = 0.

```js
r.expr(2).mod(2).run(conn, callback)
```

## [and](and/) ##

{% apibody %}
bool.and(bool) &rarr; bool
{% endapibody %}

Compute the logical and of two values.

__Example:__ True and false anded is false?

```js
r.expr(true).and(false).run(conn, callback)
```


## [or](or/) ##

{% apibody %}
bool.or(bool) &rarr; bool
{% endapibody %}

Compute the logical or of two values.

__Example:__ True or false ored is true?

```js
r.expr(true).or(false).run(conn, callback)
```


## [eq](eq/) ##

{% apibody %}
value.eq(value) &rarr; bool
{% endapibody %}

Test if two values are equal.

__Example:__ Does 2 equal 2?

```js
r.expr(2).eq(2).run(conn, callback)
```


## [ne](ne/) ##

{% apibody %}
value.ne(value) &rarr; bool
{% endapibody %}

Test if two values are not equal.

__Example:__ Does 2 not equal 2?

```js
r.expr(2).ne(2).run(conn, callback)
```


## [gt](gt/) ##

{% apibody %}
value.gt(value) &rarr; bool
{% endapibody %}

Test if the first value is greater than other.

__Example:__ Is 2 greater than 2?

```js
r.expr(2).gt(2).run(conn, callback)
```

## [ge](ge/) ##

{% apibody %}
value.ge(value) &rarr; bool
{% endapibody %}

Test if the first value is greater than or equal to other.

__Example:__ Is 2 greater than or equal to 2?

```js
r.expr(2).ge(2).run(conn, callback)
```

## [lt](lt/) ##

{% apibody %}
value.lt(value) &rarr; bool
{% endapibody %}

Test if the first value is less than other.

__Example:__ Is 2 less than 2?

```js
r.expr(2).lt(2).run(conn, callback)
```

## [le](le/) ##

{% apibody %}
value.le(value) &rarr; bool
{% endapibody %}

Test if the first value is less than or equal to other.

__Example:__ Is 2 less than or equal to 2?

```js
r.expr(2).le(2).run(conn, callback)
```


## [not](not/) ##

{% apibody %}
bool.not() &rarr; bool
{% endapibody %}
Compute the logical inverse (not).

__Example:__ Not true is false.

```js
r.expr(true).not().run(conn, callback)
```


{% endapisection %}


{% apisection Dates and times%}

## [now](now/) ##

{% apibody %}
r.now() &rarr; time
{% endapibody %}

Return a time object representing the current time in UTC. The command now() is computed once when the server receives the query, so multiple instances of r.now() will always return the same time inside a query.

__Example:__ Add a new user with the time at which he subscribed.

```js
r.table("users").insert({
    name: "John",
    subscription_date: r.now()
}).run(conn, callback)
```

## [time](time/) ##

{% apibody %}
r.time(year, month, day[, hour, minute, second], timezone)
    &rarr; time
{% endapibody %}

Create a time object for a specific time.

A few restrictions exist on the arguments:

- `year` is an integer between 1400 and 9,999.
- `month` is an integer between 1 and 12.
- `day` is an integer between 1 and 31.
- `hour` is an integer.
- `minutes` is an integer.
- `seconds` is a double. Its value will be rounded to three decimal places
(millisecond-precision).
- `timezone` can be `'Z'` (for UTC) or a string with the format `±[hh]:[mm]`.

__Example:__ Update the birthdate of the user "John" to November 3rd, 1986 UTC.

```js
r.table("user").get("John").update({birthdate: r.time(1986, 11, 3, 'Z')})
    .run(conn, callback)
```



## [epochTime](epoch_time/) ##

{% apibody %}
r.epochTime(epochTime) &rarr; time
{% endapibody %}

Create a time object based on seconds since epoch. The first argument is a double and
will be rounded to three decimal places (millisecond-precision).

__Example:__ Update the birthdate of the user "John" to November 3rd, 1986.

```js
r.table("user").get("John").update({birthdate: r.epochTime(531360000)})
    .run(conn, callback)
```


## [ISO8601](iso8601/) ##

{% apibody %}
r.ISO8601(iso8601Date[, {default_timezone:''}]) &rarr; time
{% endapibody %}

Create a time object based on an iso8601 date-time string (e.g.
'2013-01-01T01:01:01+00:00'). We support all valid ISO 8601 formats except for week
dates. If you pass an ISO 8601 date-time without a time zone, you must specify the time
zone with the optarg `default_timezone`. Read more about the ISO 8601 format on the
Wikipedia page.

__Example:__ Update the time of John's birth.

```js
r.table("user").get("John").update({birth: r.ISO8601('1986-11-03T08:30:00-07:00')}).run(conn, callback)
```


## [inTimezone](in_timezone/) ##

{% apibody %}
time.inTimezone(timezone) &rarr; time
{% endapibody %}

Return a new time object with a different timezone. While the time stays the same, the results returned by methods such as hours() will change since they take the timezone into account. The timezone argument has to be of the ISO 8601 format.

__Example:__ Hour of the day in San Francisco (UTC/GMT -8, without daylight saving time).

```js
r.now().inTimezone('-08:00').hours().run(conn, callback)
```



## [timezone](timezone/) ##

{% apibody %}
time.timezone() &rarr; string
{% endapibody %}

Return the timezone of the time object.

__Example:__ Return all the users in the "-07:00" timezone.

```js
r.table("users").filter( function(user) {
    return user("subscriptionDate").timezone().eq("-07:00")
})
```


## [during](during/) ##

{% apibody %}
time.during(startTime, endTime[, options]) &rarr; bool
{% endapibody %}

Return if a time is between two other times (by default, inclusive for the start, exclusive for the end).

__Example:__ Retrieve all the posts that were posted between December 1st, 2013 (inclusive) and December 10th, 2013 (exclusive).

```js
r.table("posts").filter(
    r.row('date').during(r.time(2013, 12, 1), r.time(2013, 12, 10))
).run(conn, callback)
```

[Read more about this command &rarr;](during/)



## [date](date/) ##

{% apibody %}
time.date() &rarr; time
{% endapibody %}

Return a new time object only based on the day, month and year (ie. the same day at 00:00).

__Example:__ Retrieve all the users whose birthday is today

```js
r.table("users").filter(function(user) {
    return user("birthdate").date().eq(r.now().date())
}).run(conn, callback)
```



## [timeOfDay](time_of_day/) ##

{% apibody %}
time.timeOfDay() &rarr; number
{% endapibody %}

Return the number of seconds elapsed since the beginning of the day stored in the time object.

__Example:__ Retrieve posts that were submitted before noon.

```js
r.table("posts").filter(
    r.row("date").timeOfDay().le(12*60*60)
).run(conn, callback)
```


## [year](year/) ##

{% apibody %}
time.year() &rarr; number
{% endapibody %}

Return the year of a time object.

__Example:__ Retrieve all the users born in 1986.

```js
r.table("users").filter(function(user) {
    return user("birthdate").year().eq(1986)
}).run(conn, callback)
```


## [month](month/) ##

{% apibody %}
time.month() &rarr; number
{% endapibody %}

Return the month of a time object as a number between 1 and 12. For your convenience, the terms r.january, r.february etc. are defined and map to the appropriate integer.

__Example:__ Retrieve all the users who were born in November.

```js
r.table("users").filter(
    r.row("birthdate").month().eq(11)
)
```

[Read more about this command &rarr;](month/)


## [day](day/) ##

{% apibody %}
time.day() &rarr; number
{% endapibody %}

Return the day of a time object as a number between 1 and 31.

__Example:__ Return the users born on the 24th of any month.

```js
r.table("users").filter(
    r.row("birthdate").day().eq(24)
).run(conn, callback)
```



## [dayOfWeek](day_of_week/) ##

{% apibody %}
time.dayOfWeek() &rarr; number
{% endapibody %}

Return the day of week of a time object as a number between 1 and 7 (following ISO 8601 standard). For your convenience, the terms r.monday, r.tuesday etc. are defined and map to the appropriate integer.

__Example:__ Return today's day of week.

```js
r.now().dayOfWeek().run(conn, callback)
```

[Read more about this command &rarr;](day_of_week/)



## [dayOfYear](day_of_year/) ##

{% apibody %}
time.dayOfYear() &rarr; number
{% endapibody %}

Return the day of the year of a time object as a number between 1 and 366 (following ISO 8601 standard).

__Example:__ Retrieve all the users who were born the first day of a year.

```js
r.table("users").filter(
    r.row("birthdate").dayOfYear().eq(1)
)
```


## [hours](hours/) ##

{% apibody %}
time.hours() &rarr; number
{% endapibody %}

Return the hour in a time object as a number between 0 and 23.

__Example:__ Return all the posts submitted after midnight and before 4am.

```js
r.table("posts").filter(function(post) {
    return post("date").hours().lt(4)
})
```


## [minutes](minutes/) ##

{% apibody %}
time.minutes() &rarr; number
{% endapibody %}

Return the minute in a time object as a number between 0 and 59.

__Example:__ Return all the posts submitted during the first 10 minutes of every hour.

```js
r.table("posts").filter(function(post) {
    return post("date").minutes().lt(10)
})
```



## [seconds](seconds/) ##

{% apibody %}
time.seconds() &rarr; number
{% endapibody %}

Return the seconds in a time object as a number between 0 and 59.999 (double precision).

__Example:__ Return the post submitted during the first 30 seconds of every minute.

```js
r.table("posts").filter(function(post) {
    return post("date").seconds().lt(30)
})
```

## [toISO8601](to_iso8601/) ##

{% apibody %}
time.toISO8601() &rarr; string
{% endapibody %}

Convert a time object to its iso 8601 format.

__Example:__ Return the current time in an ISO8601 format.

```js
r.now().toISO8601()
```


## [toEpochTime](to_epoch_time/) ##

{% apibody %}
time.toEpochTime() &rarr; number
{% endapibody %}

Convert a time object to its epoch time.

__Example:__ Return the current time in an ISO8601 format.

```js
r.now().toEpochTime()
```



{% endapisection %}


{% apisection Control structures%}

## [do](do/) ##

{% apibody %}
any.do(arg [, args]*, expr) &rarr; any
{% endapibody %}

Evaluate the expr in the context of one or more value bindings.

The type of the result is the type of the value returned from expr.

__Example:__ The object(s) passed to do() can be bound to name(s). The last argument is the expression to evaluate in the context of the bindings.

```js
r.do(r.table('marvel').get('IronMan'),
    function (ironman) { return ironman('name'); }
).run(conn, callback)
```


## [branch](branch/) ##

{% apibody %}
r.branch(test, true_branch, false_branch) &rarr; any
{% endapibody %}

If the `test` expression returns `false` or `null`, the `false_branch` will be evaluated.
Otherwise, the `true_branch` will be evaluated.

The `branch` command is effectively an `if` renamed due to language constraints.
The type of the result is determined by the type of the branch that gets executed.

__Example:__ Return heroes and superheroes.

```js
r.table('marvel').map(
    r.branch(
        r.row('victories').gt(100),
        r.row('name').add(' is a superhero'),
        r.row('name').add(' is a hero')
    )
).run(conn, callback)
```

## [forEach](for_each/) ##

{% apibody %}
sequence.forEach(write_query) &rarr; object
{% endapibody %}

Loop over a sequence, evaluating the given write query for each element.

__Example:__ Now that our heroes have defeated their villains, we can safely remove them from the villain table.

```js
r.table('marvel').forEach(function(hero) {
    return r.table('villains').get(hero('villainDefeated')).delete()
}).run(conn, callback)
```



## [error](error/) ##

{% apibody %}
r.error(message) &rarr; error
{% endapibody %}

Throw a runtime error. If called with no arguments inside the second argument to `default`, re-throw the current error.

__Example:__ Iron Man can't possibly have lost a battle:

```js
r.table('marvel').get('IronMan').do(function(ironman) {
    return r.branch(ironman('victories').lt(ironman('battles')),
        r.error('impossible code path'),
        ironman)
}).run(conn, callback)
```

## [default](default/) ##

{% apibody %}
value.default(default_value) &rarr; any
sequence.default(default_value) &rarr; any
{% endapibody %}

Handle non-existence errors. Tries to evaluate and return its first argument. If an
error related to the absence of a value is thrown in the process, or if its first
argument returns `null`, returns its second argument. (Alternatively, the second argument
may be a function which will be called with either the text of the non-existence error
or `null`.)


__Exmple:__ Suppose we want to retrieve the titles and authors of the table `posts`.
In the case where the author field is missing or `null`, we want to retrieve the string
`Anonymous`.


```js
r.table("posts").map( function(post) {
    return {
        title: post("title"),
        author: post("author").default("Anonymous")
    }
}).run(conn, callback)
```

[Read more about this command &rarr;](default/)

## [expr](expr/) ##

{% apibody %}
r.expr(value) &rarr; value
{% endapibody %}

Construct a ReQL JSON object from a native object.

__Example:__ Objects wrapped with `expr` can then be manipulated by ReQL API functions.

```js
r.expr({a:'b'}).merge({b:[1,2,3]}).run(conn, callback)
```

[Read more about this command &rarr;](expr/)

## [js](js/) ##

{% apibody %}
r.js(jsString) &rarr; value
{% endapibody %}

Create a javascript expression.

__Example:__ Concatenate two strings using Javascript'

```js
r.js("'str1' + 'str2'").run(conn, callback)
```

[Read more about this command &rarr;](js/)

## [coerceTo](coerce_to/) ##

{% apibody %}
sequence.coerceTo(typeName) &rarr; array
value.coerceTo(typeName) &rarr; string
array.coerceTo(typeName) &rarr; object
object.coerceTo(typeName) &rarr; array
{% endapibody %}

Converts a value of one type into another.

You can convert: a selection, sequence, or object into an ARRAY, an array of pairs into an OBJECT, and any DATUM into a STRING.

__Example:__ Convert a table to an array.

```js
r.table('marvel').coerceTo('array').run(conn, callback)
```

[Read more about this command &rarr;](coerce_to/)

## [typeOf](type_of/) ##

{% apibody %}
any.typeOf() &rarr; string
{% endapibody %}

Gets the type of a value.

__Example:__ Get the type of a string.

```js
r.expr("foo").typeOf().run(conn, callback)
```

## [info](info/) ##

{% apibody %}
any.info() &rarr; object
{% endapibody %}

Get information about a ReQL value.

__Example:__ Get information about a table such as primary key, or cache size.

```js
r.table('marvel').info().run(conn, callback)
```

## [json](json/) ##

{% apibody %}
r.json(json_string) &rarr; value
{% endapibody %}

Parse a JSON string on the server.

__Example:__ Send an array to the server'

```js
r.json("[1,2,3]").run(conn, callback)
```


{% endapisection %}






