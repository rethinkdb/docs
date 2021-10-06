---
layout: api-command
language: Java
permalink: api/java/get/
command: get
related_commands:
    getAll: get_all/
    between: between/
    filter: filter/
---

# Command syntax #

{% apibody %}
table.get(key) &rarr; singleRowSelection
{% endapibody %}

# Description #

Get a document by primary key.

If no document exists with that primary key, `get` will return `null`.

__Example:__ Find a document by UUID.

```java
r.table("posts").get("a9849eef-7176-4411-935b-79a6e3c56a74").run(conn);
```

__Example:__ Find a document and merge another document with it.

```java
r.table("heroes").get(3).merge(
    r.hashMap("powers", r.array("invisibility", "speed"))
).run(conn);
```

__Example:__ Subscribe to a document's [changefeed](/docs/changefeeds/).

```java
r.table("heroes").get(3).changes().run(conn);
```
