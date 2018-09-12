---
layout: documentation
title: Installing the Go driver
title_image: /assets/images/docs/driver-languages/go.png
docs_active: install-drivers
permalink: docs/install-drivers/go/
---
{% include docs/install-driver-docs-header.md %}

# Installation #

Install the driver with `go get`:

```bash
$ go get gopkg.in/rethinkdb/rethinkdb-go.v5
```

# Usage #

You can use the drivers from Go like this:

```go
package rethinkdb_test

import (
	"fmt"
	"log"

	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func Example() {
	session, err := r.Connect(r.ConnectOpts{
		Address: url, // endpoint without http
	})
	if err != nil {
		log.Fatalln(err)
	}

	res, err := r.Expr("Hello World").Run(session)
	if err != nil {
		log.Fatalln(err)
	}

	var response string
	err = res.One(&response)
	if err != nil {
		log.Fatalln(err)
	}

	fmt.Println(response)

	// Output:
	// Hello World
}
```

To view the full documentation check out [GoDoc](https://godoc.org/github.com/rethinkdb/rethinkdb-go).

# Next steps #

{% infobox %}
Move on to the [ten-minute guide](/docs/guide/javascript/) and learn how to use RethinkDB.
{% endinfobox %}
