---
layout: documentation
title: Ten-minute guide with RethinkDB and Ruby
active: docs
docs_active: guide
permalink: docs/guide/ruby/
switcher: true
language: Ruby
---


{% infobox %}
<strong>Before you start:</strong>

* Make sure you've <a href="/install">installed RethinkDB</a> &mdash; it should only take a minute!
* Make also sure you've <a href="/docs/install-drivers/ruby/">installed the Ruby driver</a>.
* Start one <a href="/docs/start-a-cluster/">or more</a> RethinkDB instances.  (Start the first with `rethinkdb` in your favorite shell).
* Read the <a href="/docs/quickstart/">thirty-second quickstart</a>.
{% endinfobox %}

<img src="/assets/images/docs/api_illustrations/10-minute-guide-ruby.png" class="api_command_illustration" />

# Import the driver #

First, start a Ruby shell:

```bash
$ irb
```

Then, import the RethinkDB driver:

```ruby
require 'rethinkdb'
include RethinkDB::Shortcuts
```

You can now access RethinkDB commands through the `r` module.

# Open a connection #

When you first start RethinkDB, the server opens a port for the client
drivers (`28015` by default). Let's open a connection:

```ruby
r.connect(:host=>"localhost", :port=>28015).repl
```

The `repl` command is a convenience method that sets a default connection in your shell so you don't have to pass it to the `run` command to run your queries.

{% infobox info %}
__Note:__ the `repl` command is useful to experiment in the shell, but
you should pass the connection to the `run` command explicitly in
real applications. See [an example
project](/docs/examples/sinatra-pastie/) for more details.
{% endinfobox%}

# Create a new table #

By default, RethinkDB creates a database `test`. Let's create a table
`authors` within this database:

```ruby
r.db("test").table_create("authors").run
```

The result should be:

```ruby
{ "created"=>1 }
```

There are a couple of things you should note about this query:

* First, we select the database `test` with the `db` command.
* Then, we add the `table_create` command to create the actual table.
* Lastly, we call `run` in order to send the query to the server.

All ReQL queries follow this general structure. Now that we've created
a table, let's insert some data!

# Insert data #

Let's insert three new documents into the `authors` table:

```ruby
r.table("authors").insert([
    { "name"=>"William Adama", "tv_show"=>"Battlestar Galactica",
      "posts"=>[
        {"title"=>"Decommissioning speech", "content"=>"The Cylon War is long over..."},
        {"title"=>"We are at war", "content"=>"Moments ago, this ship received..."},
        {"title"=>"The new Earth", "content"=>"The discoveries of the past few days..."}
      ]
    },
    { "name"=>"Laura Roslin", "tv_show"=>"Battlestar Galactica",
      "posts"=>[
        {"title"=>"The oath of office", "content"=>"I, Laura Roslin, ..."},
        {"title"=>"They look like us", "content"=>"The Cylons have the ability..."}
      ]
    },
    { "name"=>"Jean-Luc Picard", "tv_show"=>"Star Trek TNG",
      "posts"=>[
        {"title"=>"Civil rights", "content"=>"There are some words I've known since..."}
      ]
    }
]).run
```

We should get back an object that looks like this:

```ruby
{
    "unchanged"=>0,
    "skipped"=>0,
    "replaced"=>0,
    "inserted"=>3,
    "generated_keys"=>[
        "71879b1b-e81e-48c4-a42c-f41f83d7133e",
        "f0a93ef3-cec0-4364-bde6-f664088b9e77",
        "f601347b-95a1-4ffe-83bd-ed04d4a3cce5"
    ],
    "errors"=>0,
    "deleted"=>0
}
```
The server should return an object with zero errors and three inserted
documents. We didn't specify any primary keys (by default, each table
uses the `id` attribute for primary keys), so RethinkDB generated them
for us. The generated keys are returned via the `generated_keys`
attribute.

There are a couple of things to note about this query:

* Each connection sets a default database to use during its lifetime
  (if you don't specify one in `connect`, the default database is set
  to `test`). This way we can omit the `db('test')` command in our
  query. We won't specify the database explicitly from now on, but if
  you want to prepend your queries with the `db` command, it won't
  hurt.
* The `insert` command accepts a single document or an array of
  documents if you want to batch inserts. We use an array in this
  query instead of running three separate `insert` commands for each
  document.

# Retrieve documents #

Now that we inserted some data, let's see how we can query the
database!

## All documents in a table ##

To retrieve all documents from the table `authors`, we can simply run
the query `r.table('authors')`:

```ruby
cursor = r.table("authors").run
cursor.each{|document| p document}
```

The query returns the three previously inserted documents, along with
the generated `id` values.

Since the table might contain a large number of documents, the
database returns a cursor object. As you iterate through the cursor,
the server will send documents to the client in batches as they are
requested. The cursor is an iterable Ruby object so you can go
through all of the results with a simple `for` loop.

## Filter documents based on a condition ##

Let's try to retrieve the document where the `name` attribute is set
to `William Adama`.  We can use a condition to filter the documents by
chaining a `filter` command to the end of the query:

```ruby
cursor = r.table("authors").filter{|author| author["name"].eq("William Adama") }.run
cursor.each{|document| p document}
```

This query returns a cursor with one document &mdash; the record for
William Adama. The `filter` command evaluates the provided condition
for every row in the table, and returns only the relevant rows. Here's
the new commands we used to construct the condition above:

- `author` refers to the currently visited document.
- `author['name']` refers to the value of the field `name` of the visited document.
- The `eq` command returns `true` if two values are equal (in this case, the field `name` and the string `William Adama`).


Let's use `filter` again to retrieve all authors who have more than
two posts:

```ruby
cursor = r.table("authors").filter{|author| author["posts"].count > 2}.run
cursor.each{|document| p document}
```

In this case, we're using a predicate that returns `true` only if the
length of the array in the field `posts` is greater than two. This
predicate contains two commands we haven't seen before:

- The `count` command returns the size of the array.
- The `>` operator is overloaded by the RethinkDB driver to execute on
  the server. It returns `True` if a value is greater than a certain
  value (in this case, if the number of posts is greater than two).

## Retrieve documents by primary key ##

We can also efficiently retrieve documents by their primary key using
the `get` command. We can use one of the ids generated in the
previous example:

```ruby
r.db('test').table('authors').get('7644aaf2-9928-4231-aa68-4e65e31bf219').run
```

Since primary keys are unique, the `get` command returns a single
document. This way we can retrieve the document directly without
iterating through a cursor.

{% infobox info %}
Learn more about how RethinkDB can efficiently retrieve documents with
[secondary indexes](/docs/secondary-indexes/).
{% endinfobox %}

# Update documents #

Let's update all documents in the `authors` table and add a `type`
field to note that every author so far is fictional:

```ruby
r.table("authors").update({"type"=>"fictional"}).run
```

Since we changed three documents, the result should look like this:

```ruby
{
    "unchanged"=>0,
    "skipped"=>0,
    "replaced"=>3,
    "inserted"=>0,
    "errors"=>0,
    "deleted"=>0
}
```

Note that we first selected every author in the table, and then
chained the `update` command to the end of the query. We could also
update a subset of documents by filtering the table first. Let's
update William Adama's record to note that he has the rank of Admiral:

```ruby
r.table("authors").
    filter{|author| author["name"].eq("William Adama")}.
    update({"rank"=>"Admiral"}).run
```

Since we only updated one document, we get back this object:

```ruby
{
    "unchanged"=>0,
    "skipped"=>0,
    "replaced"=>1,
    "inserted"=>0,
    "errors"=>0,
    "deleted"=>0
}
```

The `update` command allows changing existing fields in the document,
as well as values inside of arrays. Let's suppose Star Trek
archaeologists unearthed a new speech by Jean-Luc Picard that we'd like
to add to his posts:

```ruby
r.table('authors').filter{|author| author["name"].eq("Jean-Luc Picard")}.
    update{|author| {"posts"=>author["posts"].append({
        "title"=>"Shakespeare",
        "content"=>"What a piece of work is man..."})
    }}.run
```

After processing this query, RethinkDB will add an additional post to
Jean-Luc Picard's document.

{% infobox info %}
Browse the [API reference](/api/ruby/) for many more array operations available in RethinkDB.
{% endinfobox %}


# Delete documents #

Suppose we'd like to trim down our database and delete every document
with less than three posts (sorry Laura and Jean-Luc):

```python
r.table("authors").
    filter{ |author| author["posts"].count < 3 }.
    delete.run
```

Since we have two authors with less than two posts, the result
is:

```ruby
{
    "unchanged"=>0,
    "skipped"=>0,
    "replaced"=>0,
    "inserted"=>0,
    "errors"=>0,
    "deleted"=>2
}
```


{% include quickstart-footer.md %} 
