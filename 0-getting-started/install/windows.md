---
layout: documentation
title: Install RethinkDB on Windows
title_image: /assets/images/docs/install-platforms/windows.png
docs_active: install
permalink: docs/install/windows/
---
{% include docs/install-docs-header.md %}

# Downloading #

{% infobox %}
The Windows port of RethinkDB is now available early for RethinkDB 2.4.3!  This is the first official 2.4.x Windows release.
{% endinfobox %}

_Prerequisites:_ We provide native 64-bit binaries for Windows 7 and above. A 64-bit version of Windows is required.

[Download](https://download.rethinkdb.com/repository/raw/windows/rethinkdb-2.4.3.zip) the ZIP archive and unpack it in a directory of your choice.

{% infobox %}
The Windows port of RethinkDB is a recent addition and hasn't received as much tuning as the Linux and OS X versions yet. Please report any performance issues on [GitHub][gh-issues].

[gh-issues]: https://github.com/rethinkdb/rethinkdb/issues/
{% endinfobox %}


# Running RethinkDB #

The Windows version of RethinkDB, like the Linux/OS X versions, is executed from the command line. You'll need to start the Windows command shell.

* Press `Win` + `X` and click "Command Prompt"; or
* Open the Start Menu, click "Run," and type "cmd" `ENTER`

Use the `cd` command to go to the directory that you unpacked `rethinkdb.exe` in.

    C:\Users\Slava\>cd RethinkDB
    C:\Users\Slava\RethinkDB\>

Then, you can start RethinkDB with its default options.

    C:\Users\Slava\RethinkDB\>rethinkdb.exe

You can also use any of the [command line options][cl] to control configuration (as well as specify a [configuration file][cf]).

[cl]: /docs/cli-options/
[cf]: /docs/config-file/

To start with a specific data directory:

    rethinkdb.exe -d c:\RethinkDB\data\

To specify a server name and another cluster to join:

    rethinkdb.exe -n jarvis -j cluster.example.com

To install RethinkDB as a Windows service, read [Start RethinkDB at system startup][st].

[st]: /docs/start-on-startup/#startup-as-a-windows-service

# Compile from source #

To build RethinkDB under Windows, you'll need to download and extract the archive at <https://download.rethinkdb.com/repository/raw/dist/rethinkdb-{{site.version.full}}.tgz>. Requirements and build directions are in the [`WINDOWS.md`][readme] file.

[readme]: https://github.com/rethinkdb/rethinkdb/blob/master/WINDOWS.md

{% include docs/install-next-step.md %}
