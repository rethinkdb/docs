---
layout: api-command
language: Java
permalink: api/java/table_list/
command: tableList
related_commands:
    tableCreate: table_create/
    tableDrop: table_drop/
---

# Command syntax #

{% apibody %}
db.tableList() &rarr; TableList
{% endapibody %}

# Description #

List all table names in a database. The result is a list of strings.

__Example:__ List all tables of the 'test' (`DEFAULT_DB_NAME`) database.

```java
List<?> tableList = r.db(DEFAULT_DB_NAME).tableList().run(connection, ArrayList.class).single();

if (tableList != null) {
    for(Object tableName : tableList) {
        System.out.println(tableName);
    }
}
```
