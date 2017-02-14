---
layout: api-command
language: JavaScript
permalink: api/javascript/table_create/
command: tableCreate
io:
    -   - db
        - table
related_commands:
    tableList: table_list/
    tableDrop: table_drop/
---

# Command syntax #

{% apibody %}
db.tableCreate(tableName[, options]) &rarr; object
r.tableCreate(tableName[, options]) &rarr; object
{% endapibody %}

# Description #

<img src="/assets/images/docs/api_illustrations/table_create_javascript.png" class="api_command_illustration" />

Create a table. A RethinkDB table is a collection of JSON documents.

If successful, the command returns an object with two fields:

* `tables_created`: always `1`.
* `config_changes`: a list containing one two-field object, `old_val` and `new_val`:
    * `old_val`: always `null`.
    * `new_val`: the table's new [config](/api/javascript/config) value.

If a table with the same name already exists, the command throws `ReqlOpFailedError`.

{% infobox %}
__Note:__ Only alphanumeric characters and underscores are valid for the table name.

Invoking `tableCreate` without specifying a database using [db](/api/javascript/db/) creates a table in the database specified in [connect](/api/javascript/connect/), or `test` if no database was specified.
{% endinfobox %}

When creating a table you can specify the following options:

* `primaryKey`: the name of the primary key. The default primary key is `id`.
* `durability`: if set to `soft`, writes will be acknowledged by the server immediately and flushed to disk in the background. The default is `hard`: acknowledgment of writes happens after data has been written to disk.
* `shards`: the number of shards, an integer from 1-64. Defaults to `1`.
* `replicas`: either an integer or a mapping object. Defaults to `1`.
    * If `replicas` is an integer, it specifies the number of replicas per shard. Specifying more replicas than there are servers will return an error.
    * If `replicas` is an object, it specifies key-value pairs of server tags and the number of replicas to assign to those servers: `{tag1: 2, tag2: 4, tag3: 2, ...}`.
* `primaryReplicaTag`: the primary server specified by its server tag. Required if `replicas` is an object; the tag must be in the object. This must *not* be specified if `replicas` is an integer.

The [data type](/docs/data-types/) of a primary key is usually a string (like a UUID) or a number, but it can also be a time, binary object, boolean or an array. Data types can be mixed in the primary key field, but all values must be unique. Using an array as a primary key causes the primary key to behave like a compound index; read the documentation on [compound secondary indexes][ci] for more information, as it applies to primary keys as well. (Note that the primary index still only covers a single field, while compound secondary indexes can cover multiple fields in a single index.) Primary keys cannot be objects.

[ci]: /docs/secondary-indexes/javascript/#compound-indexes

Tables will be available for writing when the command returns.

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

__Example:__ Create a table named 'dc_universe' using the field 'name' as primary key.

```javascript
r.db('test').tableCreate('dc_universe', {primaryKey: 'name'}).run(conn, callback);
```

__Example:__ Create a table set up for two shards and three replicas per shard. This requires three available servers.

```javascript
r.db('test').tableCreate('dc_universe', {shards: 2, replicas: 3}).run(conn, callback);
```

Read [Sharding and replication](/docs/sharding-and-replication/) for a complete discussion of the subject, including advanced topics.
