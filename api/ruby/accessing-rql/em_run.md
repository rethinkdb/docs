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

The `em_run` command returns a `QueryHandle` instance. While the `QueryHandle` will be closed at the end of the block's execution, you can explicitly close it with the `close` method.

__Example:__ return a list of users in an EventMachine loop.

```rb
EventMachine.run {
  r.table('users').order_by(:index => 'username').em_run(conn) { |row|
    # do something with returned row data
    p row
  }
}
```

__Example:__ return a list of users in an EventMachine loop, handling errors.

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

__Example:__ Explicitly close a QueryHandle.

```rb
EventMachine.run {
  printed = 0
  handle = r.table('test').order_by(:index => 'id').em_run(conn) { |row|
    printed += 1
    if printed > 3
      handle.close
    else
      p row
    end
  }
}
```

Instead of passing a block to `em_run`, you may also pass a subclass of `RethinkDB::Handler` that overwrites the event handling methods.

__Example:__ return a list of users and pass it to a handler.

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
  
  # Receive each individual user document
  def on_atom(val)
    p [:user, val]
  end

end

EventMachine.run {
  r.table('users').order_by(:index => 'username').em_run(conn, UserHandler)
}
```

__Example:__ Monitor a changefeed of the top 10 most active users.

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
  
  def on_initial_val(val)
    p [:initial, val]
  end
  
  def on_state(state)
    p [:state, state]
  end
  
  def on_change(old, new)
    p [:change, old, new]
  end  

end

EventMachine.run {
  r.table('users').order_by(:index => r.desc('posts')).limit(10).changes
    .em_run(conn, UserHandler)
}
```

Also see the documentation article on [Asynchronous connections][ac].

[ac]: /docs/async-connections/
