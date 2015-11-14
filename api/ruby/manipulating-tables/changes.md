---
layout: api-command
language: Ruby
permalink: api/ruby/changes/
command: changes
related_commands:
    table: table/
---

# Command syntax #

{% apibody %}
stream.changes([options) &rarr; stream
singleSelection.changes([options]) &rarr; stream
{% endapibody %}

# Description #

Return a changefeed, an infinite stream of objects representing changes to a query. A changefeed may return changes to a table or an individual document (a "point" changefeed), and document transformation commands such as `filter` or `map` may be used before the `changes` command to affect the output.

There are four optional arguments to `changes`.

* `squash`: Controls how change notifications are batched. Acceptable values are `true`, `false` and a numeric value:
    * `true`: When multiple changes to the same document occur before a batch of notifications is sent, the changes are "squashed" into one change. The client receives a notification that will bring it fully up to date with the server.
    * `false`: All changes will be sent to the client verbatim. This is the default.
    * `n`: A numeric value (floating point). Similar to `true`, but the server will wait `n` seconds to respond in order to squash as many changes together as possible, reducing network traffic. The first batch will always be returned immediately.
* `changefeed_queue_size`: the number of changes the server will buffer between client reads before it starts dropping changes and generates an error (default: 100,000).
* `include_initial`: if `true`, the changefeed stream will begin with the current contents of the table or selection being monitored. These initial results will have `new_val` fields, but no `old_val` fields. The initial results may be intermixed with actual changes, as long as an initial result for the changed document has already been given.
* `include_states`: if `true`, the changefeed stream will include special status documents consisting of the field `state` and a string indicating a change in the feed's state. These documents can occur at any point in the feed between the notification documents described below. If `include_states` is `false` (the default), the status documents will not be sent.

There are currently two states:

* `{:state => "initializing"}` indicates the following documents represent initial values on the feed rather than changes. This will be the first document of a feed that returns initial values.
* `{:state => "ready"}` indicates the following documents represent changes. This will be the first document of a feed that does *not* return initial values; otherwise, it will indicate the initial values have all been sent.

{% infobox %}
Starting with RethinkDB 2.2, state documents will *only* be sent if the `include_states` option is `true`, even on point changefeeds. Initial values will only be sent if `include_initial` is `true`. If `include_states` is `true` and `include_initial` is false, the first document on the feed will be `{:state => 'ready'}`.
{% endinfobox %}

If the table becomes unavailable, the changefeed will be disconnected, and a runtime exception will be thrown by the driver.

Changefeed notifications take the form of a two-field object:

```rb
{
    :old_val => <document before change>,
    :new_val => <document after change>
}
```

When a document is deleted, `new_val` will be `nil`; when a document is inserted, `old_val` will be `nil`.

{% infobox %}
Certain document transformation commands can be chained before changefeeds. For more information, read the [discussion of changefeeds](/docs/changefeeds/ruby/) in the "Query language" documentation.
{% endinfobox %}

The server will buffer up to `changefeed_queue_size` elements (default 100,000). If the buffer limit is hit, early changes will be discarded, and the client will receive an object of the form `{:error => "Changefeed cache over array size limit, skipped X elements."}` where `X` is the number of elements skipped.

Commands that operate on streams (such as [filter](/api/ruby/filter/) or [map](/api/ruby/map/)) can usually be chained after `changes`.  However, since the stream produced by `changes` has no ending, commands that need to consume the entire stream before returning (such as [reduce](/api/ruby/reduce/) or [count](/api/ruby/count/)) cannot.

__Example:__ Subscribe to the changes on a table.

Start monitoring the changefeed in one client:

```rb
r.table('games').changes().run(conn).each{|change| p(change)}
```

As these queries are performed in a second client, the first
client would receive and print the following objects:

```rb
> r.table('games').insert({:id => 1}).run(conn)
{:old_val => nil, :new_val => {:id => 1}}

> r.table('games').get(1).update({:player1 => 'Bob'}).run(conn)
{:old_val => {:id => 1}, :new_val => {:id => 1, :player1 => 'Bob'}}

> r.table('games').get(1).replace({:id => 1, :player1 => 'Bob', :player2 => 'Alice'}).run(conn)
{:old_val => {:id => 1, :player1 => 'Bob'},
 :new_val => {:id => 1, :player1 => 'Bob', :player2 => 'Alice'}}

> r.table('games').get(1).delete().run(conn)
{:old_val => {:id => 1, :player1 => 'Bob', :player2 => 'Alice'}, :new_val => nil}

> r.table_drop('games').run(conn)
ReqlRuntimeError: Changefeed aborted (table unavailable)
```

__Example:__ Return all the changes that increase a player's score.

```rb
r.table('test').changes().filter{ |row|
  row['new_val']['score'] > row['old_val']['score']
}.run(conn)
```

__Example:__ Return all the changes to a specific player's score that increase it past 10.

```rb
r.table('test').get(1).filter { |row|
    row['score'] > 10
}.run(conn)
```

__Example:__ Return all the inserts on a table.

```rb
r.table('test').changes().filter{ |row|
    row['old_val'].eq(nil)
}.run(conn)
```

__Example:__ Return all the changes to game 1, with state notifications and initial values.

```rb
r.table('games').get(1).changes({:include_initial => true, :include_states => true}).run(conn)

# result returned on changefeed
{:state => "initializing"}
{:new_val => {:id => 1, :score => 12, :arena => "Hobbiton Field"}}
{:state => "ready"}
{
	:old_val => {:id => 1, :score => 12, :arena => "Hobbiton Field"},
	:new_val => {:id => 1, :score => 14, :arena => "Hobbiton Field"}
}
{
	:old_val => {:id => 1, :score => 14, :arena => "Hobbiton Field"},
	:new_val => {:id => 1, :score => 17, :arena => "Hobbiton Field", :winner => "Frodo"}
}

```

__Example:__ Return all the changes to the top 10 games. This assumes the presence of a `score` secondary index on the `games` table.

```rb
r.table('games').order_by({:index => r.desc('score')}).limit(10).changes().run(conn)
```
