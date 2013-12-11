---
layout: documentation
title: Installing RethinkDB client drivers
active: docs
docs_active: install-drivers
permalink: docs/install-drivers/
alias: docs/guides/drivers/
---

<div class="icon-box-category">
    <h1>Official drivers &raquo;</h1>
    <a class="icon-box driver-language" href="javascript/">
        <img src="/assets/images/docs/driver-languages/javascript.png" />
        <p class="name">JavaScript</p>
    </a>
    <a class="icon-box driver-language" href="ruby/">
        <img src="/assets/images/docs/driver-languages/ruby.png" />
        <p class="name">Ruby</p>
    </a>
    <a class="icon-box driver-language" href="python/">
        <img src="/assets/images/docs/driver-languages/python.png" />
        <p class="name">Python</p>
    </a>
</div>

<div class="icon-box-category">
    <h1>Community-supported drivers &raquo;</h1>
    <a class="mini icon-box driver-language" href="https://github.com/unbit/librethinkdb">
        <img src="/assets/images/docs/driver-languages/c.png" />
        <p class="name">C</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/mfenniak/rethinkdb-net">
        <img src="/assets/images/docs/driver-languages/csharp.png" />
        <p class="name">C# / .NET</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/bitemyapp/revise">
        <img src="/assets/images/docs/driver-languages/clojure.png" />
        <p class="name smaller-font">Clojure</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/orthecreedence/cl-rethinkdb">
        <img src="/assets/images/docs/driver-languages/commonlisp.png" />
        <p class="name smaller-font">Common Lisp</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/azukiapp/elixir-rethinkdb">
        <img src="/assets/images/docs/driver-languages/elixir.png" />
        <p class="name">Elixir</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/taybin/lethink">
        <img src="/assets/images/docs/driver-languages/erlang.png" />
        <p class="name">Erlang</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/dancannon/gorethink">
        <img src="/assets/images/docs/driver-languages/go.png" />
        <p class="name">Go</p>
    </a>
    <a class="mini icon-box driver-language" href="http://hackage.haskell.org/package/rethinkdb">
        <img src="/assets/images/docs/driver-languages/haskell.png" />
        <p class="name">Haskell</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/dkhenry/rethinkjava">
        <img src="/assets/images/docs/driver-languages/java.png" />
        <p class="name">Java</span></p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/njlg/perl-rethinkdb">
        <img src="/assets/images/docs/driver-languages/perl.png" />
        <p class="name">Perl</p>
    </a>
    <a class="mini icon-box driver-language" href="http://danielmewes.github.io/php-rql/">
        <img src="/assets/images/docs/driver-languages/php.png" />
        <p class="name">PHP</p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/kclay/rethink-scala">
        <img src="/assets/images/docs/driver-languages/scala.png" />
        <p class="name">Scala <span class="driver-author">by @kclay</span></p>
    </a>
    <a class="mini icon-box driver-language" href="https://github.com/esycat/rql-scala">
        <img src="/assets/images/docs/driver-languages/scala.png" />
        <p class="name">Scala <span class="driver-author">by @esycat</span></p>
    </a>
</div>
{% infobox info %}
    <strong>Haven't installed the server yet?</strong> <a href="/install">Go do that</a> first!
{% endinfobox %}

---

# Contribute a driver #
Help make RethinkDB available on more platforms&mdash; consider [contributing a
driver](https://groups.google.com/forum/?fromgroups=#!forum/rethinkdb-dev) for
another language, or join one of the existing projects.

__Thanks to all our amazing driver contributors!__

- The [rethinkdb-net team](https://github.com/mfenniak/rethinkdb-net/graphs/contributors) (C# / .NET): [https://github.com/mfenniak/rethinkdb-net](https://github.com/mfenniak/rethinkdb-net)
- [@bitemyapp](https://github.com/bitemyapp) and [@cesarbp](https://github.com/cesarbp) (Clojure): [https://github.com/bitemyapp/revise](https://github.com/bitemyapp/revise)
- [@atnnn](https://github.com/atnnn) (Haskell): [https://github.com/atnnn](https://github.com/atnnn/haskell-rethinkdb)
- [@christopherhesse](https://github.com/christopherhesse) (Go): [https://github.com/christopherhesse/rethinkgo](https://github.com/christopherhesse/rethinkgo)
- [@dancannon](https://github.com/dancannon) (Go): [https://github.com/dancannon/gorethink](https://github.com/dancannon/gorethink)
- [@danielmewes](https://github.com/danielmewes) (PHP): [https://github.com/danielmewes/php-rql](https://github.com/danielmewes/php-rql)
- [@dkhenry](https://github.com/dkhenry) (Java): [https://github.com/dkhenry/rethinkjava](https://github.com/dkhenry/rethinkjava)
- [@esycat](https://github.com/esycat) (Scala): [https://github.com/esycat/rql-scala](https://github.com/esycat/rql-scala)
- [@kclay](https://github.com/kclay) (Scala): [https://github.com/kclay/rethink-scala](https://github.com/kclay/rethink-scala)
- [@njlg](https://github.com/njlg) (Perl): [https://github.com/njlg/perl-rethinkdb](https://github.com/njlg/perl-rethinkdb)
- [@orthecreedence](https://github.com/orthecreedence) (Common Lisp): [https://github.com/orthecreedence/cl-rethinkdb](https://github.com/orthecreedence/cl-rethinkdb)
- [@taybin](https://github.com/taybin) (Erlang): [https://github.com/taybin/lethink](https://github.com/taybin/lethink)
- [@nuxlli](https://github.com/nuxlli) (Elixir): [https://github.com/azukiapp/elixir-rethinkdb](https://github.com/azukiapp/elixir-rethinkdb)
- [@unbit](https://github.com/unbit) (C): [https://github.com/unbit/librethinkdb](https://github.com/unbit/librethinkdb)
