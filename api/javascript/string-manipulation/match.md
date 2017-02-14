---
layout: api-command
language: JavaScript
permalink: api/javascript/match/
command: match
io:
    -   - string
        - object
---

# Command syntax #

{% apibody %}
string.match(regexp) &rarr; null/object
{% endapibody %}

<img src="/assets/images/docs/api_illustrations/match.png" class="api_command_illustration" />

# Description #

Matches against a regular expression. If there is a match, returns an object with the fields:

- `str`: The matched string
- `start`: The matched string's start
- `end`: The matched string's end
- `groups`: The capture groups defined with parentheses

If no match is found, returns `null`.

<!-- break -->

Accepts [RE2 syntax][re2]. You can enable case-insensitive matching by prefixing the regular expression with `(?i)`. See the linked RE2 documentation for more flags.

[re2]: https://github.com/google/re2/wiki/Syntax

The `match` command does not support backreferences.

__Example:__ Get all users whose name starts with "A". Because `null` evaluates to `false` in
[filter](/api/javascript/filter/), you can just use the result of `match` for the predicate.


```javascript
r.table('users').filter(function(doc){
    return doc('name').match("^A")
}).run(conn, callback)
```

__Example:__ Get all users whose name ends with "n".

```javascript
r.table('users').filter(function(doc){
    return doc('name').match("n$")
}).run(conn, callback)
```
__Example:__ Get all users whose name has "li" in it

```javascript
r.table('users').filter(function(doc){
    return doc('name').match("li")
}).run(conn, callback)
```

__Example:__ Get all users whose name is "John" with a case-insensitive search.

```javascript
r.table('users').filter(function(doc){
    return doc('name').match("(?i)^john$")
}).run(conn, callback)
```

__Example:__ Get all users whose name is composed of only characters between "a" and "z".

```javascript
r.table('users').filter(function(doc){
    return doc('name').match("(?i)^[a-z]+$")
}).run(conn, callback)
```

__Example:__ Get all users where the zipcode is a string of 5 digits.

```javascript
r.table('users').filter(function(doc){
    return doc('zipcode').match("\\d{5}")
}).run(conn, callback)
```


__Example:__ Retrieve the domain of a basic email

```javascript
r.expr("name@domain.com").match(".*@(.*)").run(conn, callback)
```

Result:

```javascript
{
    start: 0,
    end: 20,
    str: "name@domain.com",
    groups: [
        {
            end: 17,
            start: 7,
            str: "domain.com"
        }
    ]
}
```

You can then retrieve only the domain with the [\(\)](/api/javascript/get_field) selector and [nth](/api/javascript/nth).

```javascript
r.expr("name@domain.com").match(".*@(.*)")("groups").nth(0)("str").run(conn, callback)
```

Returns `'domain.com'`


__Example:__ Fail to parse out the domain and returns `null`.

```javascript
r.expr("name[at]domain.com").match(".*@(.*)").run(conn, callback)
```
