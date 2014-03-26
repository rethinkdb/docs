---
layout: api
title: "ReQL command reference"
active: api
no_footer: true
permalink: api/python/
language: Python
---

{% apisection Accessing ReQL%}
All ReQL queries begin from the top-level module.

## [r](r/) ##

{% apibody %}
r &rarr; r
{% endapibody %}

The top-level ReQL namespace.

__Example:__ Set up your top-level namespace.

```py
import rethinkdb as r
```

## [connect](connect/) ##

{% apibody %}
r.connect(host="localhost", port=28015, db="test", auth_key="", timeout=20)
    &rarr; connection
r.connect(host) &rarr; connection
{% endapibody %}

Create a new connection to the database server. The keyword arguments are:

- `host`: host of the RethinkDB instance. The default value is `localhost`.
- `port`: the driver port, by default `28015`.
- `db`: the database used if not explicitly specified in a query, by default `test`.
- `auth_key`: the authentification key, by default the empty string.
- `timeout`: timeout period for the connection to be opened, by default `20` (seconds).

If the connection cannot be established, a `RqlDriverError` exception
will be thrown.

__Example:__ Opens a connection using the default host and port but
specifying the default database.

```py
conn = r.connect(db='marvel')
```

[Read more about this command &rarr;](connect/)


## [repl](repl/) ##

{% apibody %}
conn.repl()
{% endapibody %}

Set the default connection to make REPL use easier. Allows calling
`.run()` on queries without specifying a connection.

Connection objects are not thread-safe and REPL connections should not
be used in multi-threaded environments.

__Example:__ Set the default connection for the REPL, then call
`run()` without specifying the connection.

```py
r.connect(db='marvel').repl()
r.table('heroes').run()
```

## [close](close/) ##

{% apibody %}
conn.close(noreply_wait=True)
{% endapibody %}

Close an open connection. Closing a connection waits until all
outstanding requests have finished and then frees any open resources
associated with the connection.  If `noreply_wait` is set to `false`,
all outstanding requests are canceled immediately.

Closing a connection cancels all outstanding requests and frees the
memory associated with any open cursors.

__Example:__ Close an open connection, waiting for noreply writes to finish.

```py
conn.close()
```

__Example:__ Close an open connection immediately.

```py
conn.close(noreply_wait=False)
```

## [reconnect](reconnect/) ##

{% apibody %}
conn.reconnect(noreply_wait=True)
{% endapibody %}

Close and reopen a connection. Closing a connection waits until all
outstanding requests have finished.  If `noreply_wait` is set to
`false`, all outstanding requests are canceled immediately.

__Example:__ Cancel outstanding requests/queries that are no longer needed.

```py
conn.reconnect(noreply_wait=False)
```

## [use](use/) ##

{% apibody %}
conn.use(db_name)
{% endapibody %}

Change the default database on this connection.

__Example:__ Change the default database so that we don't need to
specify the database when referencing a table.

```py
conn.use('marvel')
r.table('heroes').run(conn) # refers to r.db('marvel').table('heroes')
```

## [run](run/) ##

{% apibody %}
query.run(conn, use_outdated=False, time_format='native', profile=False, durability="hard") &rarr; cursor
query.run(conn, use_outdated=False, time_format='native', profile=False, durability="hard") &rarr; object
{% endapibody %}

Run a query on a connection, returning either a single JSON result or
a cursor, depending on the query.

__Example:__ Run a query on the connection `conn` and print out every
row in the result.

```py
for doc in r.table('marvel').run(conn):
    print doc
```

[Read more about this command &rarr;](run/)

## [noreply_wait](noreply_wait/) ##

{% apibody %}
conn.noreply_wait()
{% endapibody %}

`noreply_wait` ensures that previous queries with the `noreply` flag have been processed
by the server. Note that this guarantee only applies to queries run on the given connection.

__Example:__ We have previously run queries with the `noreply` argument set to `True`. Now
wait until the server has processed them.

```py
conn.noreply_wait()
```

## [close (cursor)](close-cursor/) ##

{% apibody %}
cursor.close()
{% endapibody %}


Close a cursor. Closing a cursor cancels the corresponding query and frees the memory
associated with the open request.

__Example:__ Close a cursor.

```py
cursor.close()
```



{% endapisection %}



{% apisection Manipulating databases%}

## [db_create](db_create/) ##

{% apibody %}
r.db_create(db_name) &rarr; object
{% endapibody %}

Create a database. A RethinkDB database is a collection of tables, similar to
relational databases.

If successful, the operation returns an object: `{"created": 1}`. If a database with the
same name already exists the operation throws `RqlRuntimeError`.

Note: that you can only use alphanumeric characters and underscores for the database name.

__Example:__ Create a database named 'superheroes'.

```py
r.db_create('superheroes').run(conn)
```


## [db_drop](db_drop/) ##

{% apibody %}
r.db_drop(db_name) &rarr; object
{% endapibody %}

Drop a database. The database, all its tables, and corresponding data will be deleted.

If successful, the operation returns the object `{"dropped": 1}`. If the specified database
doesn't exist a `RqlRuntimeError` is thrown.

__Example:__ Drop a database named 'superheroes'.

```py
r.db_drop('superheroes').run(conn)
```


## [db_list](db_list/) ##

{% apibody %}
r.db_list() &rarr; array
{% endapibody %}

List all database names in the system. The result is a list of strings.

__Example:__ List all databases.

```py
r.db_list().run(conn)
```

{% endapisection %}




{% apisection Manipulating tables%}
## [table_create](table_create/) ##

{% apibody %}
db.table_create(table_name[, options]) &rarr; object
{% endapibody %}

Create a table. A RethinkDB table is a collection of JSON documents.

If successful, the operation returns an object: `{created: 1}`. If a table with the same
name already exists, the operation throws `RqlRuntimeError`.

Note: that you can only use alphanumeric characters and underscores for the table name.

When creating a table you can specify the following options:

- `primary_key`: the name of the primary key. The default primary key is id;
- `durability`: if set to `'soft'`, this enables _soft durability_ on this table:
writes will be acknowledged by the server immediately and flushed to disk in the
background. Default is `'hard'` (acknowledgement of writes happens after data has been
written to disk);
- `datacenter`: the name of the datacenter this table should be assigned to.


__Example:__ Create a table named 'dc_universe' with the default settings.

```py
r.db('test').table_create('dc_universe').run(conn)
```

[Read more about this command &rarr;](table_create/)

## [table_drop](table_drop/) ##

{% apibody %}
db.table_drop(table_name) &rarr; object
{% endapibody %}

Drop a table. The table and all its data will be deleted.

If succesful, the operation returns an object: {"dropped": 1}. If the specified table
doesn't exist a `RqlRuntimeError` is thrown.

__Example:__ Drop a table named 'dc_universe'.

```py
r.db('test').table_drop('dc_universe').run(conn)
```


## [table_list](table_list/) ##

{% apibody %}
db.table_list() &rarr; array
{% endapibody %}

List all table names in a database. The result is a list of strings.

__Example:__ List all tables of the 'test' database.

```py
r.db('test').table_list().run(conn)

```


## [index_create](index_create/) ##

{% apibody %}
table.index_create(index_name[, index_function]) &rarr; object
{% endapibody %}

Create a new secondary index on this table.

__Example:__ To efficiently query our heros by code name we have to create a secondary
index.

```py
r.table('dc').index_create('code_name').run(conn)
```

[Read more about this command &rarr;](index_create/)


## [index_drop](index_drop/) ##

{% apibody %}
table.index_drop(index_name) &rarr; object
{% endapibody %}

Delete a previously created secondary index of this table.

__Example:__ Drop a secondary index named 'code_name'.

```py
r.table('dc').index_drop('code_name').run(conn)
```


## [index_list](index_list/) ##

{% apibody %}
table.index_list() &rarr; array
{% endapibody %}

List all the secondary indexes of this table.

__Example:__ List the available secondary indexes for this table.

```py
r.table('marvel').index_list().run(conn)
```

## [index_status](index_status/) ##

{% apibody %}
table.index_status([, index...]) &rarr; array
{% endapibody %}

Get the status of the specified indexes on this table, or the status
of all indexes on this table if no indexes are specified.

__Example:__ Get the status of all the indexes on `test`:

```py
r.table('test').index_status().run(conn)
```

__Example:__ Get the status of the `timestamp` index:

```py
r.table('test').index_status('timestamp').run(conn)
```

## [index_wait](index_wait/) ##

{% apibody %}
table.index_wait([, index...]) &rarr; array
{% endapibody %}

Wait for the specified indexes on this table to be ready, or for all
indexes on this table to be ready if no indexes are specified.

__Example:__ Wait for all indexes on the table `test` to be ready:

```py
r.table('test').index_wait().run(conn)
```

__Example:__ Wait for the index `timestamp` to be ready:

```py
r.table('test').index_wait('timestamp').run(conn)
```

{% endapisection %}


{% apisection Writing data%}

## [insert](insert/) ##

{% apibody %}
table.insert(json | [json]
    [, durability="hard", return_vals=False, upsert=False])
        &rarr; object
{% endapibody %}

Insert documents into a table. Accepts a single document or an array of
documents.

__Example:__ Insert a document into the table `posts`.

```py
r.table("posts").insert({
    "id": 1,
    "title": "Lorem ipsum",
    "content": "Dolor sit amet"
}).run(conn)
```

[Read more about this command &rarr;](insert/)


## [update](update/) ##

{% apibody %}
table.update(json | exp
    [, durability="hard", return_vals=False, non_atomic=False])
        &rarr; object
selection.update(json | exp
    [, durability="hard", return_vals=False, non_atomic=False])
        &rarr; object
singleSelection.update(json | exp
    [, durability="hard", return_vals=False, non_atomic=False])
        &rarr; object
{% endapibody %}

Update JSON documents in a table. Accepts a JSON document, a ReQL expression, or a
combination of the two.

__Example:__ Update the status of the post with `id` of `1` to `published`.

```py
r.table("posts").get(1).update({"status": "published"}).run(conn)
```

[Read more about this command &rarr;](update/)


## [replace](replace/) ##

{% apibody %}
table.replace(json | expr
    [, durability="hard", return_vals=False, non_atomic=False])
        &rarr; object
selection.replace(json | expr
    [, durability="hard", return_vals=False, non_atomic=False])
        &rarr; object
singleSelection.replace(json | expr
    [, durability="hard", return_vals=False, non_atomic=False])
        &rarr; object
{% endapibody %}

Replace documents in a table. Accepts a JSON document or a ReQL expression, and replaces
the original document with the new one. The new document must have the same primary key
as the original document.

__Example:__ Replace the document with the primary key `1`.

```py
r.table("posts").get(1).replace({
    "id": 1,
    "title": "Lorem ipsum",
    "content": "Aleas jacta est",
    "status": "draft"
}).run(conn)
```

[Read more about this command &rarr;](replace/)

## [delete](delete/) ##

{% apibody %}
table.delete([durability="hard", return_vals=False])
    &rarr; object
selection.delete([durability="hard", return_vals=False])
    &rarr; object
singleSelection.delete([durability="hard", return_vals=False])
    &rarr; object
{% endapibody %}


Delete one or more documents from a table.

__Example:__ Delete a single document from the table `comments`.

```py
r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete().run(conn)
```


[Read more about this command &rarr;](delete/)

## [sync](sync/) ##

{% apibody %}
table.sync()
    &rarr; object
{% endapibody %}

`sync` ensures that writes on a given table are written to permanent storage. Queries
that specify soft durability (`durability='soft'`) do not give such guarantees, so
`sync` can be used to ensure the state of these queries. A call to `sync` does not return
until all previous writes to the table are persisted.


__Example:__ After having updated multiple heroes with soft durability, we now want to wait
until these changes are persisted.

```py
r.table('marvel').sync().run(conn)
```

{% endapisection %}


{% apisection Selecting data%}

## [db](db/) ##

{% apibody %}
r.db(db_name) &rarr; db
{% endapibody %}

Reference a database.

__Example:__ Before we can query a table we have to select the correct database.

```py
r.db('heroes').table('marvel').run(conn)
```


## [table](table/) ##

{% apibody %}
db.table(name[, use_outdated=False]) &rarr; table
{% endapibody %}

Select all documents in a table. This command can be chained with other commands to do
further processing on the data.

__Example:__ Return all documents in the table 'marvel' of the default database.

```py
r.table('marvel').run(conn)
```

[Read more about this command &rarr;](table/)

## [get](get/) ##

{% apibody %}
table.get(key) &rarr; singleRowSelection
{% endapibody %}

Get a document by primary key.

__Example:__ Find a document with the primary key 'superman'.

```py
r.table('marvel').get('superman').run(conn)
```


## [get_all](get_all/)##

{% apibody %}
table.get_all(key1[, key2...], [, index='id']) &rarr; selection
{% endapibody %}

Get all documents where the given value matches the value of the requested index.

__Example:__ Secondary index keys are not guaranteed to be unique so we cannot query via
"get" when using a secondary index.

```py
r.table('marvel').get_all('man_of_steel', index='code_name').run(conn)
```

[Read more about this command &rarr;](get_all/)


## [between](between/) ##

{% apibody %}
table.between(lower_key, upper_key
    [, index='id', left_bound='closed', right_bound='open'])
        &rarr; selection
{% endapibody %}

Get all documents between two keys. Accepts three optional arguments: `index`,
`left_bound`, and `right_bound`. If `index` is set to the name of a secondary index,
`between` will return all documents where that index's value is in the specified range
(it uses the primary key by default). `left_bound` or `right_bound` may be set to `open`
or `closed` to indicate whether or not to include that endpoint of the range (by default,
`left_bound` is closed and `right_bound` is open).

__Example:__ Find all users with primary key >= 10 and < 20 (a normal half-open interval).

```py
r.table('marvel').between(10, 20).run(conn)
```

[Read more about this command &rarr;](between/)

## [filter](filter/) ##

{% apibody %}
sequence.filter(predicate, default=False) &rarr; selection
stream.filter(predicate, default=False) &rarr; stream
array.filter(predicate, default=False) &rarr; array
{% endapibody %}

Get all the documents for which the given predicate is true.

`filter` can be called on a sequence, selection, or a field containing an array of
elements. The return type is the same as the type on which the function was called on.

The body of every filter is wrapped in an implicit `.default(False)`, which means that
if a non-existence errors is thrown (when you try to access a field that does not exist
in a document), RethinkDB will just ignore the document.
The `default` value can be changed by passing the named argument `default`.
Setting this optional argument to `r.error()` will cause any non-existence errors to
return a `RqlRuntimeError`.


__Example:__ Get all the users that are 30 years old.

```py
r.table('users').filter({"age": 30}).run(conn)
```

[Read more about this command &rarr;](filter/)


{% endapisection %}


{% apisection Joins%}
These commands allow the combination of multiple sequences into a single sequence

## [inner_join](inner_join/) ##

{% apibody %}
sequence.inner_join(other_sequence, predicate) &rarr; stream
array.inner_join(other_sequence, predicate) &rarr; array
{% endapibody %}

Returns the inner product of two sequences (e.g. a table, a filter result) filtered by
the predicate. The query compares each row of the left sequence with each row of the
right sequence to find all pairs of rows which satisfy the predicate. When the predicate
is satisfied, each matched pair of rows of both sequences are combined into a result row.

__Example:__ Construct a sequence of documents containing all cross-universe matchups where a marvel hero would lose.

```py
r.table('marvel').inner_join(r.table('dc'), lambda marvelRow, dcRow:
    marvelRow['strength'] < dcRow['strength']).run(conn)
```


## [outer_join](outer_join/) ##

{% apibody %}
sequence.outer_join(other_sequence, predicate) &rarr; stream
array.outer_join(other_sequence, predicate) &rarr; array
{% endapibody %}

Computes a left outer join by retaining each row in the left table even if no match was
found in the right table.

__Example:__ Construct a sequence of documents containing all cross-universe matchups
where a marvel hero would lose, but keep marvel heroes who would never lose a matchup in
the sequence.

```py
r.table('marvel').outer_join(r.table('dc'),
  lambda marvelRow, dcRow: marvelRow['strength'] < dcRow['strength']).run(conn)
```


## [eq_join](eq_join/) ##

{% apibody %}
sequence.eq_join(left_attr, other_table[, index='id']) &rarr; stream
array.eq_join(left_attr, other_table[, index='id']) &rarr; array
{% endapibody %}

An efficient join that looks up elements in the right table by primary key.

__Example:__ Let our heroes join forces to battle evil!

```py
r.table('marvel').eq_join('main_dc_collaborator', r.table('dc')).run(conn)
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
r.table('marvel').eq_join('main_dc_collaborator', r.table('dc')).zip().run(conn)
```



{% endapisection %}

{% apisection Transformations%}
These commands are used to transform data in a sequence.

## [map](map/) ##

{% apibody %}
sequence.map(mapping_function) &rarr; stream
array.map(mapping_function) &rarr; array
{% endapibody %}

Transform each element of the sequence by applying the given mapping function.

__Example:__ Construct a sequence of hero power ratings.

```py
r.table('marvel').map(lambda hero:
    hero['combatPower'] + hero['compassionPower'] * 2
).run(conn)
```


## [with_fields](with_fields/) ##

{% apibody %}
sequence.with_fields([selector1, selector2...]) &rarr; stream
array.with_fields([selector1, selector2...]) &rarr; array
{% endapibody %}

Takes a sequence of objects and a list of fields. If any objects in the sequence don't
have all of the specified fields, they're dropped from the sequence. The remaining
objects have the specified fields plucked out. (This is identical to `has_fields`
followed by `pluck` on a sequence.)

__Example:__ Get a list of heroes and their nemeses, excluding any heroes that lack one.

```py
r.table('marvel').with_fields('id', 'nemesis')
```

[Read more about this command &rarr;](with_fields/)


## [concat_map](concat_map/) ##

{% apibody %}
sequence.concat_map(mapping_function) &rarr; stream
array.concat_map(mapping_function) &rarr; array
{% endapibody %}

Flattens a sequence of arrays returned by the mappingFunction into a single sequence.

__Example:__ Construct a sequence of all monsters defeated by Marvel heroes. Here the field
'defeatedMonsters' is a list that is concatenated to the sequence.

```py
r.table('marvel').concat_map(lambda hero: hero['defeatedMonsters']).run(conn)
```


## [order_by](order_by/) ##

{% apibody %}
table.order_by([key1...], index=index_name) -> selection<stream>
selection.order_by(key1, [key2...]) -> selection<array>
sequence.order_by(key1, [key2...]) -> array
{% endapibody %}

Sort the sequence by document values of the given key(s). `orderBy` defaults to ascending
ordering. To explicitly specify the ordering, wrap the attribute with either `r.asc` or
`r.desc`.

__Example:__ Order our heroes by a series of performance metrics.

```py
r.table('marvel').order_by('enemies_vanquished', 'damsels_saved').run(conn)
```

[Read more about this command &rarr;](order_by/)


## [skip](skip/) ##

{% apibody %}
sequence.skip(n) &rarr; stream
array.skip(n) &rarr; array
{% endapibody %}

Skip a number of elements from the head of the sequence.

__Example:__ Here in conjunction with `order_by` we choose to ignore the most successful heroes.

```py
r.table('marvel').order_by('successMetric').skip(10).run(conn)
```


## [limit](limit/) ##

{% apibody %}
sequence.limit(n) &rarr; stream
array.limit(n) &rarr; array
{% endapibody %}


End the sequence after the given number of elements.

__Example:__ Only so many can fit in our Pantheon of heroes.

```py
r.table('marvel').order_by('belovedness').limit(10).run(conn)
```

## [\[\]](slice/) ##

{% apibody %}
sequence[start_index[:end_index]] &rarr; stream
array[start_index[:end_index]] &rarr; array
{% endapibody %}

Trim the sequence to within the bounds provided.

__Example:__ For this fight, we need heroes with a good mix of strength and agility.

```py
r.table('marvel').order_by('strength')[5:10].run(conn)
```

## [\[\]](nth/) ##

{% apibody %}
sequence[index] &arr; object
sequence.nth(index) &rarr; object
{% endapibody %}

Get the nth element of a sequence.

__Example:__ Select the second element in the array.

```py
r.expr([1,2,3])[1].run(conn)
r.expr([1,2,3]).nth(1).run(conn)
```


## [indexes_of](indexes_of/) ##

{% apibody %}
sequence.indexes_of(datum | predicate) &rarr; array
{% endapibody %}

Get the indexes of an element in a sequence. If the argument is a predicate, get the indexes of all elements matching it.

__Example:__ Find the position of the letter 'c'.

```py
r.expr(['a','b','c']).indexes_of('c').run(conn)
```

[Read more about this command &rarr;](indexes_of/)


## [is_empty](is_empty/) ##

{% apibody %}
sequence.is_empty() &rarr; bool
{% endapibody %}

Test if a sequence is empty.

__Example:__ Are there any documents in the marvel table?

```py
r.table('marvel').is_empty().run(conn)
```

## [union](union/) ##

{% apibody %}
sequence.union(sequence) &rarr; array
{% endapibody %}

Concatenate two sequences.

__Example:__ Construct a stream of all heroes.

```py
r.table('marvel').union(r.table('dc')).run(conn)
```


## [sample](sample/) ##

{% apibody %}
sequence.sample(number) &rarr; selection
stream.sample(number) &rarr; array
array.sample(number) &rarr; array
{% endapibody %}

Select a given number of elements from a sequence with uniform random distribution. Selection is done without replacement.

__Example:__ Select 3 random heroes.

```py
r.table('marvel').sample(3).run(conn)
```


{% endapisection %}


{% apisection Aggregation%}
These commands are used to compute smaller values from large sequences.


## [group](group/) ##

{% apibody %}
sequence.group(field_or_function..., [index='index_name']) &rarr; grouped_stream
{% endapibody %}

Takes a stream and partitions it into multiple groups based on the
fields or functions provided.  Commands chained after `group` will be
called on each of these grouped sub-streams, producing grouped data.

__Example:__ What is each player's best game?

```py
r.table('games').group('player').max('points').run(conn)
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

The format of the array returned by `ungroup` is the same as the
default native format of grouped data in the javascript driver and
data explorer.

__Example:__ What is the maximum number of points scored by each
player, with the highest scorers first?

```py
r.table('games')
    .group('player').max('points')['points']
    .ungroup().order_by(r.desc('reduction')).run(conn)
```

[Read more about this command &rarr;](ungroup/)



## [reduce](reduce/) ##

{% apibody %}
sequence.reduce(reduction_function) &rarr; value
{% endapibody %}

Produce a single value from a sequence through repeated application of a reduction
function.

Produces a single value from a sequence by repeatedly calling the
reduction function.  The reduction function should take two arguments
and combine them together.  The arguments to the reduction function
can be either elements of the stream, or the results of a previous
call to the reduction function.

__Example:__ What's the product of all the bonus multipliers in game 7324?

```py
r.table('games').get(7324)['bonus_multipliers'].reduce(lambda a, b: a*b).run(conn)
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

```py
(r.table('marvel').count() + r.table('dc').count()).run(conn)
```

[Read more about this command &rarr;](count/)


## [sum](sum/) ##

{% apibody %}
sequence.sum([field_or_function]) &rarr; number
{% endapibody %}

Sums all the elements of a sequence.  If called with a field name,
sums all the values of that field in the sequence, skipping elements
of the sequence that lack that field.  If called with a function,
calls that function on every element of the sequence and sums the
results, skipping elements of the sequence where that function returns
`null` or a non-existence error.

__Example:__ What's 3 + 5 + 7?

```py
r.expr([3, 5, 7]).sum().run(conn)
```

[Read more about this command &rarr;](sum/)



## [avg](avg/) ##

{% apibody %}
sequence.avg([field_or_function]) &rarr; number
{% endapibody %}

Averages all the elements of a sequence.  If called with a field name,
averages all the values of that field in the sequence, skipping
elements of the sequence that lack that field.  If called with a
function, calls that function on every element of the sequence and
averages the results, skipping elements of the sequence where that
function returns `null` or a non-existence error.


__Example:__ What's the average of 3, 5, and 7?

```py
r.expr([3, 5, 7]).avg().run(conn)
```


[Read more about this command &rarr;](avg/)


## [min](min/) ##

{% apibody %}
sequence.min([field_or_function]) &rarr; element
{% endapibody %}

Finds the minimum of a sequence.  If called with a field name, finds
the element of that sequence with the smallest value in that field.
If called with a function, calls that function on every element of the
sequence and returns the element which produced the smallest value,
ignoring any elements where the function returns `null` or produces a
non-existence error.

__Example:__ What's the minimum of 3, 5, and 7?

```py
r.expr([3, 5, 7]).min().run(conn)
```


[Read more about this command &rarr;](min/)


## [max](max/) ##

{% apibody %}
sequence.max([field_or_function]) &rarr; element
{% endapibody %}

Finds the maximum of a sequence.  If called with a field name, finds
the element of that sequence with the largest value in that field.  If
called with a function, calls that function on every element of the
sequence and returns the element which produced the largest value,
ignoring any elements where the function returns `null` or produces a
non-existence error.


__Example:__ What's the maximum of 3, 5, and 7?

```py
r.expr([3, 5, 7]).max().run(conn)
```

[Read more about this command &rarr;](max/)



## [distinct](distinct/) ##

{% apibody %}
sequence.distinct() &rarr; array
{% endapibody %}

Remove duplicate elements from the sequence.

__Example:__ Which unique villains have been vanquished by marvel heroes?

```py
r.table('marvel').concat_map(lambda hero: hero['villainList']).distinct().run(conn)
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

```py
r.table('marvel').get('ironman')['opponents'].contains('superman').run(conn)
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

```py
r.table('users').filter(r.row['age'] > 5).run(conn)
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

```py
r.table('marvel').get('IronMan').pluck('reactorState', 'reactorPower').run(conn)
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

```py
r.table('marvel').get('IronMan').without('personalVictoriesList').run(conn)
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

```py
r.table('marvel').get('IronMan').merge(
    r.table('loadouts').get('alienInvasionKit')
).run(conn)
```

[Read more about this command &rarr;](merge/)

## [append](append/) ##

{% apibody %}
array.append(value) &rarr; array
{% endapibody %}

Append a value to an array.

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```py
r.table('marvel').get('IronMan')['equipment'].append('newBoots').run(conn)
```


## [prepend](prepend/) ##

{% apibody %}
array.prepend(value) &rarr; array
{% endapibody %}

Prepend a value to an array.

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```py
r.table('marvel').get('IronMan')['equipment'].prepend('newBoots').run(conn)
```


## [difference](difference/) ##

{% apibody %}
array.difference(array) &rarr; array
{% endapibody %}

Remove the elements of one array from another array.

__Example:__ Retrieve Iron Man's equipment list without boots.

```py
r.table('marvel').get('IronMan')['equipment'].difference(['Boots']).run(conn)
```


## [set_insert](set_insert/) ##

{% apibody %}
array.set_insert(value) &rarr; array
{% endapibody %}

Add a value to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots.

```py
r.table('marvel').get('IronMan')['equipment'].set_insert('newBoots').run(conn)
```


## [set_union](set_union/) ##

{% apibody %}
array.set_union(array) &rarr; array
{% endapibody %}

Add a several values to an array and return it as a set (an array with distinct values).

__Example:__ Retrieve Iron Man's equipment list with the addition of some new boots and an arc reactor.

```py
r.table('marvel').get('IronMan')['equipment'].set_union(['newBoots', 'arc_reactor']).run(conn)
```


## [set_intersection](set_intersection/) ##

{% apibody %}
array.set_intersection(array) &rarr; array
{% endapibody %}

Intersect two arrays returning values that occur in both of them as a set (an array with
distinct values).

__Example:__ Check which pieces of equipment Iron Man has from a fixed list.

```py
r.table('marvel').get('IronMan')['equipment'].set_intersection(['newBoots', 'arc_reactor']).run(conn)
```


## [set_difference](set_difference/) ##

{% apibody %}
array.set_difference(array) &rarr; array
{% endapibody %}

Remove the elements of one array from another and return them as a set (an array with
distinct values).

__Example:__ Check which pieces of equipment Iron Man has, excluding a fixed list.

```py
r.table('marvel').get('IronMan')['equipment'].set_difference(['newBoots', 'arc_reactor']).run(conn)
```


## [\[\]](get_field/) ##

{% apibody %}
sequence[attr] &rarr; sequence
singleSelection[attr] &rarr; value
object[attr] &rarr; value
{% endapibody %}

Get a single field from an object. If called on a sequence, gets that field from every
object in the sequence, skipping objects that lack it.

__Example:__ What was Iron Man's first appearance in a comic?

```py
r.table('marvel').get('IronMan')['firstAppearance'].run(conn)
```


## [has_fields](has_fields/) ##

{% apibody %}
sequence.has_fields([selector1, selector2...]) &rarr; stream
array.has_fields([selector1, selector2...]) &rarr; array
singleSelection.has_fields([selector1, selector2...]) &rarr; boolean
object.has_fields([selector1, selector2...]) &rarr; boolean
{% endapibody %}

Test if an object has all of the specified fields. An object has a field if it has the
specified key and that key maps to a non-null value. For instance, the object
`{'a':1,'b':2,'c': None}` has the fields `a` and `b`.

__Example:__ Which heroes are married?

```py
r.table('marvel').has_fields('spouse').run(conn)
```

[Read more about this command &rarr;](has_fields/)


## [insert_at](insert_at/) ##

{% apibody %}
array.insert_at(index, value) &rarr; array
{% endapibody %}

Insert a value in to an array at a given index. Returns the modified array.

__Example:__ Hulk decides to join the avengers.

```py
r.expr(["Iron Man", "Spider-Man"]).insert_at(1, "Hulk").run(conn)
```


## [splice_at](splice_at/) ##

{% apibody %}
array.splice_at(index, array) &rarr; array
{% endapibody %}

Insert several values in to an array at a given index. Returns the modified array.

__Example:__ Hulk and Thor decide to join the avengers.

```py
r.expr(["Iron Man", "Spider-Man"]).splice_at(1, ["Hulk", "Thor"]).run(conn)
```


## [delete_at](delete_at/) ##

{% apibody %}
array.delete_at(index [,endIndex]) &rarr; array
{% endapibody %}

Remove an element from an array at a given index. Returns the modified array.

__Example:__ Hulk decides to leave the avengers.

```py
r.expr(["Iron Man", "Hulk", "Spider-Man"]).delete_at(1).run(conn)
```

[Read more about this command &rarr;](delete_at/)


## [change_at](change_at/) ##

{% apibody %}
array.change_at(index, value) &rarr; array
{% endapibody %}

Change a value in an array at a given index. Returns the modified array.

__Example:__ Bruce Banner hulks out.

```py
r.expr(["Iron Man", "Bruce", "Spider-Man"]).change_at(1, "Hulk").run(conn)
```

## [keys](keys/) ##

{% apibody %}
singleSelection.keys() &rarr; array
object.keys() &rarr; array
{% endapibody %}

Return an array containing all of the object's keys.

__Example:__ Get all the keys of a row.

```py
r.table('marvel').get('ironman').keys().run(conn)
```

## [object](object/) ##

{% apibody %}
r.object([key, value,]...) &rarr; object
{% endapibody %}

Creates an object from a list of key-value pairs, where the keys must
be strings.  `r.object(A, B, C, D)` is equivalent to
`r.expr([[A, B], [C, D]]).coerce_to('OBJECT')`.

__Example:__ Create a simple object.

```py
> r.object('id', 5, 'data', ['foo', 'bar']).run(conn)
{"data": ["foo", "bar"], "id": 5}
```

{% endapisection %}


{% apisection String manipulation%}
These commands provide string operators.

## [match](match/) ##

{% apibody %}
string.match(regexp) &rarr; None/object
{% endapibody %}

Matches against a regular expression. If there is a match, returns an object with the fields:

- `str`: The matched string
- `start`: The matched string's start
- `end`: The matched string's end
- `groups`: The capture groups defined with parentheses

If no match is found, returns `None`.

__Example:__ Get all users whose name starts with "A".

```py
r.table('users').filter(lambda doc:
    doc['name'].match("^A")
).run(conn)
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
called with `None` as the separator if you want to split on whitespace
while still specifying `max_splits`.)

Mimics the behavior of Python's `string.split` in edge cases, except
for splitting on the empty string, which instead produces an array of
single-character strings.

__Example:__ Split on whitespace.

```py
> r.expr("foo  bar bax").split().run(conn)
["foo", "bar", "bax"]
```

[Read more about this command &rarr;](split/)

## [upcase](upcase/) ##

{% apibody %}
string.upcase() &rarr; string
{% endapibody %}

Upcases a string.

__Example:__

```py
> r.expr("Sentence about LaTeX.").upcase().run(conn)
"SENTENCE ABOUT LATEX."
```

## [downcase](downcase/) ##

{% apibody %}
string.downcase() &rarr; string
{% endapibody %}

Downcases a string.

__Example:__

```py
> r.expr("Sentence about LaTeX.").downcase().run(conn)
"sentence about latex."
```

{% endapisection %}


{% apisection Math and logic%}

## [+](add/) ##

{% apibody %}
number + number &rarr; number
string + string &rarr; string
array + array &rarr; array
time + number &rarr; time
{% endapibody %}

Sum two numbers, concatenate two strings, or concatenate 2 arrays.

__Example:__ It's as easy as 2 + 2 = 4.

```py
(r.expr(2) + 2).run(conn)
```

[Read more about this command &rarr;](add/)


## [-](sub/) ##

{% apibody %}
number - number &rarr; number
time - time &rarr; number
time - number &rarr; time
{% endapibody %}

Subtract two numbers.

__Example:__ It's as easy as 2 - 2 = 0.

```py
(r.expr(2) - 2).run(conn)
```

[Read more about this command &rarr;](sub/)


## [*](mul/) ##

{% apibody %}
number * number &rarr; number
array * number &rarr; array
{% endapibody %}

Multiply two numbers, or make a periodic array.

__Example:__ It's as easy as 2 * 2 = 4.

```py
(r.expr(2) * 2).run(conn)
```

[Read more about this command &rarr;](mul/)

## [/](div/) ##

{% apibody %}
number / number &rarr; number
{% endapibody %}

Divide two numbers.

__Example:__ It's as easy as 2 / 2 = 1.

```py
(r.expr(2) / 2).run(conn)
```



## [%](mod/) ##

{% apibody %}
number % number &rarr; number
{% endapibody %}

Find the remainder when dividing two numbers.

__Example:__ It's as easy as 2 % 2 = 0.

```py
(r.expr(2) % 2).run(conn)
```

## [&, and_](and/) ##

{% apibody %}
bool & bool &rarr; bool
r.and_(bool, bool) &rarr; bool
bool.and_(bool) &rarr; bool
{% endapibody %}

# Description #

Compute the logical and of two values.

__Example:__ True and false anded is false?

```py
(r.expr(True) & False).run(conn)
r.expr(True).and_(False).run(conn)
r.and_(True, False).run(conn)
```


## [|, or_](or/) ##

{% apibody %}
bool | bool &rarr; bool
bool.or_(bool) &rarr; bool
r.or_(bool, bool) &rarr; bool
{% endapibody %}

# Description #

Compute the logical or of two values.

__Example:__ True or false ored is true?

```py
(r.expr(True) | False).run(conn)
r.expr(True).or_(False).run(conn)
r.or_(True, False).run(conn)
```


## [==, eq](eq/) ##

{% apibody %}
value == value &rarr; bool
value.eq(value) &rarr; bool
{% endapibody %}

Test if two values are equal.

__Example:__ Does 2 equal 2?

```py
(r.expr(2) == 2).run(conn)
r.expr(2).eq(2).run(conn)
```


## [!=, ne](ne/) ##

{% apibody %}
value != value &rarr; bool
value.ne(value) &rarr; bool
{% endapibody %}

# Description #

Test if two values are not equal.

__Example:__ Does 2 not equal 2?

```py
(r.expr(2) != 2).run(conn)
r.expr(2).ne(2).run(conn)
```


## [>, gt](gt/) ##

{% apibody %}
value > value &rarr; bool
value.gt(value) &rarr; bool
{% endapibody %}

Test if the first value is greater than other.

__Example:__ Is 2 greater than 2?

```py
(r.expr(2) > 2).run(conn)
r.expr(2).gt(2).run(conn)
```

## [>=, ge](ge/) ##

{% apibody %}
value >= value &rarr; bool
value.ge(value) &rarr; bool
{% endapibody %}

# Description #

Test if the first value is greater than or equal to other.

__Example:__ Is 2 greater than or equal to 2?

```py
(r.expr(2) >= 2).run(conn)
r.expr(2).ge(2).run(conn)
```

## [<, lt](lt/) ##

{% apibody %}
value < value &rarr; bool
value.lt(value) &rarr; bool
{% endapibody %}

# Description #

Test if the first value is less than other.

__Example:__ Is 2 less than 2?

```py
(r.expr(2) < 2).run(conn)
r.expr(2).lt(2).run(conn)
```

## [<=, le](le/) ##

{% apibody %}
value <= value &rarr; bool
value.le(value) &rarr; bool
{% endapibody %}

# Description #

Test if the first value is less than or equal to other.

__Example:__ Is 2 less than or equal to 2?

```py
(r.expr(2) <= 2).run(conn)
r.expr(2).le(2).run(conn)
```


## [~, not_](not/) ##

{% apibody %}
~bool &rarr; bool
bool.not_() &rarr; bool
r.not_(bool) &rarr; bool
{% endapibody %}

# Description #
Compute the logical inverse (not).

__Example:__ Not true is false.

```py
r.not_(True).run(conn)
r.expr(True).not_().run(conn)
(~r.expr(True)).run(conn)
```

[Read more about this command &rarr;](not/)


{% endapisection %}


{% apisection Dates and times%}

## [now](now/) ##

{% apibody %}
r.now() &rarr; time
{% endapibody %}

Return a time object representing the current time in UTC. The command now() is computed once when the server receives the query, so multiple instances of r.now() will always return the same time inside a query.

__Example:__ Add a new user with the time at which he subscribed.

```py
r.table("users").insert({
    "name": "John",
    "subscription_date": r.now()
}).run(conn)
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

```py
r.table("user").get("John").update({"birthdate": r.time(1986, 11, 3, 'Z')}).run(conn)
```



## [epoch_time](epoch_time/) ##

{% apibody %}
r.epoch_time(epoch_time) &rarr; time
{% endapibody %}

Create a time object based on seconds since epoch. The first argument is a double and
will be rounded to three decimal places (millisecond-precision).

__Example:__ Update the birthdate of the user "John" to November 3rd, 1986.

```py
r.table("user").get("John").update({"birthdate": r.epoch_time(531360000)}).run(conn)
```


## [iso8601](iso8601/) ##

{% apibody %}
r.iso8601(iso8601Date[, default_timezone='']) &rarr; time
{% endapibody %}

Create a time object based on an iso8601 date-time string (e.g.
'2013-01-01T01:01:01+00:00'). We support all valid ISO 8601 formats except for week
dates. If you pass an ISO 8601 date-time without a time zone, you must specify the time
zone with the optarg `default_timezone`. Read more about the ISO 8601 format on the
Wikipedia page.


__Example:__ Update the time of John's birth.

```py
r.table("user").get("John").update({"birth": r.iso8601('1986-11-03T08:30:00-07:00')}).run(conn)
```


## [in_timezone](in_timezone/) ##

{% apibody %}
time.in_timezone(timezone) &rarr; time
{% endapibody %}

Return a new time object with a different timezone. While the time stays the same, the results returned by methods such as hours() will change since they take the timezone into account. The timezone argument has to be of the ISO 8601 format.

__Example:__ Hour of the day in San Francisco (UTC/GMT -8, without daylight saving time).

```py
r.now().in_timezone('-08:00').hours().run(conn)
```



## [timezone](timezone/) ##

{% apibody %}
time.timezone() &rarr; string
{% endapibody %}

Return the timezone of the time object.

__Example:__ Return all the users in the "-07:00" timezone.

```py
r.table("users").filter(lambda user:
    user["subscriptionDate"].timezone() == "-07:00"
)
```


## [during](during/) ##

{% apibody %}
time.during(start_time, end_time
    [, left_bound="open/closed", right_bound="open/closed"])
        &rarr; bool
{% endapibody %}

Return if a time is between two other times (by default, inclusive for the start, exclusive for the end).

__Example:__ Retrieve all the posts that were posted between December 1st, 2013 (inclusive) and December 10th, 2013 (exclusive).

```py
r.table("posts").filter(
    r.row['date'].during(r.time(2013, 12, 1, "Z"), r.time(2013, 12, 10, "Z"))
).run(conn)
```

[Read more about this command &rarr;](during/)



## [date](date/) ##

{% apibody %}
time.date() &rarr; time
{% endapibody %}

Return a new time object only based on the day, month and year (ie. the same day at 00:00).

__Example:__ Retrieve all the users whose birthday is today

```py
r.table("users").filter(lambda user:
    user["birthdate"].date() == r.now().date()
).run(conn)
```



## [time\_of\_day](time_of_day) ##

{% apibody %}
time.time_of_day() &rarr; number
{% endapibody %}

Return the number of seconds elapsed since the beginning of the day stored in the time object.

__Example:__ Retrieve posts that were submitted before noon.

```py
r.table("posts").filter(
    r.row["date"].time_of_day() <= 12*60*60
).run(conn)
```


## [year](year/) ##

{% apibody %}
time.year() &rarr; number
{% endapibody %}

Return the year of a time object.

__Example:__ Retrieve all the users born in 1986.

```py
r.table("users").filter(lambda user:
    user["birthdate"].year() == 1986
).run(conn)
```


## [month](month/) ##

{% apibody %}
time.month() &rarr; number
{% endapibody %}

Return the month of a time object as a number between 1 and 12. For your convenience, the terms r.january, r.february etc. are defined and map to the appropriate integer.

__Example:__ Retrieve all the users who were born in November.

```py
r.table("users").filter(
    r.row["birthdate"].month() == 11
)
```

[Read more about this command &rarr;](month/)


## [day](day/) ##

{% apibody %}
time.day() &rarr; number
{% endapibody %}

Return the day of a time object as a number between 1 and 31.

__Example:__ Return the users born on the 24th of any month.

```py
r.table("users").filter(
    r.row["birthdate"].day() == 24
)
```



## [day\_of\_week](day_of_week/) ##

{% apibody %}
time.day_of_week() &rarr; number
{% endapibody %}

Return the day of week of a time object as a number between 1 and 7 (following ISO 8601 standard). For your convenience, the terms r.monday, r.tuesday etc. are defined and map to the appropriate integer.

__Example:__ Return today's day of week.

```py
r.now().day_of_week().run(conn)
```

[Read more about this command &rarr;](day_of_week/)


## [day\_of\_year](day_of_year) ##

{% apibody %}
time.day_of_year() &rarr; number
{% endapibody %}

Return the day of the year of a time object as a number between 1 and 366 (following ISO 8601 standard).

__Example:__ Retrieve all the users who were born the first day of a year.

```py
r.table("users").filter(
    r.row["birthdate"].day_of_year() == 1
).run(conn)
```


## [hours](hours/) ##

{% apibody %}
time.hours() &rarr; number
{% endapibody %}

Return the hour in a time object as a number between 0 and 23.

__Example:__ Return all the posts submitted after midnight and before 4am.

```py
r.table("posts").filter(lambda post:
    post["date"].hours() < 4
).run(conn)
```


## [minutes](minutes/) ##

{% apibody %}
time.minutes() &rarr; number
{% endapibody %}

Return the minute in a time object as a number between 0 and 59.

__Example:__ Return all the posts submitted during the first 10 minutes of every hour.

```py
r.table("posts").filter(lambda post:
    post["date"].minutes() < 10
).run(conn)
```



## [seconds](seconds/) ##

{% apibody %}
time.seconds() &rarr; number
{% endapibody %}

Return the seconds in a time object as a number between 0 and 59.999 (double precision).

__Example:__ Return the post submitted during the first 30 seconds of every minute.

```py
r.table("posts").filter(lambda post:
    post["date"].seconds() < 30
).run(conn)
```


## [to_iso8601](to_iso8601/) ##

{% apibody %}
time.to_iso8601() &rarr; number
{% endapibody %}

Convert a time object to its iso 8601 format.

__Example:__ Return the current time in an ISO8601 format.

```py
r.now().to_iso8601()
```


## [to\_epoch\_time](to_epoch_time) ##

{% apibody %}
time.to_epoch_time() &rarr; number
{% endapibody %}

Convert a time object to its epoch time.

__Example:__ Return the current time in an ISO8601 format.

```py
r.now().to_epoch_time()
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

```py
r.do(r.table('marvel').get('IronMan'),
    lambda ironman: ironman['name']).run(conn)
```


## [branch](branch/) ##

{% apibody %}
r.branch(test, true_branch, false_branch) &rarr; any
{% endapibody %}

If the `test` expression returns `False` or `None`, the `false_branch` will be evaluated.
Otherwise, the `true_branch` will be evaluated.

The `branch` command is effectively an `if` renamed due to language constraints.

__Example:__ Return heroes and superheroes.

```
r.table('marvel').map(
    r.branch(
        r.row['victories'] > 100,
        r.row['name'] + ' is a superhero',
        r.row['name'] + ' is a hero'
    )
).run(conn)
```

## [for_each](for_each/) ##

{% apibody %}
sequence.for_each(write_query) &rarr; object
{% endapibody %}

Loop over a sequence, evaluating the given write query for each element.

__Example:__ Now that our heroes have defeated their villains, we can safely remove them from the villain table.

```py
r.table('marvel').for_each(
    lambda hero: r.table('villains').get(hero['villainDefeated']).delete()
).run(conn)
```



## [error](error/) ##

{% apibody %}
r.error(message) &rarr; error
{% endapibody %}

Throw a runtime error. If called with no arguments inside the second argument to `default`, re-throw the current error.

__Example:__ Iron Man can't possibly have lost a battle:

```py
r.table('marvel').get('IronMan').do(
    lambda ironman: r.branch(ironman['victories'] < ironman['battles'],
                             r.error('impossible code path'),
                             ironman)
).run(conn)
```

## [default](default/) ##

{% apibody %}
value.default(default_value) &rarr; any
sequence.default(default_value) &rarr; any
{% endapibody %}

Handle non-existence errors. Tries to evaluate and return its first argument. If an
error related to the absence of a value is thrown in the process, or if its first
argument returns `None`, returns its second argument. (Alternatively, the second argument
may be a function which will be called with either the text of the non-existence error
or `None`.)


__Exmple:__ Suppose we want to retrieve the titles and authors of the table `posts`.
In the case where the author field is missing or `None`, we want to retrieve the string
`Anonymous`.


```py
r.table("posts").map(lambda post:
    {
        "title": post["title"],
        "author": post["author"].default("Anonymous")
    }
).run(conn)
```

[Read more about this command &rarr;](default/)

## [expr](expr/) ##

{% apibody %}
r.expr(value) &rarr; value
{% endapibody %}

Construct a ReQL JSON object from a native object.

__Example:__ Objects wrapped with `expr` can then be manipulated by ReQL API functions.

```py
r.expr({'a':'b'}).merge({'b':[1,2,3]}).run(conn)
```

## [js](js/) ##

{% apibody %}
r.js(jsString) &rarr; value
{% endapibody %}

Create a javascript expression.

__Example:__ Concatenate two strings using Javascript'

```py
r.js("'str1' + 'str2'").run(conn)
```

[Read more about this command &rarr;](js/)

## [coerce_to](coerce_to/) ##

{% apibody %}
sequence.coerce_to(type_name) &rarr; array
value.coerce_to(type_name) &rarr; string
array.coerce_to(type_name) &rarr; object
object.coerce_to(type_name) &rarr; array
{% endapibody %}

Converts a value of one type into another.

You can convert: a selection, sequence, or object into an ARRAY, an array of pairs into an OBJECT, and any DATUM into a STRING.

__Example:__ Convert a table to an array.

```py
r.table('marvel').coerce_to('array').run(conn)
```

[Read more about this command &rarr;](coerce_to/)

## [type_of](type_of) ##

{% apibody %}
any.type_of() &rarr; string
{% endapibody %}

Gets the type of a value.

__Example:__ Get the type of a string.

```py
r.expr("foo").type_of().run(conn)
```

## [info](info/) ##

{% apibody %}
any.info() &rarr; object
{% endapibody %}

Get information about a ReQL value.

__Example:__ Get information about a table such as primary key, or cache size.

```py
r.table('marvel').info().run(conn)
```

## [json](json/) ##

{% apibody %}
r.json(json_string) &rarr; value
{% endapibody %}

Parse a JSON string on the server.

__Example:__ Send an array to the server'

```py
r.json("[1,2,3]").run(conn)
```


{% endapisection %}






