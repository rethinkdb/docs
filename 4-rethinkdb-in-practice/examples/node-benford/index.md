---
layout: example-app 
title: "Benford's law"
github_url: "https://github.com/rethinkdb/rethinkdb-example-nodejs/tree/master/benford"
active: docs
docs_active: examples
permalink: docs/examples/node-benford/
---


# About

This little example illustrates
<a href="http://en.wikipedia.org/wiki/Benford's_law">Benford's law</a> using
Twitter's streaming API. Benford's law refers to the frequency distribution of digits
in many (but not all) real-life sources of data. In this distribution, the number 1
occurs as the leading digit about 30% of the time, while larger numbers occur in that
position less frequently: 9 as the first digit less than 5% of the time[[Wikiepdia](http://en.wikipedia.org/wiki/Benford's_law)].

This example is composed of two parts.

- The first one is the crawler. A Node.js script listens to Twitter's sample stream, and extracts
the first significant digits of every numbers. It then increments the number of occurrences of the
significant digits found.
- The second part is a web server that listens to the changes on the database and broadcasts them to
the browsers. The browsers will then update the interface to display the last results.


# Implementation

## Crawler

The file `crawler.js` connects to Twitter, and listen to the sample stream. For every tweets, it
will extract the first significant digits of any number, and update the number of occurrence


First, import some modules and define some variables.

```js
var config = require(__dirname+"/config.js");

var Twit = require('twit');
var T = new Twit({
    consumer_key: config.twitter.consumer_key,
    consumer_secret: config.twitter.consumer_secret,
    access_token: config.twitter.access_token,
    access_token_secret: config.twitter.access_token_secret
});

var r = require('rethinkdb');

// Define some global variables
var data;
var connection;
```


Open a connection to RethinkDB, initialize the database (create a database, table and the documents)
and call `listen` to start listening at the Twitter stream.

If the table was already created, the operations will silently fail and `listen` will
eventually be called.

```js
r.connect({
    host: config.rethinkdb.host,
    port: config.rethinkdb.port,
    db: config.rethinkdb.db
}, function(err, conn) {
    if (err) {
        throw new Error("Could not open a connection to rethinkdb\n"+err.message)
    }

    connection = conn;

    // Initialize the table with first the database
    r.dbCreate(config.rethinkdb.db).run(connection, function(err, result) {
        // If the database already exists, we'll get an error here, but we'll just keep going
        r.db(config.rethinkdb.db).tableCreate('benford').run(connection, function(err, result) {
            // If the table already exists, we'll get an error here, but we'll just keep going

            var seeds = [];
            for(var i=1; i<10; i++) {
                // Note: We use the digit value as the primary key and save it as a string
                seeds.push({id: ""+i, value: 0});
            }
            r.db(config.rethinkdb.db).table('benford').insert(seeds).run(connection, function(err, result) {
                // If the database was already initialized, the inserts will not be executed since RethinkDB
                // does not allow redundant primary keys (`id`)

                // Start listening to Twitter's stream
                listen();
            });
        });
    });
});
```


Listen to the stream of random statuses, extract the first significant digit of each number, and
increment its occurrence in the database.

```js
function listen() {
    // Open the stream
    var stream = T.stream('statuses/sample');

    stream.on('tweet', function (tweet) {
        var words = tweet.text.split(/\s+/); // Split a tweet on white space

        var foundSignificantDigits = false; // Whether we found a snificant digit to save
        var data = {}; // Keep track of the data to send to the database

        for(var i=0; i<words.length; i++) {
            if (words[i].match(/^-?\d*[\.,]?\d*$/) !== null) { // Check if a word is a "usual" number - x/x.y/x,y/-x/etc.
                var digit = null;
                for(var position in words[i]) { // Look for the first significant digit
                    if (words[i][position].match(/[1-9]/) !== null) {
                        digit = words[i][position];
                        break;
                    }
                }
                if (digit != null) { // Check if we found a significant digit (we may not find one for "0" for example.
                    foundSignificantDigits = true; // We found at least one number

                    data[digit] = data[digit] || 0; // If data[digit] is undefined, set it to 0
                    data[digit]++
                }
            }
        }
        if (foundSignificantDigits === true) {
            for(var digit in data) {
                // Update the document by incrementing its value with data[digit]
                // Not that we fire the write without expecting an answer
                r.db(config.rethinkdb.db).table('benford').get(digit)
                    .update({value: r.row("value").add(data[digit])}).run(connection, {noreply: true})
            }
        }
    });
}
```

## HTTP server

Import some modules.

```js
var config = require(__dirname+"/config.js");

var express = require('express');
var r = require('rethinkdb');

var cluster = require('cluster');
var numCPUs = require('os').cpus().length;

var sticky = require('sticky-session');
```

We are going to use the Node.js cluster API to use all the cores available on the server. We use
[socket.io](http://socket.io) to push data from the server to the browers. This require the requests
from one browser to be handle by the same HTTP server. We use for that `sticky-session` that will
hash the IP of a request and use it to forward it to a HTTP server.

```js
// We do not use directly the `cluster` modules because socket.io won't work
// sticky will use the request's ip such that a client always connect to the same server
sticky(function() {
    var app = express();

    // Serve static content
    app.use(express.static(__dirname + '/public'));

    var server = require('http').createServer(app);
    var io = require('socket.io')(server);

    // Initialize the values for each significant digits with what we have in the database
    var alldata = {};
    r.connect({}, function(err, connection) {
        r.db('examples').table('benford').run(connection, function(err, cursor) {
            if (err) throw new Error("Could not retrieve the data from the server. Is `crawler.js` running?")

            cursor.each(function(err, row) {
                alldata[row.id] = row.value;
            });
        });
    });

    // Everytime a client connect to the server, we send him all the data we have
    io.on('connection', function(socket) {
        socket.emit('all', alldata);
    })

    // Create a connection to RethinkDB
    r.connect({
        host: config.rethinkdb.host,
        port: config.rethinkdb.port,
        db: config.rethinkdb.db
    }, function(err, connection) {

        // Open a feed to listen to the changes on the database
        r.db('examples').table('benford').changes().run(connection, function(err, feed) {

            feed.on('data', function(change) {
                // Broadcast the change to all the sockets
                io.sockets.emit('update', change);

                // Update alldata with the new value
                alldata[change.new_val.id] = change.new_val.value; 
            });
        });
    });

    return server;
}).listen(config.http.port, function() {
    console.log('Server listenening at port %d', config.http.port)
});
```

One really nice thing about having change feeds on the database is that you do not have
to synchronize the data between your HTTP server, which while doable is not really
pleasant to do.

## Browser

The code in the browser is pretty simple.
We listen on the two events `all` and `update`, and update the interface with the
new received data.

```js
$(function() {
    var socket = io();
    var total = 0;

    socket.on('all', function(alldata) {
        // alldata = {<digit>: {old_val: {id: ..., value: ...}, new_val: {id: ..., value: ...}} }
        for(var digit in alldata) {
            total += alldata[digit];
        }
        for(digit in alldata) {
            $("#occurrences_"+digit).html(alldata[digit]);
            $("#percentage_"+digit).html((alldata[digit]/total*100).toFixed(1)+"%");
        }
    });
    socket.on('update', function(data) {
        $("#occurrences_"+data.new_val.id).html(data.new_val.value);
        total += data.new_val.value - data.old_val.value;
        $("#percentage_"+data.new_val.id).html((data.new_val.value/total*100).toFixed(1)+"%");
    });
});
```

{% infobox info %}
__Any question?:__ Shoot us an email at <a href="mailto:info@rethinkdb.com">info@rethinkdb.com</a>.
{% endinfobox %}

