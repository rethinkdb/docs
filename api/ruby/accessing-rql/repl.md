---
layout: api-command
language: Ruby
permalink: api/ruby/repl/
command: repl
js: false
java: false
related_commands:
    connect: connect/
    use: use/
    close: close/
---


# Command syntax #

{% apibody %}
connection.repl
{% endapibody %}

# Description #

Set the default connection to make REPL use easier. Allows calling
`.run` on queries without specifying a connection.

__Note:__ Avoid using `repl` in application code. RethinkDB connection objects are not thread-safe, and calls to `connect` from multiple threads may change the global connection object used by `repl`. Applications should specify connections explicitly.

__Example:__ Set the default connection for the REPL, then call
`run` without specifying the connection.

```rb
r.connect(:db => 'marvel').repl
r.table('heroes').run
```
