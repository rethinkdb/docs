---
layout: documentation
title: Installing the Java driver
title_image: /assets/images/docs/driver-languages/java.png
docs_active: install-drivers
permalink: docs/install-drivers/java/
---
{% include docs/install-driver-docs-header.md %}

# Installation #

## Using Maven ##

If you're using Maven, add this to your `pom.xml` file:

```xml
<dependencies>
  <dependency>
    <groupId>com.rethinkdb</groupId>
    <artifactId>rethinkdb-driver</artifactId>
    <version>2.4.4</version>
  </dependency>
</dependencies>
```

## Using Gradle ##

If you're using Gradle, modify your `build.gradle` file:

```groovy
dependencies {
    compile group: 'com.rethinkdb', name: 'rethinkdb-driver', version: '2.4.4'
}
```

## Using Ant ##

If you're using Ant, add the following to your `build.xml`:

```xml
<artifact:dependencies pathId="dependency.classpath">
  <dependency groupId="com.rethinkdb" artifactId="rethinkdb-driver" version="2.4.4" />
</artifact:dependencies>
```

## Using SBT ##

If you're using SBT, add the following to your `build.sbt`:

```scala
libraryDependencies += "com.rethinkdb" % "rethinkdb-driver" % "2.4.4"
```

# Usage #

You can use the drivers from Java like this:

```java
import com.rethinkdb.RethinkDB;
import com.rethinkdb.gen.exc.ReqlError;
import com.rethinkdb.gen.exc.ReqlQueryLogicError;
import com.rethinkdb.model.MapObject;
import com.rethinkdb.net.Connection;


public static final RethinkDB r = RethinkDB.r;

Connection conn = r.connection().hostname("localhost").port(28015).connect();

r.db("test").tableCreate("tv_shows").run(conn);
r.table("tv_shows").insert(r.hashMap("name", "Star Trek TNG")).run(conn);
```

# Next steps #

{% infobox %}
Move on to the [ten-minute guide](/docs/guide/java/) and learn how to use RethinkDB.
{% endinfobox %}