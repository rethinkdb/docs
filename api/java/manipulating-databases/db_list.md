---
layout: api-command
language: Java
permalink: api/java/db_list/
command: dbList
related_commands:
    dbCreate: db_create/
    dbDrop: db_drop/
    tableCreate: table_create/
---

# Command syntax #

{% apibody %}
r.dbList() &rarr; DbList
{% endapibody %}

# Description #

List all database names in the cluster. The result is a list of strings.

__Example:__ List all databases.

```java
List<?> dbList = r.dbList().run(connection, ArrayList.class).single();

if (dbList != null) {
    dbList.forEach(System.out::println);
}
```
