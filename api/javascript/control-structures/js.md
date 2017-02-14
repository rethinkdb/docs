---
layout: api-command
language: JavaScript
permalink: api/javascript/js/
command: js
io:
    -   - r
        - value
---

# Command syntax #

{% apibody %}
r.js(jsString[, {timeout: <number>}]) &rarr; value
{% endapibody %}

# Description #

Create a javascript expression.

`timeout` is the number of seconds before `r.js` times out. The default value is 5 seconds.

{% infobox %}
Whenever possible, you should use native ReQL commands rather than `r.js` for better performance.
{% endinfobox %}

__Example:__ Concatenate two strings using JavaScript.

```javascript
r.js("'str1' + 'str2'").run(conn, callback)
```

__Example:__ Select all documents where the 'magazines' field is greater than 5 by running JavaScript on the server.

```javascript
r.table('marvel').filter(
    r.js('(function (row) { return row.magazines.length > 5; })')
).run(conn, callback)
```


__Example:__ You may also specify a timeout in seconds (defaults to 5).

```javascript
r.js('while(true) {}', {timeout:1.3}).run(conn, callback)
```

