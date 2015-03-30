---
layout: documentation
title: Asynchronous connections
docs_active: async-connections
permalink: docs/async-connections/
---

Certain RethinkDB drivers support asynchronous connections by integrating with popular async libraries. This is particularly useful with [changefeeds][cf] and other real-time applications.

[cf]: /docs/changefeeds

Due to its event-driven nature, JavaScript can easily execute RethinkDB queries in an asynchronous fashion. The official RethinkDB drivers currently support integration with EventMachine for Ruby and Tornado for Python.

{% toctag %}

# JavaScript

No special procedures or commands are necessary to execute RethinkDB queries asynchronously in JavaScript. Read about using callbacks and promises with RethinkDB in the documentation for the [run][] command.

[run]: /api/javascript/run/

In addition, RethinkDB's cursors and feeds implement an [EventEmitter interface][ee] compatible with Node's. This allows your application to set up listeners to receive data from queries as the data becomes available.

[ee]: /api/javascript/event_emitter-cursor/

# Ruby and EventMachine

The RethinkDB Ruby driver adds a new ReQL command, [em_run](/api/ruby/em_run), designed to work with [EventMachine](http://rubyeventmachine.com). In addition, it provides a superclass, `RethinkDB::Handler`, with event-specific methods (e.g., `on_open`, `on_close`) that may be overridden by a class your application defines and passes to `em_run`.

## Simple usage

The easiest way to use RethinkDB with EventMachine is simply by passing a block to `em_run`. If RethinkDB returns a sequence (including a stream), the block will be called once with each element of the sequence. Otherwise, the block will be called just once with the returned value.

__Example: iterate over a stream__

```rb
require 'eventmachine'
require 'rethinkdb'
include RethinkDB::Shortcuts

conn = r.connect(host: 'localhost', port: 28015)

EventMachine.run {
  r.table('test').order_by(:index => 'id').em_run(conn) { |row|
    # do something with returned row data
    p row
  }
}
```

## Using RethinkDB::Handler

To gain more precise control, write a class that inherits from `RethinkDB::Handler` and override the event handling methods, then pass an instance of that class to `em_run`.

__Example: Iterate over a stream using a handler__

```rb
require 'eventmachine'
require 'rethinkdb'
include RethinkDB::Shortcuts

conn = r.connect(host: 'localhost', port: 28015)

class Printer < RethinkDB::Handler

  def on_open
    p :open
  end
  
  def on_close
    p :closed
  end
  
  def on_error(err)
    p [:err, err.to_s]
  end
  
  def on_val(val)
    p [:val, val]
  end

end

EventMachine.run {
  r.table('test').order_by(:index => 'id').em_run(conn, Printer)
}

# sample output
:open
[:val, {"id"=>1}]
[:val, {"id"=>2}]
[:val, {"id"=>3}]
:closed
```

# Python and Tornado