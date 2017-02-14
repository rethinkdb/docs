---
layout: api
title: "ReQL command reference"
active: api
no_footer: true
permalink: api/javascript/
language: JavaScript
alias: api/
---

{% apisection Accessing ReQL %}

## [r](r/) ##

{% apibody %}
r &rarr; r
{% endapibody %}

The top-level ReQL namespace.

__Example:__ Set up your top-level namespace.

```javascript
var r = require('rethinkdb');
```

[Read more about this command &rarr;](r/)

## [connect](connect/) ##

{% apibody %}
r.connect([options, ]callback)
r.connect([host, ]callback)
r.connect([options]) &rarr; promise
r.connect([host]) &rarr; promise

{% endapibody %}

Create a new connection to the database server. Accepts the following
options:

- `host`: the host to connect to (default `localhost`).
- `port`: the port to connect on (default `28015`).
- `db`: the default database (default `test`).
- `user`: the user account to connect as (default `admin`).
- `password`: the password for the user account to connect as (default `''`, empty).
- `timeout`: timeout period in seconds for the connection to be opened (default `20`).
- `ssl`: a hash of options to support SSL connections (default `null`). Currently, there is only one option available, and if the `ssl` option is specified, this key is required:
    - `ca`: a list of [Node.js](http://nodejs.org) `Buffer` objects containing SSL CA certificates.

If the connection cannot be established, a `ReqlDriverError` will be passed to the callback instead of a connection.

__Example:__ Open a connection using the default host and port, specifying the default database.

```javascript
r.connect({
    db: 'marvel'
}, function(err, conn) {
    // ...
});
```

If no callback is provided, a promise will be returned.

```javascript
var promise = r.connect({db: 'marvel'});
```

[Read more about this command &rarr;](connect/)

## [close](close/) ##

{% apibody %}
conn.close([{noreplyWait: true}, ]callback)
conn.close([{noreplyWait: true}]) &rarr; promise
{% endapibody %}

Close an open connection. If no callback is provided, a promise will be returned.

__Example:__ Close an open connection, waiting for noreply writes to finish.

```javascript
conn.close(function(err) { if (err) throw err; })
```

[Read more about this command &rarr;](close/)

## [reconnect](reconnect/) ##

{% apibody %}
conn.reconnect([{noreplyWait: true}, ]callback)
conn.reconnect([{noreplyWait: true}]) &rarr; promise
{% endapibody %}

Close and reopen a connection. If no callback is provided, a promise will be returned.

__Example:__ Cancel outstanding requests/queries that are no longer needed.

```javascript
conn.reconnect({noreplyWait: false}, function(error, connection) { ... })
```

[Read more about this command &rarr;](reconnect/)

## [use](use/) ##

{% apibody %}
conn.use(dbName)
{% endapibody %}

Change the default database on this connection.

__Example:__ Change the default database so that we don't need to
specify the database when referencing a table.

```javascript
conn.use('marvel')
r.table('heroes').run(conn, ...) // refers to r.db('marvel').table('heroes')
```

[Read more about this command &rarr;](use/)

## [run](run/) ##

{% apibody %}
query.run(conn[, options], callback)
query.run(conn[, options]) &rarr; promise
{% endapibody %}

Run a query on a connection. The callback will get either an error, a single JSON
result, or a cursor, depending on the query.

__Example:__ Run a query on the connection `conn` and log each row in
the result to the console.

```javascript
r.table('marvel').run(conn, function(err, cursor) {
    cursor.each(console.log);
})
```

[Read more about this command &rarr;](run/)

## [changes](changes/) ##

{% apibody %}
stream.changes([options]) &rarr; stream
singleSelection.changes([options]) &rarr; stream
{% endapibody %}

Turn a query into a changefeed, an infinite stream of objects representing changes to the query's results as they occur. A changefeed may return changes to a table or an individual document (a "point" changefeed). Commands such as `filter` or `map` may be used before the `changes` command to transform or filter the output, and many commands that operate on sequences can be chained after `changes`.

__Example:__ Subscribe to the changes on a table.

Start monitoring the changefeed in one client:

```javascript
r.table('games').changes().run(conn, function(err, cursor) {
  cursor.each(console.log);
});
```

As these queries are performed in a second client, the first
client would receive and print the following objects:

```javascript
> r.table('games').insert({id: 1}).run(conn, callback);
{old_val: null, new_val: {id: 1}}

> r.table('games').get(1).update({player1: 'Bob'}).run(conn, callback);
{old_val: {id: 1}, new_val: {id: 1, player1: 'Bob'}}

> r.table('games').get(1).replace({id: 1, player1: 'Bob', player2: 'Alice'}).run(conn, callback);
{old_val: {id: 1, player1: 'Bob'},
 new_val: {id: 1, player1: 'Bob', player2: 'Alice'}}

> r.table('games').get(1).delete().run(conn, callback)
{old_val: {id: 1, player1: 'Bob', player2: 'Alice'}, new_val: null}

> r.tableDrop('games').run(conn, callback);
ReqlRuntimeError: Changefeed aborted (table unavailable)
```

[Read more about this command &rarr;](changes/)

## [noreplyWait](noreply_wait/) ##

{% apibody %}
conn.noreplyWait(callback)
conn.noreplyWait() &rarr; promise
{% endapibody %}

`noreplyWait` ensures that previous queries with the `noreply` flag have been processed by the server. Note that this guarantee only applies to queries run on the given connection.

If no callback is provided, a promise will be returned.

__Example:__ We have previously run queries with the `noreply` argument set to `true`. Now
wait until the server has processed them.

```javascript
conn.noreplyWait(function(err) { ... })
```

[Read more about this command &rarr;](noreply_wait/)

## [server](server/) ##

{% apibody %}
conn.server(callback)
conn.server() &rarr; promise
{% endapibody %}

Return information about the server being used by a connection.

__Example:__ Return server information.

```javascript
conn.server(callback);

// Result passed to callback
{
    "id": "404bef53-4b2c-433f-9184-bc3f7bda4a15",
    "name": "amadeus",
    "proxy": false
}
```

If no callback is provided, a promise will be returned.

[Read more about this command &rarr;](server/)

## [EventEmitter (connection)](event_emitter/) ##

{% apibody %}
connection.addListener(event, listener)
connection.on(event, listener)
connection.once(event, listener)
connection.removeListener(event, listener)
connection.removeAllListeners([event])
connection.setMaxListeners(n)
connection.listeners(event)
connection.emit(event, [arg1], [arg2], [...])
{% endapibody %}

Connections implement the same interface as Node's [EventEmitter][ee]. This allows you to listen for changes in connection state.

__Example:__ Monitor the connection state with events.

```javascript
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

[Read more about this command &rarr;](event_emitter/)

{% endapisection %}

{% apisection Cursors %}

## [next](next/) ##

{% apibody %}
cursor.next(callback)
array.next(callback)
cursor.next() &rarr; promise
array.next() &rarr; promise
{% endapibody %}

Get the next element in the cursor.

__Example:__ Retrieve the next element.

```javascript
cursor.next(function(err, row) {
    if (err) throw err;
    processRow(row);
});
```

[Read more about this command &rarr;](next/)

## [each](each/) ##

{% apibody %}
cursor.each(callback[, onFinishedCallback])
array.each(callback[, onFinishedCallback])
feed.each(callback)
{% endapibody %}

Lazily iterate over the result set one element at a time. The second callback is optional
and is called when the iteration stops (when there are no more rows or when the callback
returns `false`).

__Example:__ Let's process all the elements!

```javascript
cursor.each(function(err, row) {
    if (err) throw err;
    processRow(row);
});
```

[Read more about this command &rarr;](each/)

## [eachAsync](each_async/) ##

{% apibody %}
sequence.eachAsync(function[, errorFunction]) &rarr; promise
{% endapibody %}

Lazily iterate over a cursor, array, or feed one element at a time. `eachAsync` always returns a promise that will be resolved once all rows are returned.

__Example:__ Process all the elements in a stream, using `then` and `catch` for handling the end of the stream and any errors. Note that iteration may be stopped in the first callback (`rowProcess`) by returning any non-Promise value.

```javascript
cursor.eachAsync(function (row) {
    var ok = processRowData(row);
    if (!ok) {
        throw new Error('Bad row: ' + row);
    }
}).then(function () {
    console.log('done processing');
}).catch(function (error) {
    console.log('Error:', error.message);
});
```

[Read more about this command &rarr;](each_async/)

## [toArray](to_array/) ##

{% apibody %}
cursor.toArray(callback)
array.toArray(callback)
cursor.toArray() &rarr; promise
array.toArray() &rarr; promise
{% endapibody %}

Retrieve all results and pass them as an array to the given callback.

__Example:__ For small result sets it may be more convenient to process them at once as
an array.

```javascript
cursor.toArray(function(err, results) {
    if (err) throw err;
    processResults(results);
});
```

[Read more about this command &rarr;](to_array/)

## [close](close-cursor/) ##

{% apibody %}
cursor.close([callback])
cursor.close() &rarr; promise
{% endapibody %}

Close a cursor. Closing a cursor cancels the corresponding query and frees the memory associated with the open request.

__Example:__ Close a cursor.

```javascript
cursor.close(function (err) {
    if (err) {
        console.log("An error occurred on cursor close");
    }
});
```

[Read more about this command &rarr;](close-cursor/)

## [EventEmitter (cursor)](ee-cursor/) ##

{% apibody %}
cursor.addListener(event, listener)
cursor.on(event, listener)
cursor.once(event, listener)
cursor.removeListener(event, listener)
cursor.removeAllListeners([event])
cursor.setMaxListeners(n)
cursor.listeners(event)
cursor.emit(event, [arg1], [arg2], [...])
{% endapibody %}

Cursors and feeds implement the same interface as Node's [EventEmitter](http://nodejs.org/api/events.html#events_class_events_eventemitter).

__Example:__ Broadcast all messages with [socket.io](http://socket.io).

```javascript
r.table("messages").orderBy({index: "date"}).run(conn, function(err, cursor) {
    if (err) {
        // Handle error
        return
    }

    cursor.on("error", function(error) {
        // Handle error
    })
    cursor.on("data", function(message) {
        socket.broadcast.emit("message", message)
    })
});
```

[Read more about this command &rarr;](ee-cursor/)

{% endapisection %}

{% apisection Manipulating databases %}

## [dbCreate](db_create/) ##

{% apibody %}
r.dbCreate(dbName) &rarr; object
{% endapibody %}

Create a database. A RethinkDB database is a collection of tables, similar to
relational databases.

__Example:__ Create a database named 'superheroes'.

```javascript
> r.dbCreate('superheroes').run(conn, callback);
// Result passed to callback
{
    "config_changes": [
        {
            "new_val": {
                "id": "e4689cfc-e903-4532-a0e6-2d6797a43f07",
                "name": "superheroes"
            },
            "old_val": null
        }
    ],
    "dbs_created": 1
}
```

[Read more about this command &rarr;](db_create/)

## [dbDrop](db_drop/) ##

{% apibody %}
r.dbDrop(dbName) &rarr; object
{% endapibody %}

Drop a database. The database, all its tables, and corresponding data will be deleted.

__Example:__ Drop a database named 'superheroes'.

```javascript
> r.dbDrop('superheroes').run(conn, callback);
// Result passed to callback
{
    "config_changes": [
        {
            "old_val": {
                "id": "e4689cfc-e903-4532-a0e6-2d6797a43f07",
                "name": "superheroes"
            },
            "new_val": null
        }
    ],
    "tables_dropped": 3,
    "dbs_dropped": 1
}
```

[Read more about this command &rarr;](db_drop/)

## [dbList](db_list/) ##

{% apibody %}
r.dbList() &rarr; array
{% endapibody %}

List all database names in the system. The result is a list of strings.

__Example:__ List all databases.

```javascript
r.dbList().run(conn, callback)
```

[Read more about this command &rarr;](db_list/)

{% endapisection %}

{% apisection Manipulating tables %}

## [tableCreate](table_create/) ##

{% apibody %}
db.tableCreate(tableName[, options]) &rarr; object
r.tableCreate(tableName[, options]) &rarr; object
{% endapibody %}

Create a table. A RethinkDB table is a collection of JSON documents.

__Example:__ Create a table named 'dc_universe' with the default settings.

```javascript
> r.db('heroes').tableCreate('dc_universe').run(conn, callback);
// Result passed to callback
{
    "config_changes": [
        {
            "new_val": {
                "db": "test",
                "durability":  "hard",
                "id": "20ea60d4-3b76-4817-8828-98a236df0297",
                "name": "dc_universe",
                "primary_key": "id",
                "shards": [
                    {
                        "primary_replica": "rethinkdb_srv1",
                        "replicas": [
                            "rethinkdb_srv1",
                            "rethinkdb_srv2"
                        ]
                    }
                ],
                "write_acks": "majority"
            },
            "old_val": null
        }
    ],
    "tables_created": 1
}
```

[Read more about this command &rarr;](table_create/)

## [tableDrop](table_drop/) ##

{% apibody %}
db.tableDrop(tableName) &rarr; object
{% endapibody %}

Drop a table from a database. The table and all its data will be deleted.

__Example:__ Drop a table named 'dc_universe'.

```javascript
> r.db('test').tableDrop('dc_universe').run(conn, callback);
// Result passed to callback
{
    "config_changes": [
        {
            "old_val": {
                "db": "test",
                "durability":  "hard",
                "id": "20ea60d4-3b76-4817-8828-98a236df0297",
                "name": "dc_universe",
                "primary_key": "id",
                "shards": [
                    {
                        "primary_replica": "rethinkdb_srv1",
                        "replicas": [
                            "rethinkdb_srv1",
                            "rethinkdb_srv2"
                        ]
                    }
                ],
                "write_acks": "majority"
            },
            "new_val": null
        }
    ],
    "tables_dropped": 1
}
```

[Read more about this command &rarr;](table_drop/)

## [tableList](table_list/) ##

{% apibody %}
db.tableList() &rarr; array
{% endapibody %}

List all table names in a database. The result is a list of strings.

__Example:__ List all tables of the 'test' database.

```javascript
r.db('test').tableList().run(conn, callback)
```

[Read more about this command &rarr;](table_list/)

## [indexCreate](index_create/) ##

{% apibody %}
table.indexCreate(indexName[, indexFunction][, {multi: false, geo: false}]) &rarr; object
{% endapibody %}

Create a new secondary index on a table. Secondary indexes improve the speed of many read queries at the slight cost of increased storage space and decreased write performance. For more information about secondary indexes, read the article "[Using secondary indexes in RethinkDB](/docs/secondary-indexes/)."

__Example:__ Create a simple index based on the field `postId`.

```javascript
r.table('comments').indexCreate('postId').run(conn, callback)
```

[Read more about this command &rarr;](index_create/)

## [indexDrop](index_drop/) ##

{% apibody %}
table.indexDrop(indexName) &rarr; object
{% endapibody %}

Delete a previously created secondary index of this table.

__Example:__ Drop a secondary index named 'code_name'.

```javascript
r.table('dc').indexDrop('code_name').run(conn, callback)
```

[Read more about this command &rarr;](index_drop/)

## [indexList](index_list/) ##

{% apibody %}
table.indexList() &rarr; array
{% endapibody %}

List all the secondary indexes of this table.

__Example:__ List the available secondary indexes for this table.

```javascript
r.table('marvel').indexList().run(conn, callback)
```

[Read more about this command &rarr;](index_list/)

## [indexRename](index_rename/) ##

{% apibody %}
table.indexRename(oldIndexName, newIndexName[, {overwrite: false}]) &rarr; object
{% endapibody %}

Rename an existing secondary index on a table. If the optional argument `overwrite` is specified as `true`, a previously existing index with the new name will be deleted and the index will be renamed. If `overwrite` is `false` (the default) an error will be raised if the new index name already exists.

__Example:__ Rename an index on the comments table.

```javascript
r.table('comments').indexRename('postId', 'messageId').run(conn, callback)
```

[Read more about this command &rarr;](index_rename/)

## [indexStatus](index_status/) ##

{% apibody %}
table.indexStatus([, index...]) &rarr; array
{% endapibody %}

Get the status of the specified indexes on this table, or the status
of all indexes on this table if no indexes are specified.

__Example:__ Get the status of all the indexes on `test`:

```javascript
r.table('test').indexStatus().run(conn, callback)
```

[Read more about this command &rarr;](index_status/)

## [indexWait](index_wait/) ##

{% apibody %}
table.indexWait([, index...]) &rarr; array
{% endapibody %}

Wait for the specified indexes on this table to be ready, or for all
indexes on this table to be ready if no indexes are specified.

__Example:__ Wait for all indexes on the table `test` to be ready:

```javascript
r.table('test').indexWait().run(conn, callback)
```

[Read more about this command &rarr;](index_wait/)

{% endapisection %}

{% apisection Writing data %}

## [insert](insert/) ##

{% apibody %}
table.insert(object | [object1, object2, ...][, {durability: "hard", returnChanges: false, conflict: "error"}]) &rarr; object
{% endapibody %}

Insert documents into a table. Accepts a single document or an array of
documents.

__Example:__ Insert a document into the table `posts`.

```javascript
r.table("posts").insert({
    id: 1,
    title: "Lorem ipsum",
    content: "Dolor sit amet"
}).run(conn, callback)
```

[Read more about this command &rarr;](insert/)

## [update](update/) ##

{% apibody %}
table.update(object | function[, {durability: "hard", returnChanges: false, nonAtomic: false}])
    &rarr; object
selection.update(object | function[, {durability: "hard", returnChanges: false, nonAtomic: false}])
    &rarr; object
singleSelection.update(object | function[, {durability: "hard", returnChanges: false, nonAtomic: false}])
    &rarr; object
{% endapibody %}

Update JSON documents in a table. Accepts a JSON document, a ReQL expression, or a combination of the two.

__Example:__ Update the status of the post with `id` of `1` to `published`.

```javascript
r.table("posts").get(1).update({status: "published"}).run(conn, callback)
```

[Read more about this command &rarr;](update/)

## [replace](replace/) ##

{% apibody %}
table.replace(object | function[, {durability: "hard", returnChanges: false, nonAtomic: false}])
    &rarr; object
selection.replace(object | function[, {durability: "hard", returnChanges: false, nonAtomic: false}])
    &rarr; object
singleSelection.replace(object | function[, {durability: "hard", returnChanges: false, nonAtomic: false}])
    &rarr; object
{% endapibody %}

Replace documents in a table. Accepts a JSON document or a ReQL expression,
and replaces the original document with the new one. The new document must
have the same primary key as the original document.

__Example:__ Replace the document with the primary key `1`.

```javascript
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
table.delete([{durability: "hard", returnChanges: false}])
    &rarr; object
selection.delete([{durability: "hard", returnChanges: false}])
    &rarr; object
singleSelection.delete([{durability: "hard", returnChanges: false}])
    &rarr; object
{% endapibody %}

Delete one or more documents from a table.

__Example:__ Delete a single document from the table `comments`.

```javascript
r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete().run(conn, callback)
```

[Read more about this command &rarr;](delete/)

## [sync](sync/) ##

{% apibody %}
table.sync() &rarr; object
{% endapibody %}

`sync` ensures that writes on a given table are written to permanent storage. Queries
that specify soft durability (`{durability: 'soft'}`) do not give such guarantees, so
`sync` can be used to ensure the state of these queries. A call to `sync` does not return
until all previous writes to the table are persisted.

__Example:__ After having updated multiple heroes with soft durability, we now want to wait
until these changes are persisted.

```javascript
r.table('marvel').sync().run(conn, callback)
```

[Read more about this command &rarr;](sync/)

{% endapisection %}

{% apisection Selecting data %}

## [db](db/) ##

{% apibody %}
r.db(dbName) &rarr; db
{% endapibody %}

Reference a database.

__Example:__ Explicitly specify a database for a query.

```javascript
r.db('heroes').table('marvel').run(conn, callback)
```

[Read more about this command &rarr;](db/)

## [table](table/) ##

{% apibody %}
db.table(name[, {readMode: 'single', identifierFormat: 'name'}]) &rarr; table
{% endapibody %}

Return all documents in a table. Other commands may be chained after `table` to return a subset of documents (such as [get](/api/javascript/get/) and [filter](/api/javascript/filter/)) or perform further processing.

__Example:__ Return all documents in the table 'marvel' of the default database.

```javascript
r.table('marvel').run(conn, callback)
```

[Read more about this command &rarr;](table/)

## [get](get/) ##

{% apibody %}
table.get(key) &rarr; singleRowSelection
{% endapibody %}

Get a document by primary key.

__Example:__ Find a document by UUID.

```javascript
r.table('posts').get('a9849eef-7176-4411-935b-79a6e3c56a74').run(conn, callback);
```

[Read more about this command &rarr;](get/)

## [getAll](get_all/) ##

{% apibody %}
table.getAll([key, key2...], [, {index:'id'}]) &rarr; selection
{% endapibody %}

Get all documents where the given value matches the value of the requested index.

__Example:__ Secondary index keys are not guaranteed to be unique so we cannot query via [get](/api/javascript/get/) when using a secondary index.

```javascript
r.table('marvel').getAll('man_of_steel', {index:'code_name'}).run(conn, callback)
```

[Read more about this command &rarr;](get_all/)

## [between](between/) ##

{% apibody %}
table.between(lowerKey, upperKey[, options]) &rarr; table_slice
table_slice.between(lowerKey, upperKey[, options]) &rarr; table_slice
{% endapibody %}

Get all documents between two keys. Accepts three optional arguments: `index`, `leftBound`, and `rightBound`. If `index` is set to the name of a secondary index, `between` will return all documents where that index's value is in the specified range (it uses the primary key by default). `leftBound` or `rightBound` may be set to `open` or `closed` to indicate whether or not to include that endpoint of the range (by default, `leftBound` is closed and `rightBound` is open).

__Example:__ Find all users with primary key >= 10 and < 20 (a normal half-open interval).

```javascript
r.table('marvel').between(10, 20).run(conn, callback);
```

[Read more about this command &rarr;](between/)

## [filter](filter/) ##

{% apibody %}
selection.filter(predicate_function[, {default: false}]) &rarr; selection
stream.filter(predicate_function[, {default: false}]) &rarr; stream
array.filter(predicate_function[, {default: false}]) &rarr; array
{% endapibody %}

Return all the elements in a sequence for which the given predicate is true. The return value of `filter` will be the same as the input (sequence, stream, or array). Documents can be filtered in a variety of ways&mdash;ranges, nested values, boolean conditions, and the results of anonymous functions.

__Example:__ Get all users who are 30 years old.

```javascript
r.table('users').filter({age: 30}).run(conn, callback);
```

The predicate `{age: 30}` selects documents in the `users` table with an `age` field whose value is `30`. Documents with an `age` field set to any other value *or* with no `age` field present are skipped.

[Read more about this command &rarr;](filter/)

{% endapisection %}

{% apisection Joins %}

## [innerJoin](inner_join/) ##

{% apibody %}
sequence.innerJoin(otherSequence, predicate_function) &rarr; stream
array.innerJoin(otherSequence, predicate_function) &rarr; array
{% endapibody %}

Returns an inner join of two sequences.

__Example:__ Return a list of all matchups between Marvel and DC heroes in which the DC hero could beat the Marvel hero in a fight.

```javascript
r.table('marvel').innerJoin(r.table('dc'), function(marvelRow, dcRow) {
    return marvelRow('strength').lt(dcRow('strength'))
}).zip().run(conn, callback)
```

[Read more about this command &rarr;](inner_join/)

## [outerJoin](outer_join/) ##

{% apibody %}
sequence.outerJoin(otherSequence, predicate_function) &rarr; stream
array.outerJoin(otherSequence, predicate_function) &rarr; array
{% endapibody %}

Returns a left outer join of two sequences. The returned sequence represents a union of the left-hand sequence and the right-hand sequence: all documents in the left-hand sequence will be returned, each matched with a document in the right-hand sequence if one satisfies the predicate condition. In most cases, you will want to follow the join with [zip](/api/javascript/zip) to combine the left and right results.

__Example:__ Return a list of all Marvel heroes, paired with any DC heroes who could beat them in a fight.

```javascript
r.table('marvel').outerJoin(r.table('dc'), function(marvelRow, dcRow) {
    return marvelRow('strength').lt(dcRow('strength'))
}).run(conn, callback)
```

(Compare this to an [innerJoin](/api/javascript/inner_join) with the same inputs and predicate, which would return a list only of the matchups in which the DC hero has the higher strength.)

[Read more about this command &rarr;](outer_join/)

## [eqJoin](eq_join/) ##

{% apibody %}
sequence.eqJoin(leftField, rightTable[, {index: 'id', ordered: false}]) &rarr; sequence
sequence.eqJoin(function, rightTable[, {index: 'id', ordered: false}]) &rarr; sequence
{% endapibody %}

Join tables using a field or function on the left-hand sequence matching primary keys or secondary indexes on the right-hand table. `eqJoin` is more efficient than other ReQL join types, and operates much faster. Documents in the result set consist of pairs of left-hand and right-hand documents, matched when the field on the left-hand side exists and is non-null and an entry with that field's value exists in the specified index on the right-hand side.

__Example:__ Match players with the games they've played against one another.

Join these tables using `gameId` on the player table and `id` on the games table:

```javascript
r.table('players').eqJoin('gameId', r.table('games')).run(conn, callback)
```

This will return a result set such as the following:

```javascript
[
    {
        "left" : { "gameId" : 3, "id" : 2, "player" : "Agatha" },
        "right" : { "id" : 3, "field" : "Bucklebury" }
    },
    {
        "left" : { "gameId" : 2, "id" : 3, "player" : "Fred" },
        "right" : { "id" : 2, "field" : "Rushock Bog" }
    },
    ...
]
```

[Read more about this command &rarr;](eq_join/)

## [zip](zip/) ##

{% apibody %}
stream.zip() &rarr; stream
array.zip() &rarr; array
{% endapibody %}

Used to 'zip' up the result of a join by merging the 'right' fields into 'left' fields of each member of the sequence.

__Example:__ 'zips up' the sequence by merging the left and right fields produced by a join.

```javascript
r.table('marvel').eqJoin('main_dc_collaborator', r.table('dc'))
    .zip().run(conn, callback)
```

[Read more about this command &rarr;](zip/)

{% endapisection %}

{% apisection Transformations %}

## [map](map/) ##

{% apibody %}
sequence1.map([sequence2, ...], function) &rarr; stream
array1.map([array2, ...], function) &rarr; array
r.map(sequence1[, sequence2, ...], function) &rarr; stream
r.map(array1[, array2, ...], function) &rarr; array
{% endapibody %}

Transform each element of one or more sequences by applying a mapping function to them. If `map` is run with two or more sequences, it will iterate for as many items as there are in the shortest sequence.

__Example:__ Return the first five squares.

```javascript
r.expr([1, 2, 3, 4, 5]).map(function (val) {
    return val.mul(val);
}).run(conn, callback);
// Result passed to callback
[1, 4, 9, 16, 25]
```

[Read more about this command &rarr;](map/)

## [withFields](with_fields/) ##

{% apibody %}
sequence.withFields([selector1, selector2...]) &rarr; stream
array.withFields([selector1, selector2...]) &rarr; array
{% endapibody %}

Plucks one or more attributes from a sequence of objects, filtering out any objects in the sequence that do not have the specified fields. Functionally, this is identical to [hasFields](/api/javascript/has_fields/) followed by [pluck](/api/javascript/pluck/) on a sequence.

__Example:__ Get a list of users and their posts, excluding any users who have not made any posts.

Existing table structure:

```javascript
[
    { 'id': 1, 'user': 'bob', 'email': 'bob@foo.com', 'posts': [ 1, 4, 5 ] },
    { 'id': 2, 'user': 'george', 'email': 'george@foo.com' },
    { 'id': 3, 'user': 'jane', 'email': 'jane@foo.com', 'posts': [ 2, 3, 6 ] }
]
```

Command and output:

```javascript
> r.table('users').withFields('id', 'user', 'posts').run(conn, callback)
// Result passed to callback
[
    { 'id': 1, 'user': 'bob', 'posts': [ 1, 4, 5 ] },
    { 'id': 3, 'user': 'jane', 'posts': [ 2, 3, 6 ] }
]
```

[Read more about this command &rarr;](with_fields/)

## [concatMap](concat_map/) ##

{% apibody %}
stream.concatMap(function) &rarr; stream
array.concatMap(function) &rarr; array
{% endapibody %}

Concatenate one or more elements into a single sequence using a mapping function.

__Example:__ Construct a sequence of all monsters defeated by Marvel heroes. The field "defeatedMonsters" is an array of one or more monster names.

```javascript
r.table('marvel').concatMap(function(hero) {
    return hero('defeatedMonsters')
}).run(conn, callback)
```

[Read more about this command &rarr;](concat_map/)

## [orderBy](order_by/) ##

{% apibody %}
table.orderBy([key | function...], {index: index_name}) &rarr; table_slice
selection.orderBy(key | function[, ...]) &rarr; selection<array>
sequence.orderBy(key | function[, ...]) &rarr; array
{% endapibody %}

Sort the sequence by document values of the given key(s). To specify
the ordering, wrap the attribute with either `r.asc` or `r.desc`
(defaults to ascending).

__Example:__ Order all the posts using the index `date`.

```javascript
r.table('posts').orderBy({index: 'date'}).run(conn, callback);
```

[Read more about this command &rarr;](order_by/)

## [skip](skip/) ##

{% apibody %}
sequence.skip(n) &rarr; stream
array.skip(n) &rarr; array
{% endapibody %}

Skip a number of elements from the head of the sequence.

__Example:__ Here in conjunction with [orderBy](/api/javascript/order_by/) we choose to ignore the most successful heroes.

```javascript
r.table('marvel').orderBy('successMetric').skip(10).run(conn, callback)
```

[Read more about this command &rarr;](skip/)

## [limit](limit/) ##

{% apibody %}
sequence.limit(n) &rarr; stream
array.limit(n) &rarr; array
{% endapibody %}

End the sequence after the given number of elements.

__Example:__ Only so many can fit in our Pantheon of heroes.

```javascript
r.table('marvel').orderBy('belovedness').limit(10).run(conn, callback)
```

[Read more about this command &rarr;](limit/)

## [slice](slice/) ##

{% apibody %}
selection.slice(startOffset[, endOffset, {leftBound:'closed', rightBound:'open'}]) &rarr; selection
stream.slice(startOffset[, endOffset, {leftBound:'closed', rightBound:'open'}]) &rarr; stream
array.slice(startOffset[, endOffset, {leftBound:'closed', rightBound:'open'}]) &rarr; array
binary.slice(startOffset[, endOffset, {leftBound:'closed', rightBound:'open'}]) &rarr; binary
string.slice(startOffset[, endOffset, {leftBound:'closed', rightBound:'open'}]) &rarr; string
{% endapibody %}

Return the elements of a sequence within the specified range.

__Example:__ Return the fourth, fifth and sixth youngest players. (The youngest player is at index 0, so those are elements 3&ndash;5.)

```javascript
r.table('players').orderBy({index: 'age'}).slice(3,6).run(conn, callback);
```

[Read more about this command &rarr;](slice/)

## [nth](nth/) ##

{% apibody %}
sequence.nth(index) &rarr; object
selection.nth(index) &rarr; selection&lt;object&gt;
{% endapibody %}

Get the *nth* element of a sequence, counting from zero. If the argument is negative, count from the last element.

__Example:__ Select the second element in the array.

```javascript
r.expr([1,2,3]).nth(1).run(conn, callback)
r.expr([1,2,3])(1).run(conn, callback)
```

[Read more about this command &rarr;](nth/)

## [offsetsOf](offsets_of/) ##

{% apibody %}
sequence.offsetsOf(datum | predicate_function) &rarr; array
{% endapibody %}

Get the indexes of an element in a sequence. If the argument is a predicate, get the indexes of all elements matching it.

__Example:__ Find the position of the letter 'c'.

```javascript
r.expr(['a','b','c']).offsetsOf('c').run(conn, callback)
```

[Read more about this command &rarr;](offsets_of/)

## [isEmpty](is_empty/) ##

{% apibody %}
sequence.isEmpty() &rarr; bool
{% endapibody %}

Test if a sequence is empty.

__Example:__ Are there any documents in the marvel table?

```javascript
r.table('marvel').isEmpty().run(conn, callback)
```

[Read more about this command &rarr;](is_empty/)

## [union](union/) ##

{% apibody %}
stream.union(sequence[, sequence, ...][, {interleave: true}]) &rarr; stream
array.union(sequence[, sequence, ...][, {interleave: true}]) &rarr; array
r.union(stream, sequence[, sequence, ...][, {interleave: true}]) &rarr; stream
r.union(array, sequence[, sequence, ...][, {interleave: true}]) &rarr; array
{% endapibody %}

Merge two or more sequences.

__Example:__ Construct a stream of all heroes.

```javascript
r.table('marvel').union(r.table('dc')).run(conn, callback);
```

[Read more about this command &rarr;](union/)

## [sample](sample/) ##

{% apibody %}
sequence.sample(number) &rarr; selection
stream.sample(number) &rarr; array
array.sample(number) &rarr; array
{% endapibody %}

Select a given number of elements from a sequence with uniform random distribution. Selection is done without replacement.

__Example:__ Select 3 random heroes.

```javascript
r.table('marvel').sample(3).run(conn, callback)
```

[Read more about this command &rarr;](sample/)

{% endapisection %}

{% apisection Aggregation %}

## [group](group/) ##

{% apibody %}
sequence.group(field | function..., [{index: <indexname>, multi: false}]) &rarr; grouped_stream
r.group(sequence, field | function..., [{index: <indexname>, multi: false}]) &rarr; grouped_stream
{% endapibody %}

Takes a stream and partitions it into multiple groups based on the
fields or functions provided.

__Example:__ Group games by player.

```javascript
> r.table('games').group('player').run(conn, callback)

// Result passed to callback
[
    {
        group: "Alice",
        reduction: [
            {id: 5, player: "Alice", points: 7, type: "free"},
            {id: 12, player: "Alice", points: 2, type: "free"}
        ]
    },
    {
        group: "Bob",
        reduction: [
            {id: 2, player: "Bob", points: 15, type: "ranked"},
            {id: 11, player: "Bob", points: 10, type: "free"}
        ]
    }
]
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

```javascript
r.table('games')
   .group('player').max('points')('points')
   .ungroup().orderBy(r.desc('reduction')).run(conn, callback)
```

[Read more about this command &rarr;](ungroup/)

## [reduce](reduce/) ##

{% apibody %}
sequence.reduce(function) &rarr; value
r.reduce(sequence, function) &rarr; value
{% endapibody %}

Produce a single value from a sequence through repeated application of a reduction function.

__Example:__ Return the number of documents in the table `posts`.

```javascript
r.table("posts").map(function(doc) {
    return 1;
}).reduce(function(left, right) {
    return left.add(right);
}).default(0).run(conn, callback);
```

A shorter way to execute this query is to use [count](/api/javascript/count).

[Read more about this command &rarr;](reduce/)

## [fold](fold/) ##

{% apibody %}
sequence.fold(base, function) &rarr; value
sequence.fold(base, function, {emit: function[, finalEmit: function]}) &rarr; sequence
{% endapibody %}

Apply a function to a sequence in order, maintaining state via an accumulator. The `fold` command returns either a single value or a new sequence.

__Example:__ Concatenate words from a list.

```javascript
r.table('words').orderBy('id').fold('', function (acc, word) {
    return acc.add(r.branch(acc.eq(''), '', ', ')).add(word);
}).run(conn, callback);
```

(This example could be implemented with `reduce`, but `fold` will preserve the order when `words` is a RethinkDB table or other stream, which is not guaranteed with `reduce`.)

[Read more about this command &rarr;](fold/)

## [count](count/) ##

{% apibody %}
sequence.count([value | predicate_function]) &rarr; number
binary.count() &rarr; number
string.count() &rarr; number
object.count() &rarr; number
r.count(sequence | binary | string | object[, predicate_function]) &rarr; number
{% endapibody %}

Counts the number of elements in a sequence or key/value pairs in an object, or returns the size of a string or binary object.

__Example:__ Count the number of users.

```javascript
r.table('users').count().run(conn, callback);
```

[Read more about this command &rarr;](count/)

## [sum](sum/) ##

{% apibody %}
sequence.sum([field | function]) &rarr; number
r.sum(sequence, [field | function]) &rarr; number
{% endapibody %}

Sums all the elements of a sequence.  If called with a field name,
sums all the values of that field in the sequence, skipping elements
of the sequence that lack that field.  If called with a function,
calls that function on every element of the sequence and sums the
results, skipping elements of the sequence where that function returns
`null` or a non-existence error.

__Example:__ What's 3 + 5 + 7?

```javascript
r.expr([3, 5, 7]).sum().run(conn, callback)
```

[Read more about this command &rarr;](sum/)

## [avg](avg/) ##

{% apibody %}
sequence.avg([field | function]) &rarr; number
r.avg(sequence, [field | function]) &rarr; number
{% endapibody %}

Averages all the elements of a sequence.  If called with a field name,
averages all the values of that field in the sequence, skipping
elements of the sequence that lack that field.  If called with a
function, calls that function on every element of the sequence and
averages the results, skipping elements of the sequence where that
function returns `null` or a non-existence error.

__Example:__ What's the average of 3, 5, and 7?

```javascript
r.expr([3, 5, 7]).avg().run(conn, callback)
```

[Read more about this command &rarr;](avg/)

## [min](min/) ##

{% apibody %}
sequence.min(field | function) &rarr; element
sequence.min({index: <indexname>}) &rarr; element
r.min(sequence, field | function) &rarr; element
r.min(sequence, {index: <indexname>}) &rarr; element
{% endapibody %}

Finds the minimum element of a sequence.

__Example:__ Return the minimum value in the list `[3, 5, 7]`.

```javascript
r.expr([3, 5, 7]).min().run(conn, callback);
```

[Read more about this command &rarr;](min/)

## [max](max/) ##

{% apibody %}
sequence.max(field | function) &rarr; element
sequence.max({index: <indexname>}) &rarr; element
r.max(sequence, field | function) &rarr; element
r.max(sequence, {index: <indexname>}) &rarr; element
{% endapibody %}

Finds the maximum element of a sequence.

__Example:__ Return the maximum value in the list `[3, 5, 7]`.

```javascript
r.expr([3, 5, 7]).max().run(conn, callback);
```

[Read more about this command &rarr;](max/)

## [distinct](distinct/) ##

{% apibody %}
sequence.distinct() &rarr; array
table.distinct([{index: <indexname>}]) &rarr; stream
r.distinct(sequence) &rarr; array
r.distinct(table, [{index: <indexname>}]) &rarr; stream
{% endapibody %}

Removes duplicates from elements in a sequence.

__Example:__ Which unique villains have been vanquished by Marvel heroes?

```javascript
r.table('marvel').concatMap(function(hero) {
    return hero('villainList')
}).distinct().run(conn, callback)
```

[Read more about this command &rarr;](distinct/)

## [contains](contains/) ##

{% apibody %}
sequence.contains([value | predicate_function, ...]) &rarr; bool
r.contains(sequence, [value | predicate_function, ...]) &rarr; bool
{% endapibody %}

When called with values, returns `true` if a sequence contains all the
specified values.  When called with predicate functions, returns `true`
if for each predicate there exists at least one element of the stream
where that predicate returns `true`.

__Example:__ Has Iron Man ever fought Superman?

```javascript
r.table('marvel').get('ironman')('opponents').contains('superman').run(conn, callback);
```

[Read more about this command &rarr;](contains/)

{% endapisection %}

{% apisection Document manipulation %}

## [row](row/) ##

{% apibody %}
r.row &rarr; value
{% endapibody %}

Returns the currently visited document.

__Example:__ Get all users whose age is greater than 5.

```javascript
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

```javascript
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

```javascript
r.table('marvel').get('IronMan').without('personalVictoriesList').run(conn, callback)
```

[Read more about this command &rarr;](without/)

## [merge](merge/) ##

{% apibody %}
singleSelection.merge([object | function, object | function, ...]) &rarr; object
object.merge([object | function, object | function, ...]) &rarr; object
sequence.merge([object | function, object | function, ...]) &rarr; stream
array.merge([object | function, object | function, ...]) &rarr; array
{% endapibody %}

Merge two or more objects together to construct a new object with properties from all. When there is a conflict between field names, preference is given to fields in the rightmost object in the argument list. `merge` also accepts a subquery function that returns an object, which will be used similarly to a [map](/api/javascript/map/) function.

__Example:__ Equip Thor for battle.

```javascript
r.table('marvel').get('thor').merge(
    r.table('equipment').get('hammer'),
    r.table('equipment').get('pimento_sandwich')
).run(conn, callback)
```

[Read more about this command &rarr;](merge/)

## [append](append/) ##

{% apibody %}
array.append(value) &rarr; array
{% endapibody %}

Append a value to an array.

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```javascript
r.table('marvel').get('IronMan')('equipment').append('newBoots').run(conn, callback)
```

[Read more about this command &rarr;](append/)

## [prepend](prepend/) ##

{% apibody %}
array.prepend(value) &rarr; array
{% endapibody %}

Prepend a value to an array.

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```javascript
r.table('marvel').get('IronMan')('equipment').prepend('newBoots').run(conn, callback)
```

[Read more about this command &rarr;](prepend/)

## [difference](difference/) ##

{% apibody %}
array.difference(array) &rarr; array
{% endapibody %}

Remove the elements of one array from another array.

__Example:__ Retrieve Iron Man's equipment list without boots.

```javascript
r.table('marvel').get('IronMan')('equipment')
  .difference(['Boots'])
  .run(conn, callback)
```

[Read more about this command &rarr;](difference/)

## [setInsert](set_insert/) ##

{% apibody %}
array.setInsert(value) &rarr; array
{% endapibody %}

Add a value to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```javascript
r.table('marvel').get('IronMan')('equipment').setInsert('newBoots').run(conn, callback)
```

[Read more about this command &rarr;](set_insert/)

## [setUnion](set_union/) ##

{% apibody %}
array.setUnion(array) &rarr; array
{% endapibody %}

Add a several values to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots and an arc reactor.

```javascript
r.table('marvel').get('IronMan')('equipment').setUnion(['newBoots', 'arc_reactor']).run(conn, callback)
```

[Read more about this command &rarr;](set_union/)

## [setIntersection](set_intersection/) ##

{% apibody %}
array.setIntersection(array) &rarr; array
{% endapibody %}

Intersect two arrays returning values that occur in both of them as a set (an array with
distinct values).

__Example:__ Check which pieces of equipment Iron Man has from a fixed list.

```javascript
r.table('marvel').get('IronMan')('equipment').setIntersection(['newBoots', 'arc_reactor']).run(conn, callback)
```

[Read more about this command &rarr;](set_intersection/)

## [setDifference](set_difference/) ##

{% apibody %}
array.setDifference(array) &rarr; array
{% endapibody %}

Remove the elements of one array from another and return them as a set (an array with
distinct values).

__Example:__ Check which pieces of equipment Iron Man has, excluding a fixed list.

```javascript
r.table('marvel').get('IronMan')('equipment').setDifference(['newBoots', 'arc_reactor']).run(conn, callback)
```

[Read more about this command &rarr;](set_difference/)

## [() (bracket)](bracket/) ##

{% apibody %}
sequence(attr) &rarr; sequence
singleSelection(attr) &rarr; value
object(attr) &rarr; value
array(index) &rarr; value
{% endapibody %}

Get a single field from an object. If called on a sequence, gets that field from every object in the sequence, skipping objects that lack it.

__Example:__ What was Iron Man's first appearance in a comic?

```javascript
r.table('marvel').get('IronMan')('firstAppearance').run(conn, callback)
```

[Read more about this command &rarr;](bracket/)

## [getField](get_field/) ##

{% apibody %}
sequence.getField(attr) &rarr; sequence
singleSelection.getField(attr) &rarr; value
object.getField(attr) &rarr; value
{% endapibody %}

Get a single field from an object. If called on a sequence, gets that field from every
object in the sequence, skipping objects that lack it.

__Example:__ What was Iron Man's first appearance in a comic?

```javascript
r.table('marvel').get('IronMan').getField('firstAppearance').run(conn, callback)
```

[Read more about this command &rarr;](get_field/)

## [hasFields](has_fields/) ##

{% apibody %}
sequence.hasFields([selector1, selector2...]) &rarr; stream
array.hasFields([selector1, selector2...]) &rarr; array
object.hasFields([selector1, selector2...]) &rarr; boolean
{% endapibody %}

Test if an object has one or more fields. An object has a field if it has that key and the key has a non-null value. For instance, the object `{'a': 1,'b': 2,'c': null}` has the fields `a` and `b`.

__Example:__ Return the players who have won games.

```javascript
r.table('players').hasFields('games_won').run(conn, callback)
```

[Read more about this command &rarr;](has_fields/)

## [insertAt](insert_at/) ##

{% apibody %}
array.insertAt(offset, value) &rarr; array
{% endapibody %}

Insert a value in to an array at a given index. Returns the modified array.

__Example:__ Hulk decides to join the avengers.

```javascript
r.expr(["Iron Man", "Spider-Man"]).insertAt(1, "Hulk").run(conn, callback)
```

[Read more about this command &rarr;](insert_at/)

## [spliceAt](splice_at/) ##

{% apibody %}
array.spliceAt(offset, array) &rarr; array
{% endapibody %}

Insert several values in to an array at a given index. Returns the modified array.

__Example:__ Hulk and Thor decide to join the avengers.

```javascript
r.expr(["Iron Man", "Spider-Man"]).spliceAt(1, ["Hulk", "Thor"]).run(conn, callback)
```

[Read more about this command &rarr;](splice_at/)

## [deleteAt](delete_at/) ##

{% apibody %}
array.deleteAt(offset [,endOffset]) &rarr; array
{% endapibody %}

Remove one or more elements from an array at a given index. Returns the modified array. (Note: `deleteAt` operates on arrays, not documents; to delete documents, see the [delete](/api/javascript/delete) command.)

__Example:__ Delete the second element of an array.

```javascript
> r(['a','b','c','d','e','f']).deleteAt(1).run(conn, callback)
// result passed to callback
['a', 'c', 'd', 'e', 'f']
```

[Read more about this command &rarr;](delete_at/)

## [changeAt](change_at/) ##

{% apibody %}
array.changeAt(offset, value) &rarr; array
{% endapibody %}

Change a value in an array at a given index. Returns the modified array.

__Example:__ Bruce Banner hulks out.

```javascript
r.expr(["Iron Man", "Bruce", "Spider-Man"]).changeAt(1, "Hulk").run(conn, callback)
```

[Read more about this command &rarr;](change_at/)

## [keys](keys/) ##

{% apibody %}
singleSelection.keys() &rarr; array
object.keys() &rarr; array
{% endapibody %}

Return an array containing all of an object's keys. Note that the keys will be sorted as described in [ReQL data types](/docs/data-types/#sorting-order) (for strings, lexicographically).

__Example:__ Get all the keys from a table row.

```javascript
// row: { id: 1, mail: "fred@example.com", name: "fred" }

r.table('users').get(1).keys().run(conn, callback);
// Result passed to callback
[ "id", "mail", "name" ]
```

[Read more about this command &rarr;](keys/)

## [values](values/) ##

{% apibody %}
singleSelection.values() &rarr; array
object.values() &rarr; array
{% endapibody %}

Return an array containing all of an object's values. `values()` guarantees the values will come out in the same order as [keys](/api/javascript/keys).

__Example:__ Get all of the values from a table row.

```javascript
// row: { id: 1, mail: "fred@example.com", name: "fred" }

r.table('users').get(1).values().run(conn, callback);
// Result passed to callback
[ 1, "fred@example.com", "fred" ]
```

[Read more about this command &rarr;](values/)

## [literal](literal/) ##

{% apibody %}
r.literal(object) &rarr; special
{% endapibody %}

Replace an object in a field instead of merging it with an existing object in a `merge` or `update` operation. Using `literal` with no arguments in a `merge` or `update` operation will remove the corresponding field.

__Example:__ Replace one nested document with another rather than merging the fields.

```javascript
r.table('users').get(1).update({ data: r.literal({ age: 19, job: 'Engineer' }) }).run(conn, callback)

// Result passed to callback
{
    "id": 1,
    "name": "Alice",
    "data": {
        "age": 19,
        "job": "Engineer"
    }
}
```

[Read more about this command &rarr;](literal/)

## [object](object/) ##

{% apibody %}
r.object([key, value,]...) &rarr; object
{% endapibody %}

Creates an object from a list of key-value pairs, where the keys must
be strings.  `r.object(A, B, C, D)` is equivalent to
`r.expr([[A, B], [C, D]]).coerceTo('OBJECT')`.

__Example:__ Create a simple object.

```javascript
r.object('id', 5, 'data', ['foo', 'bar']).run(conn, callback)
```

Result:

```javascript
{data: ["foo", "bar"], id: 5}
```

[Read more about this command &rarr;](object/)

{% endapisection %}

{% apisection String manipulation %}

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

__Example:__ Get all users whose name starts with "A". Because `null` evaluates to `false` in
[filter](/api/javascript/filter/), you can just use the result of `match` for the predicate.

```javascript
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

__Example:__ Split on whitespace.

```javascript
r.expr("foo  bar bax").split().run(conn, callback)
```

Result:

```javascript
["foo", "bar", "bax"]
```

[Read more about this command &rarr;](split/)

## [upcase](upcase/) ##

{% apibody %}
string.upcase() &rarr; string
{% endapibody %}

Uppercases a string.

__Example:__

```javascript
r.expr("Sentence about LaTeX.").upcase().run(conn, callback)
```

Result:

```javascript
"SENTENCE ABOUT LATEX."
```

__Note:__ `upcase` and `downcase` only affect ASCII characters.

[Read more about this command &rarr;](upcase/)

## [downcase](downcase/) ##

{% apibody %}
string.downcase() &rarr; string
{% endapibody %}

Lowercases a string.

__Example:__

```javascript
r.expr("Sentence about LaTeX.").downcase().run(conn, callback)
```

Result:

```javascript
"sentence about latex."
```

__Note:__ `upcase` and `downcase` only affect ASCII characters.

[Read more about this command &rarr;](downcase/)

{% endapisection %}

{% apisection Math and logic %}

## [add](add/) ##

{% apibody %}
value.add(value[, value, ...]) &rarr; value
time.add(number[, number, ...]) &rarr; time
{% endapibody %}

Sum two or more numbers, or concatenate two or more strings or arrays.

__Example:__ It's as easy as 2 + 2 = 4.

```javascript
> r.expr(2).add(2).run(conn, callback)
// result passed to callback
4
```

[Read more about this command &rarr;](add/)

## [sub](sub/) ##

{% apibody %}
number.sub(number[, number, ...]) &rarr; number
time.sub(number[, number, ...]) &rarr; time
time.sub(time) &rarr; number
{% endapibody %}

Subtract two numbers.

__Example:__ It's as easy as 2 - 2 = 0.

```javascript
r.expr(2).sub(2).run(conn, callback)
```

[Read more about this command &rarr;](sub/)

## [mul](mul/) ##

{% apibody %}
number.mul(number[, number, ...]) &rarr; number
array.mul(number[, number, ...]) &rarr; array
{% endapibody %}

Multiply two numbers, or make a periodic array.

__Example:__ It's as easy as 2 * 2 = 4.

```javascript
r.expr(2).mul(2).run(conn, callback)
```

[Read more about this command &rarr;](mul/)

## [div](div/) ##

{% apibody %}
number.div(number[, number ...]) &rarr; number
{% endapibody %}

Divide two numbers.

__Example:__ It's as easy as 2 / 2 = 1.

```javascript
r.expr(2).div(2).run(conn, callback)
```

[Read more about this command &rarr;](div/)

## [mod](mod/) ##

{% apibody %}
number.mod(number) &rarr; number
{% endapibody %}



__Example:__ It's as easy as 2 % 2 = 0.

```javascript
r.expr(2).mod(2).run(conn, callback)
```

[Read more about this command &rarr;](mod/)

## [and](and/) ##

{% apibody %}
bool.and([bool, bool, ...]) &rarr; bool
r.and([bool, bool, ...]) &rarr; bool
{% endapibody %}

Compute the logical "and" of one or more values.

__Example:__ Return whether both `a` and `b` evaluate to true.

```javascript
var a = true, b = false;
r.expr(a).and(b).run(conn, callback);
// result passed to callback
false
```

[Read more about this command &rarr;](and/)

## [or](or/) ##

{% apibody %}
bool.or([bool, bool, ...]) &rarr; bool
r.or([bool, bool, ...]) &rarr; bool
{% endapibody %}

Compute the logical "or" of one or more values.

__Example:__ Return whether either `a` or `b` evaluate to true.

```javascript
var a = true, b = false;
r.expr(a).or(b).run(conn, callback);
// result passed to callback
true
```

[Read more about this command &rarr;](or/)

## [eq](eq/) ##

{% apibody %}
value.eq(value[, value, ...]) &rarr; bool
{% endapibody %}

Test if two or more values are equal.

__Example:__ See if a user's `role` field is set to `administrator`.

```javascript
r.table('users').get(1)('role').eq('administrator').run(conn, callback);
```

[Read more about this command &rarr;](eq/)

## [ne](ne/) ##

{% apibody %}
value.ne(value[, value, ...]) &rarr; bool
{% endapibody %}

Test if two or more values are not equal.

__Example:__ See if a user's `role` field is not set to `administrator`.

```javascript
r.table('users').get(1)('role').ne('administrator').run(conn, callback);
```

[Read more about this command &rarr;](ne/)

## [gt](gt/) ##

{% apibody %}
value.gt(value[, value, ...]) &rarr; bool
{% endapibody %}

Compare values, testing if the left-hand value is greater than the right-hand.

__Example:__ Test if a player has scored more than 10 points.

```javascript
r.table('players').get(1)('score').gt(10).run(conn, callback);
```

[Read more about this command &rarr;](gt/)

## [ge](ge/) ##

{% apibody %}
value.ge(value[, value, ...]) &rarr; bool
{% endapibody %}

Compare values, testing if the left-hand value is greater than or equal to the right-hand.

__Example:__ Test if a player has scored 10 points or more.

```javascript
r.table('players').get(1)('score').ge(10).run(conn, callback);
```

[Read more about this command &rarr;](ge/)

## [lt](lt/) ##

{% apibody %}
value.lt(value[, value, ...]) &rarr; bool
{% endapibody %}

Compare values, testing if the left-hand value is less than the right-hand.

__Example:__ Test if a player has scored less than 10 points.

```javascript
r.table('players').get(1)('score').lt(10).run(conn, callback);
```

[Read more about this command &rarr;](lt/)

## [le](le/) ##

{% apibody %}
value.le(value[, value, ...]) &rarr; bool
{% endapibody %}

Compare values, testing if the left-hand value is less than or equal to the right-hand.

__Example:__ Test if a player has scored 10 points or less.

```javascript
r.table('players').get(1)('score').le(10).run(conn, callback);
```

[Read more about this command &rarr;](le/)

## [not](not/) ##

{% apibody %}
bool.not() &rarr; bool
not(bool) &rarr; bool
{% endapibody %}

Compute the logical inverse (not) of an expression.

__Example:__ Not true is false.

```javascript
r(true).not().run(conn, callback)
r.not(true).run(conn, callback)
```

These evaluate to `false`.

[Read more about this command &rarr;](not/)

## [random](random/) ##

{% apibody %}
r.random() &rarr; number
r.random(number[, number], {float: true}) &rarr; number
r.random(integer[, integer]) &rarr; integer
{% endapibody %}

Generate a random number between given (or implied) bounds. `random` takes zero, one or two arguments.

__Example:__ Generate a random number in the range `[0,1)`

```javascript
r.random().run(conn, callback)
```

[Read more about this command &rarr;](random/)

## [round](round/) ##

{% apibody %}
r.round(number) &rarr; number
number.round() &rarr; number
{% endapibody %}

Rounds the given value to the nearest whole integer.

__Example:__ Round 12.345 to the nearest integer.

```javascript
r.round(12.345).run(conn, callback);
// Result passed to callback
12.0
```

The `round` command can also be chained after an expression.

[Read more about this command &rarr;](round/)

## [ceil](ceil/) ##

{% apibody %}
r.ceil(number) &rarr; number
number.ceil() &rarr; number
{% endapibody %}

Rounds the given value up, returning the smallest integer value greater than or equal to the given value (the value's ceiling).

__Example:__ Return the ceiling of 12.345.

```javascript
r.ceil(12.345).run(conn, callback);
// Result passed to callback
13.0
```

The `ceil` command can also be chained after an expression.

[Read more about this command &rarr;](ceil/)

## [floor](floor/) ##

{% apibody %}
r.floor(number) &rarr; number
number.floor() &rarr; number
{% endapibody %}

Rounds the given value down, returning the largest integer value less than or equal to the given value (the value's floor).

__Example:__ Return the floor of 12.345.

```javascript
r.floor(12.345).run(conn, callback);
// Result passed to callback
12.0
```

The `floor` command can also be chained after an expression.

[Read more about this command &rarr;](floor/)

{% endapisection %}

{% apisection Dates and times %}

## [now](now/) ##

{% apibody %}
r.now() &rarr; time
{% endapibody %}

Return a time object representing the current time in UTC. The command now() is computed once when the server receives the query, so multiple instances of r.now() will always return the same time inside a query.

__Example:__ Add a new user with the time at which he subscribed.

```javascript
r.table("users").insert({
    name: "John",
    subscription_date: r.now()
}).run(conn, callback)
```

[Read more about this command &rarr;](now/)

## [time](time/) ##

{% apibody %}
r.time(year, month, day[, hour, minute, second], timezone)
    &rarr; time
{% endapibody %}

Create a time object for a specific time.

__Example:__ Update the birthdate of the user "John" to November 3rd, 1986 UTC.

```javascript
r.table("user").get("John").update({birthdate: r.time(1986, 11, 3, 'Z')}).run(conn, callback)
```

[Read more about this command &rarr;](time/)

## [epochTime](epoch_time/) ##

{% apibody %}
r.epochTime(number) &rarr; time
{% endapibody %}

Create a time object based on seconds since epoch. The first argument is a double and
will be rounded to three decimal places (millisecond-precision).

__Example:__ Update the birthdate of the user "John" to November 3rd, 1986.

```javascript
r.table("user").get("John").update({birthdate: r.epochTime(531360000)}).run(conn, callback)
```

[Read more about this command &rarr;](epoch_time/)

## [ISO8601](iso8601/) ##

{% apibody %}
r.ISO8601(string[, {defaultTimezone:''}]) &rarr; time
{% endapibody %}

Create a time object based on an ISO 8601 date-time string (e.g. '2013-01-01T01:01:01+00:00'). RethinkDB supports all valid ISO 8601 formats except for week dates. Read more about the ISO 8601 format at [Wikipedia](http://en.wikipedia.org/wiki/ISO_8601).

__Example:__ Update the time of John's birth.

```javascript
r.table("user").get("John").update({birth: r.ISO8601('1986-11-03T08:30:00-07:00')}).run(conn, callback)
```

[Read more about this command &rarr;](iso8601/)

## [inTimezone](in_timezone/) ##

{% apibody %}
time.inTimezone(timezone) &rarr; time
{% endapibody %}

Return a new time object with a different timezone. While the time stays the same, the results returned by methods such as hours() will change since they take the timezone into account. The timezone argument has to be of the ISO 8601 format.

__Example:__ Hour of the day in San Francisco (UTC/GMT -8, without daylight saving time).

```javascript
r.now().inTimezone('-08:00').hours().run(conn, callback)
```

[Read more about this command &rarr;](in_timezone/)

## [timezone](timezone/) ##

{% apibody %}
time.timezone() &rarr; string
{% endapibody %}

Return the timezone of the time object.

__Example:__ Return all the users in the "-07:00" timezone.

```javascript
r.table("users").filter( function(user) {
    return user("subscriptionDate").timezone().eq("-07:00")
})
```

[Read more about this command &rarr;](timezone/)

## [during](during/) ##

{% apibody %}
time.during(startTime, endTime[, {leftBound: "closed", rightBound: "open"}]) &rarr; bool
{% endapibody %}

Return whether a time is between two other times.

__Example:__ Retrieve all the posts that were posted between December 1st, 2013
(inclusive) and December 10th, 2013 (exclusive).

```javascript
r.table("posts").filter(
    r.row('date').during(r.time(2013, 12, 1, "Z"), r.time(2013, 12, 10, "Z"))
).run(conn, callback)
```

[Read more about this command &rarr;](during/)

## [date](date/) ##

{% apibody %}
time.date() &rarr; time
{% endapibody %}

Return a new time object only based on the day, month and year (ie. the same day at 00:00).

__Example:__ Retrieve all the users whose birthday is today.

```javascript
r.table("users").filter(function(user) {
    return user("birthdate").date().eq(r.now().date())
}).run(conn, callback)
```

[Read more about this command &rarr;](date/)

## [timeOfDay](time_of_day/) ##

{% apibody %}
time.timeOfDay() &rarr; number
{% endapibody %}

Return the number of seconds elapsed since the beginning of the day stored in the time object.

__Example:__ Retrieve posts that were submitted before noon.

```javascript
r.table("posts").filter(
    r.row("date").timeOfDay().le(12*60*60)
).run(conn, callback)
```

[Read more about this command &rarr;](time_of_day/)

## [year](year/) ##

{% apibody %}
time.year() &rarr; number
{% endapibody %}

Return the year of a time object.

__Example:__ Retrieve all the users born in 1986.

```javascript
r.table("users").filter(function(user) {
    return user("birthdate").year().eq(1986)
}).run(conn, callback)
```

[Read more about this command &rarr;](year/)

## [month](month/) ##

{% apibody %}
time.month() &rarr; number
{% endapibody %}

Return the month of a time object as a number between 1 and 12. For your convenience, the terms r.january, r.february etc. are defined and map to the appropriate integer.

__Example:__ Retrieve all the users who were born in November.

```javascript
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

```javascript
r.table("users").filter(
    r.row("birthdate").day().eq(24)
).run(conn, callback)
```

[Read more about this command &rarr;](day/)

## [dayOfWeek](day_of_week/) ##

{% apibody %}
time.dayOfWeek() &rarr; number
{% endapibody %}

Return the day of week of a time object as a number between 1 and 7 (following ISO 8601 standard). For your convenience, the terms r.monday, r.tuesday etc. are defined and map to the appropriate integer.

__Example:__ Return today's day of week.

```javascript
r.now().dayOfWeek().run(conn, callback)
```

[Read more about this command &rarr;](day_of_week/)

## [dayOfYear](day_of_year/) ##

{% apibody %}
time.dayOfYear() &rarr; number
{% endapibody %}

Return the day of the year of a time object as a number between 1 and 366 (following ISO 8601 standard).

__Example:__ Retrieve all the users who were born the first day of a year.

```javascript
r.table("users").filter(
    r.row("birthdate").dayOfYear().eq(1)
)
```

[Read more about this command &rarr;](day_of_year/)

## [hours](hours/) ##

{% apibody %}
time.hours() &rarr; number
{% endapibody %}

Return the hour in a time object as a number between 0 and 23.

__Example:__ Return all the posts submitted after midnight and before 4am.

```javascript
r.table("posts").filter(function(post) {
    return post("date").hours().lt(4)
})
```

[Read more about this command &rarr;](hours/)

## [minutes](minutes/) ##

{% apibody %}
time.minutes() &rarr; number
{% endapibody %}

Return the minute in a time object as a number between 0 and 59.

__Example:__ Return all the posts submitted during the first 10 minutes of every hour.

```javascript
r.table("posts").filter(function(post) {
    return post("date").minutes().lt(10)
})
```

[Read more about this command &rarr;](minutes/)

## [seconds](seconds/) ##

{% apibody %}
time.seconds() &rarr; number
{% endapibody %}

Return the seconds in a time object as a number between 0 and 59.999 (double precision).

__Example:__ Return the post submitted during the first 30 seconds of every minute.

```javascript
r.table("posts").filter(function(post) {
    return post("date").seconds().lt(30)
})
```

[Read more about this command &rarr;](seconds/)

## [toISO8601](to_iso8601/) ##

{% apibody %}
time.toISO8601() &rarr; string
{% endapibody %}

Convert a time object to a string in ISO 8601 format.

__Example:__ Return the current ISO 8601 time.

```javascript
r.now().toISO8601().run(conn, callback)
// Result passed to callback
"2015-04-20T18:37:52.690+00:00"
```

[Read more about this command &rarr;](to_iso8601/)

## [toEpochTime](to_epoch_time/) ##

{% apibody %}
time.toEpochTime() &rarr; number
{% endapibody %}

Convert a time object to its epoch time.

__Example:__ Return the current time in seconds since the Unix Epoch with millisecond-precision.

```javascript
r.now().toEpochTime()
```

[Read more about this command &rarr;](to_epoch_time/)

{% endapisection %}

{% apisection Control structures %}

## [args](args/) ##

{% apibody %}
r.args(array) &rarr; special
{% endapibody %}

`r.args` is a special term that's used to splice an array of arguments
into another term.  This is useful when you want to call a variadic
term such as [getAll](/api/javascript/get_all/) with a set of arguments produced at runtime.

__Example:__ Get Alice and Bob from the table `people`.

```javascript
r.table('people').getAll('Alice', 'Bob').run(conn, callback)
// or
r.table('people').getAll(r.args(['Alice', 'Bob'])).run(conn, callback)
```

[Read more about this command &rarr;](args/)

## [binary](binary/) ##

{% apibody %}
r.binary(data) &rarr; binary
{% endapibody %}

Encapsulate binary data within a query.

__Example:__ Save an avatar image to a existing user record.

```javascript
var fs = require('fs');
fs.readFile('./defaultAvatar.png', function (err, avatarImage) {
    if (err) {
        // Handle error
    }
    else {
        r.table('users').get(100).update({
            avatar: avatarImage
        })
    }
});
```

[Read more about this command &rarr;](binary/)

## [do](do/) ##

{% apibody %}
any.do(function) &rarr; any
r.do([args]*, function) &rarr; any
any.do(expr) &rarr; any
r.do([args]*, expr) &rarr; any
{% endapibody %}

Call an anonymous function using return values from other ReQL commands or queries as arguments.

__Example:__ Compute a golfer's net score for a game.

```javascript
r.table('players').get('f19b5f16-ef14-468f-bd48-e194761df255').do(
    function (player) {
        return player('gross_score').sub(player('course_handicap'));
    }
).run(conn, callback);
```

[Read more about this command &rarr;](do/)

## [branch](branch/) ##

{% apibody %}
r.branch(test, true_action[, test2, test2_action, ...], false_action) &rarr; any
test.branch(true_action[, test2, test2_action, ...], false_action) &rarr; any
{% endapibody %}

Perform a branching conditional equivalent to `if-then-else`.

The `branch` command takes 2n+1 arguments: pairs of conditional expressions and commands to be executed if the conditionals return any value but `false` or `null` (i.e., "truthy" values), with a final "else" command to be evaluated if all of the conditionals are `false` or `null`.

__Example:__ Test the value of x.

```javascript
var x = 10;
r.branch(r.expr(x).gt(5), 'big', 'small').run(conn, callback);
// Result passed to callback
"big"
```

[Read more about this command &rarr;](branch/)

## [forEach](for_each/) ##

{% apibody %}
sequence.forEach(write_function) &rarr; object
{% endapibody %}

Loop over a sequence, evaluating the given write query for each element.

__Example:__ Now that our heroes have defeated their villains, we can safely remove them from the villain table.

```javascript
r.table('marvel').forEach(function(hero) {
    return r.table('villains').get(hero('villainDefeated')).delete()
}).run(conn, callback)
```

[Read more about this command &rarr;](for_each/)

## [range](range/) ##

{% apibody %}
r.range() &rarr; stream
r.range([startValue, ]endValue) &rarr; stream
{% endapibody %}

Generate a stream of sequential integers in a specified range.

__Example:__ Return a four-element range of `[0, 1, 2, 3]`.

```javascript
> r.range(4).run(conn, callback)
// result returned to callback
[0, 1, 2, 3]
```

[Read more about this command &rarr;](range/)

## [error](error/) ##

{% apibody %}
r.error(message) &rarr; error
{% endapibody %}

Throw a runtime error. If called with no arguments inside the second argument to `default`, re-throw the current error.

__Example:__ Iron Man can't possibly have lost a battle:

```javascript
r.table('marvel').get('IronMan').do(function(ironman) {
    return r.branch(ironman('victories').lt(ironman('battles')),
        r.error('impossible code path'),
        ironman)
}).run(conn, callback)
```

[Read more about this command &rarr;](error/)

## [default](default/) ##

{% apibody %}
value.default(default_value | function) &rarr; any
sequence.default(default_value | function) &rarr; any
{% endapibody %}

Provide a default value in case of non-existence errors. The `default` command evaluates its first argument (the value it's chained to). If that argument returns `null` or a non-existence error is thrown in evaluation, then `default` returns its second argument. The second argument is usually a default value, but it can be a function that returns a value.

__Example:__ Retrieve the titles and authors of the table `posts`.
In the case where the author field is missing or `null`, we want to retrieve the string
`Anonymous`.

```javascript
r.table("posts").map(function (post) {
    return {
        title: post("title"),
        author: post("author").default("Anonymous")
    }
}).run(conn, callback);
```

[Read more about this command &rarr;](default/)

## [expr](expr/) ##

{% apibody %}
r.expr(value) &rarr; value
{% endapibody %}

Construct a ReQL JSON object from a native object.

__Example:__ Objects wrapped with `expr` can then be manipulated by ReQL API functions.

```javascript
r.expr({a:'b'}).merge({b:[1,2,3]}).run(conn, callback)
```

[Read more about this command &rarr;](expr/)

## [js](js/) ##

{% apibody %}
r.js(jsString[, {timeout: <number>}]) &rarr; value
{% endapibody %}

Create a javascript expression.

__Example:__ Concatenate two strings using JavaScript.

```javascript
r.js("'str1' + 'str2'").run(conn, callback)
```

[Read more about this command &rarr;](js/)

## [coerceTo](coerce_to/) ##

{% apibody %}
sequence.coerceTo('array') &rarr; array
value.coerceTo('string') &rarr; string
string.coerceTo('number') &rarr; number
array.coerceTo('object') &rarr; object
sequence.coerceTo('object') &rarr; object
object.coerceTo('array') &rarr; array
binary.coerceTo('string') &rarr; string
string.coerceTo('binary') &rarr; binary
{% endapibody %}

Convert a value of one type into another.

__Example:__ Coerce a stream to an array to store its output in a field. (A stream cannot be stored in a field directly.)

```javascript
r.table('posts').map(function (post) {
    return post.merge({ comments: r.table('comments').getAll(post('id'), {index: 'postId'}).coerceTo('array')});
}).run(conn, callback)
```

[Read more about this command &rarr;](coerce_to/)

## [typeOf](type_of/) ##

{% apibody %}
any.typeOf() &rarr; string
{% endapibody %}

Gets the type of a ReQL query's return value.

__Example:__ Get the type of a string.

```javascript
r.expr("foo").typeOf().run(conn, callback);
// Result passed to callback
"STRING"
```

[Read more about this command &rarr;](type_of/)

## [info](info/) ##

{% apibody %}
any.info() &rarr; object
r.info(any) &rarr; object
{% endapibody %}

Get information about a ReQL value.

__Example:__ Get information about a table such as primary key, or cache size.

```javascript
r.table('marvel').info().run(conn, callback)
```

[Read more about this command &rarr;](info/)

## [json](json/) ##

{% apibody %}
r.json(json_string) &rarr; value
{% endapibody %}

Parse a JSON string on the server.

__Example:__ Send an array to the server.

```javascript
r.json("[1,2,3]").run(conn, callback)
```

[Read more about this command &rarr;](json/)

## [toJsonString, toJSON](to_json_string/) ##

{% apibody %}
value.toJsonString() &rarr; string
value.toJSON() &rarr; string
{% endapibody %}

Convert a ReQL value or object to a JSON string. You may use either `toJsonString` or `toJSON`.

__Example:__ Get a ReQL document as a JSON string.

```javascript
> r.table('hero').get(1).toJSON()
// result returned to callback
'{"id": 1, "name": "Batman", "city": "Gotham", "powers": ["martial arts", "cinematic entrances"]}'
```

[Read more about this command &rarr;](to_json_string/)

## [http](http/) ##

{% apibody %}
r.http(url[, options]) &rarr; value
r.http(url[, options]) &rarr; stream
{% endapibody %}

Retrieve data from the specified URL over HTTP.  The return type depends on the `resultFormat` option, which checks the `Content-Type` of the response by default.

__Example:__ Perform an HTTP `GET` and store the result in a table.

```javascript
r.table('posts').insert(r.http('http://httpbin.org/get')).run(conn, callback)
```

[Read more about this command &rarr;](http/)

## [uuid](uuid/) ##

{% apibody %}
r.uuid([string]) &rarr; string
{% endapibody %}

Return a UUID (universally unique identifier), a string that can be used as a unique ID. If a string is passed to `uuid` as an argument, the UUID will be deterministic, derived from the string's SHA-1 hash.

__Example:__ Generate a UUID.

```javascript
> r.uuid().run(conn, callback)
// result returned to callback
"27961a0e-f4e8-4eb3-bf95-c5203e1d87b9"
```

[Read more about this command &rarr;](uuid/)

{% endapisection %}

{% apisection Geospatial commands %}

## [circle](circle/) ##

{% apibody %}
r.circle([longitude, latitude], radius[, {numVertices: 32, geoSystem: 'WGS84', unit: 'm', fill: true}]) &rarr; geometry
r.circle(point, radius[, {numVertices: 32, geoSystem: 'WGS84', unit: 'm', fill: true}]) &rarr; geometry
{% endapibody %}

Construct a circular line or polygon. A circle in RethinkDB is a polygon or line *approximating* a circle of a given radius around a given center, consisting of a specified number of vertices (default 32).

__Example:__ Define a circle.

```javascript
r.table('geo').insert({
    id: 300,
    name: 'Hayes Valley',
    neighborhood: r.circle([-122.423246,37.779388], 1000)
}).run(conn, callback);
```

[Read more about this command &rarr;](circle/)

## [distance](distance/) ##

{% apibody %}
geometry.distance(geometry[, {geoSystem: 'WGS84', unit: 'm'}]) &rarr; number
r.distance(geometry, geometry[, {geoSystem: 'WGS84', unit: 'm'}]) &rarr; number
{% endapibody %}

Compute the distance between a point and another geometry object. At least one of the geometry objects specified must be a point.

__Example:__ Compute the distance between two points on the Earth in kilometers.

```javascript
var point1 = r.point(-122.423246,37.779388);
var point2 = r.point(-117.220406,32.719464);
r.distance(point1, point2, {unit: 'km'}).run(conn, callback);
// result returned to callback
734.1252496021841
```

[Read more about this command &rarr;](distance/)

## [fill](fill/) ##

{% apibody %}
line.fill() &rarr; polygon
{% endapibody %}

Convert a Line object into a Polygon object. If the last point does not specify the same coordinates as the first point, `polygon` will close the polygon by connecting them.

__Example:__ Create a line object and then convert it to a polygon.

```javascript
r.table('geo').insert({
    id: 201,
    rectangle: r.line(
        [-122.423246,37.779388],
        [-122.423246,37.329898],
        [-121.886420,37.329898],
        [-121.886420,37.779388]
    )
}).run(conn, callback);

r.table('geo').get(201).update({
    rectangle: r.row('rectangle').fill()
}, {nonAtomic: true}).run(conn, callback);
```

[Read more about this command &rarr;](fill/)

## [geojson](geojson/) ##

{% apibody %}
r.geojson(geojson) &rarr; geometry
{% endapibody %}

Convert a [GeoJSON](http://geojson.org) object to a ReQL geometry object.

__Example:__ Convert a GeoJSON object to a ReQL geometry object.

```javascript
var geoJson = {
    'type': 'Point',
    'coordinates': [ -122.423246, 37.779388 ]
};
r.table('geo').insert({
    id: 'sfo',
    name: 'San Francisco',
    location: r.geojson(geoJson)
}).run(conn, callback);
```

[Read more about this command &rarr;](geojson/)

## [toGeojson](to_geojson/) ##

{% apibody %}
geometry.toGeojson() &rarr; object
{% endapibody %}

Convert a ReQL geometry object to a [GeoJSON](http://geojson.org) object.

__Example:__ Convert a ReQL geometry object to a GeoJSON object.

```javascript
r.table('geo').get('sfo')('location').toGeojson.run(conn, callback);
// result passed to callback
{
    'type': 'Point',
    'coordinates': [ -122.423246, 37.779388 ]
}
```

[Read more about this command &rarr;](to_geojson/)

## [getIntersecting](get_intersecting/) ##

{% apibody %}
table.getIntersecting(geometry, {index: 'indexname'}) &rarr; selection<stream>
{% endapibody %}

Get all documents where the given geometry object intersects the geometry object of the requested geospatial index.

__Example:__ Which of the locations in a list of parks intersect `circle1`?

```javascript
var circle1 = r.circle([-117.220406,32.719464], 10, {unit: 'mi'});
r.table('parks').getIntersecting(circle1, {index: 'area'}).run(conn, callback);
```

[Read more about this command &rarr;](get_intersecting/)

## [getNearest](get_nearest/) ##

{% apibody %}
table.getNearest(point, {index: 'indexname'[, maxResults: 100, maxDist: 100000, unit: 'm', geoSystem: 'WGS84']}) &rarr; array
{% endapibody %}

Return a list of documents closest to a specified point based on a geospatial index, sorted in order of increasing distance.

__Example:__ Return a list of the closest 25 enemy hideouts to the secret base.

```javascript
var secretBase = r.point(-122.422876,37.777128);
r.table('hideouts').getNearest(secretBase,
    {index: 'location', maxResults: 25}
).run(conn, callback)
```

[Read more about this command &rarr;](get_nearest/)

## [includes](includes/) ##

{% apibody %}
sequence.includes(geometry) &rarr; sequence
geometry.includes(geometry) &rarr; bool
{% endapibody %}

Tests whether a geometry object is completely contained within another. When applied to a sequence of geometry objects, `includes` acts as a [filter](/api/javascript/filter), returning a sequence of objects from the sequence that include the argument.

__Example:__ Is `point2` included within a 2000-meter circle around `point1`?

```javascript
var point1 = r.point(-117.220406,32.719464);
var point2 = r.point(-117.206201,32.725186);
r.circle(point1, 2000).includes(point2).run(conn, callback);
// result returned to callback
true
```

[Read more about this command &rarr;](includes/)

## [intersects](intersects/) ##

{% apibody %}
sequence.intersects(geometry) &rarr; sequence
geometry.intersects(geometry) &rarr; bool
r.intersects(sequence, geometry) &rarr; sequence
r.intersects(geometry, geometry) &rarr; bool
{% endapibody %}

Tests whether two geometry objects intersect with one another. When applied to a sequence of geometry objects, `intersects` acts as a [filter](/api/javascript/filter), returning a sequence of objects from the sequence that intersect with the argument.

__Example:__ Is `point2` within a 2000-meter circle around `point1`?

```javascript
var point1 = r.point(-117.220406,32.719464);
var point2 = r.point(-117.206201,32.725186);
r.circle(point1, 2000).intersects(point2).run(conn, callback);
// result returned to callback
true
```

[Read more about this command &rarr;](intersects/)

## [line](line/) ##

{% apibody %}
r.line([lon1, lat1], [lon2, lat2], ...) &rarr; line
r.line(point1, point2, ...) &rarr; line
{% endapibody %}

Construct a geometry object of type Line. The line can be specified in one of two ways:

* Two or more two-item arrays, specifying latitude and longitude numbers of the line's vertices;
* Two or more [Point](/api/javascript/point) objects specifying the line's vertices.

__Example:__ Define a line.

```javascript
r.table('geo').insert({
    id: 101,
    route: r.line([-122.423246,37.779388], [-121.886420,37.329898])
}).run(conn, callback);
```

[Read more about this command &rarr;](line/)

## [point](point/) ##

{% apibody %}
r.point(longitude, latitude) &rarr; point
{% endapibody %}

Construct a geometry object of type Point. The point is specified by two floating point numbers, the longitude (&minus;180 to 180) and latitude (&minus;90 to 90) of the point on a perfect sphere. See [Geospatial support](/docs/geo-support/) for more information on ReQL's coordinate system.

__Example:__ Define a point.

```javascript
r.table('geo').insert({
    id: 1,
    name: 'San Francisco',
    location: r.point(-122.423246,37.779388)
}).run(conn, callback);
```

[Read more about this command &rarr;](point/)

## [polygon](polygon/) ##

{% apibody %}
r.polygon([lon1, lat1], [lon2, lat2], [lon3, lat3], ...) &rarr; polygon
r.polygon(point1, point2, point3, ...) &rarr; polygon
{% endapibody %}

Construct a geometry object of type Polygon. The Polygon can be specified in one of two ways:

* Three or more two-item arrays, specifying latitude and longitude numbers of the polygon's vertices;
* Three or more [Point](/api/javascript/point) objects specifying the polygon's vertices.

__Example:__ Define a polygon.

```javascript
r.table('geo').insert({
    id: 101,
    rectangle: r.polygon(
        [-122.423246,37.779388],
        [-122.423246,37.329898],
        [-121.886420,37.329898],
        [-121.886420,37.779388]
    )
}).run(conn, callback);
```

[Read more about this command &rarr;](polygon/)

## [polygonSub](polygon_sub/) ##

{% apibody %}
polygon1.polygonSub(polygon2) &rarr; polygon
{% endapibody %}

Use `polygon2` to "punch out" a hole in `polygon1`. `polygon2` must be completely contained within `polygon1` and must have no holes itself (it must not be the output of `polygonSub` itself).

__Example:__ Define a polygon with a hole punched in it.

```javascript
var outerPolygon = r.polygon(
    [-122.4,37.7],
    [-122.4,37.3],
    [-121.8,37.3],
    [-121.8,37.7]
);
var innerPolygon = r.polygon(
    [-122.3,37.4],
    [-122.3,37.6],
    [-122.0,37.6],
    [-122.0,37.4]
);
outerPolygon.polygonSub(innerPolygon).run(conn, callback);
```

[Read more about this command &rarr;](polygon_sub/)

{% endapisection %}

{% apisection Administration %}

## [grant](grant/) ##

{% apibody %}
r.grant("username", {permission: bool[, ...]}) &rarr; object
db.grant("username", {permission: bool[, ...]}) &rarr; object
table.grant("username", {permission: bool[, ...]}) &rarr; object
{% endapibody %}

Grant or deny access permissions for a user account, globally or on a per-database or per-table basis.

__Example:__ Grant the `chatapp` user account read and write permissions on the `users` database.

```javascript
r.db('users').grant('chatapp', {read: true, write: true}).run(conn, callback);

// Result passed to callback
{
    "granted": 1,
    "permissions_changes": [
        {
            "new_val": { "read": true, "write": true },
            "old_val": { null }
        }
    ]
```

[Read more about this command &rarr;](grant/)

## [config](config/) ##

{% apibody %}
table.config() &rarr; selection&lt;object&gt;
database.config() &rarr; selection&lt;object&gt;
{% endapibody %}

Query (read and/or update) the configurations for individual tables or databases.

__Example:__ Get the configuration for the `users` table.

```javascript
> r.table('users').config().run(conn, callback);
```

[Read more about this command &rarr;](config/)

## [rebalance](rebalance/) ##

{% apibody %}
table.rebalance() &rarr; object
database.rebalance() &rarr; object
{% endapibody %}

Rebalances the shards of a table. When called on a database, all the tables in that database will be rebalanced.

__Example:__ Rebalance a table.

```javascript
> r.table('superheroes').rebalance().run(conn, callback);
```

[Read more about this command &rarr;](rebalance/)

## [reconfigure](reconfigure/) ##

{% apibody %}
table.reconfigure({shards: <s>, replicas: <r>[, primaryReplicaTag: <t>, dryRun: false, nonvotingReplicaTags: null}]) &rarr; object
database.reconfigure({shards: <s>, replicas: <r>[, primaryReplicaTag: <t>, dryRun: false, nonvotingReplicaTags: null}]) &rarr; object
table.reconfigure(emergencyRepair: <option>, dryRun: false) &rarr; object
{% endapibody %}

Reconfigure a table's sharding and replication.

__Example:__ Reconfigure a table.

```javascript
> r.table('superheroes').reconfigure({shards: 2, replicas: 1}).run(conn, callback);
```

[Read more about this command &rarr;](reconfigure/)

## [status](status/) ##

{% apibody %}
table.status() &rarr; selection&lt;object&gt;
{% endapibody %}

Return the status of a table.

__Example:__ Get a table's status.

```javascript
> r.table('superheroes').status().run(conn, callback);
```

[Read more about this command &rarr;](status/)

## [wait](wait/) ##

{% apibody %}
table.wait([{waitFor: 'all_replicas_ready', timeout: <sec>}]) &rarr; object
database.wait([{waitFor: 'all_replicas_ready', timeout: <sec>}]) &rarr; object
r.wait(table | database, [{waitFor: 'all_replicas_ready', timeout: <sec>}]) &rarr; object
{% endapibody %}

Wait for a table or all the tables in a database to be ready. A table may be temporarily unavailable after creation, rebalancing or reconfiguring. The `wait` command blocks until the given table (or database) is fully up to date.

__Example:__ Wait on a table to be ready.

```javascript
> r.table('superheroes').wait().run(conn, callback);
// Result passed to callback
{ "ready": 1 }
```

[Read more about this command &rarr;](wait/)

{% endapisection %}

