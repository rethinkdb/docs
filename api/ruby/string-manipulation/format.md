---
layout: api-command
language: Ruby
permalink: api/ruby/format/
command: format
io:
    -   - r
        - string
related_commands:
    match: match/
    split: split/
    upcase: upcase/
    downcase: downcase/
---

# Command syntax #

{% apibody %}
r.format(string, object) &rarr; string
{% endapibody %}

# Description #

Format command takes a string as a template and formatting parameters as an object. The parameters in the template string must exist as keys in the object, otherwise, an error raised. The template must be a string literal and cannot be the result of other commands.

__Example:__ Using simple parameters for formatting.

```rb
r.format("{name} loves {candy}.", {
    "name" => "Bob",
    "candy" => "candy floss",
}).run(conn)
```

Result:

```rb
"Bob loves candy floss."
```

__Example:__ Using row for formatting.

```rb
r.table("movies").map({
  "id" => r.row('id'),
  "ratings" => r.http(r.format('http://example.com/movies/?title={title}&release={year}', r.row))
}).run(conn)
```

Result:

```rb
# `ratings` is the result of the HTTP request
[{ id: 1, ratings: { positive: 99, negative: 0 }}]
```
