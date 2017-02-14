---
layout: api-command
language: JavaScript
permalink: api/javascript/ee-cursor/
alias:
    - api/javascript/add_listener-cursor/
    - api/javascript/on-cursor/
    - api/javascript/once-cursor/
    - api/javascript/remove_listener-cursor/
    - api/javascript/remove_all_listeners-cursor/
    - api/javascript/listeners-cursor/
    - api/javascript/emit-cursor/
command: "EventEmitter (cursor)"
py: false
rb: false
io:
    -   - cursor 
        - undefined
related_commands:
    next: next/
    each: each/
---

# Command syntax #

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

# Description #

Cursors and feeds implement the same interface as Node's [EventEmitter](http://nodejs.org/api/events.html#events_class_events_eventemitter).

- Two events can be emitted, `data` and `error`.
- Once you start using the `EventEmitter` interface, the other RethinkDB cursor commands like `next`, `toArray`, and `each` will not be available anymore.
- The first time you call an `EventEmitter` method, the cursor or feed will emit data just after the I/O events callbacks and before `setTimeout` and `setInterval` callbacks.


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

<!-- stop -->

This query can be rewritten with the `each` command:

```javascript
r.table("messages").orderBy({index: "date"}).run(conn, function(err, cursor) {
    if (err) {
        // Handle error
        return
    }
    
    cursor.each(function(error, message) {
        if(error) {
            // Handle error
        }
        socket.broadcast.emit("message", message)
    })
});
```


__Example:__ Broadcast all the messages inserted.

```javascript
r.table("messages").changes().filter({old_val: null}).run(conn, function(err, feed) {
    if (err) {
        // Handle error
        return
    }

    feed.on("error", function(error) {
        // Handle error
    })
    feed.on("data", function(newMessage) {
        socket.broadcast.emit("message", newMessage)
    })
});
```
