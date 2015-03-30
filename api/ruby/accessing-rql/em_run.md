---
layout: api-command
language: Ruby
permalink: api/ruby/em_run/
command: em_run
javascript: false
python: false
related_commands:
    run: run/
---

# Command syntax #

{% apibody %}
query.em_run(conn, block) &rarr; cursor
query.em_run(conn, block) &rarr; object
{% endapibody %}

# Description #

Run a query asynchronously on a connection using [EventMachine](http://rubyeventmachine.com). If the query returns a sequence (including a stream), the block will be called once with each element of the sequence. Otherwise, the block will be called just once with the returned value.

__Example: return a list of users in an EventMachine loop.__

```rb
EventMachine.run {
  r.table('users').order_by(:index => 'username').em_run(conn) { |row|
    # do something with returned row data
    p row
  }
}
```

__Example: return a list of users in an EventMachine loop, handling errors.__

```rb
EventMachine.run {
  r.table('users').order_by(:index => 'username').em_run(conn) { |err, row|
    if err:
      # do something with the error
      p [:err, err]
    else:
      # do something with returned row data
      p [:userdata, row]
    end
  }
}
```

Instead of passing a block to `em_run`, you may also pass a subclass of `RethinkDB::Handler` that overwrites the event handling methods.

__Example: return a list of users and pass it to a handler.__

```rb
class UserHandler < RethinkDB::Handler

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
  r.table('users').order_by(:index => 'username').em_run(conn, UserHandler)
}
```

Also see the documentation article on [Asynchronous connections][ac].

[ac]: /docs/async-connections/
