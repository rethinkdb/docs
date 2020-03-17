---
layout: documentation
title: Connections from mobile devices
docs_active: mobile-connections
permalink: docs/mobile-connections/
---

Although connecting to a RethinkDB through mobile devices (currently, it can be done on Android SDK 26 or greater with the Java driver, for example), it doesn't mean that you should do it.

Whether you database is an Oracle SQL Server or RethinkDB, connecting to your database directly from a mobile device is a bad idea and should be discouraged. In general, there's a number of issues doing it:
* **Database security** --- Connecting directly though a database means your user has direct access over the database. With a decompiler, manifest extractor, or network analysis tools, you can get the database's IP address, user, password, and it to get access to the server and exploit it. And if the permissions are not set-up or badly configured, they can wipe your database.
* **Reliability** --- A mobile connection might be made through GPRS, which can lead to subtle disconnections and data losses, and lots of undefined behaviour and inconsistent data states.
* **Speed and caching** --- If your app frequently queries your server, with large responses, it'll make RethinkDB need to process a lot of data, sometimes not on RAM, continuously. With a simple webserver, you can throttle querying and cache results.
* **Compatibility and Cross-platform** --- Fine, you may be able to query stuff in Android with the Java driver, but you may not in other platform (say, Apple's iOS). Once again, web queries are supported by almost everything, and a simple webserver is all you need. Even Android-only apps benefit using a webserver instead of a direct connection into RethinkDB, by lowering the minimum SDK API from version 26 all the way down to version 9.

There may be cases where you may trust your users (a mobile Admin tool for RethinkDB, say) and have a driver for it, and directly connect to your server. But in most cases, a webserver is faster, more reliable and way safer.

{% infobox %}
**Important!** In case you found vulnerability or security issue in one of the drivers or the database, please contact us via e-mail at [security@rethinkdb.com](mailto:security@rethinkdb.com). Please do **not** use this channel for support.
{% endinfobox %}

