---
layout: documentation
title: Install RethinkDB on Arch Linux
title_image: /assets/images/docs/install-platforms/arch.png
docs_active: install
permalink: docs/install/arch/
---
{% include docs/install-docs-header.md %}
{% include docs/install-community-platform-warning.md %}

# Install binary packages #

RethinkDB is in the `community` repository. To install the server, run:

```bash
# pacman -S rethinkdb
```

See [the ArchWiki article on RethinkDB][awr] for more information.

[awr]: https://wiki.archlinux.org/index.php/RethinkDB

# Install with the Arch Build System #

RethinkDB can be compiled automatically by the Arch Build System, the ports-like system for building and packaging software from source code in Arch Linux. Note that ABS may lag slightly behind the Arch binary repositories.

{% infobox %}

According to the `PKGBUILD` some tests may be "flaky" on Btrfs. If you use Btrfs and you are unable to build RethinkDB due to failed tests, you should not edit the `PKGBUILD` to skip the test suite; this might expose you to security problems in production. We suggest using binary packages, or editing the specific failing test.

{% endinfobox %}

## `yaourt` shortcut ##

If you have `yaourt` installed, simply run:

```bash
$ yaourt -Sb rethinkdb
```

This will automatically download the `PKGBUILD` script provided by ABS, download and extract the RethinkDB source, compile and test RethinkDB, create a `pacman`-compatible package, and install the package on the local system. Full customization is possible by editing the `PKGBUILD` when prompted.

## Semi-manual build ##

Ensure you have the `abs` package installed, `/etc/abs.conf` configured for the `community` repository (see [the ArchWiki article on ABS][abs]), and `/etc/makepkg.conf` configured to your liking (see [the ArchWiki article on makepkg][makepkg]).

[abs]: https://wiki.archlinux.org/index.php/Arch_Build_System#How_to_use_ABS
[makepkg]: https://wiki.archlinux.org/index.php/Makepkg

Copy the `PKGBUILD` and related files to a working directory:

```
$ sudo abs community/rethinkdb
$ cp -r /var/abs/community/rethinkdb/ ~
```

Edit `PKGBUILD` to customize the build at this point.

Install the dependencies, build and install the package (the `-s` flag causes `makepkg` to attempt to
install explicit build dependencies):

```
# pacman -S base-devel
$ cd ~/rethinkdb
$ makepkg -s
# pacman -U rethinkdb-1.15.1-1-x86_64.pkg.tar.xz
```


# Build from official source #

## Install build dependencies  ##

You will need to install the `base-devel` group and several additional build dependencies:

```
# pacman -S gcc protobuf git python3 make
```

## Get the source code ##

Download and extract the archive:

```bash
$ wget https://download.rethinkdb.com/repository/raw/dist/rethinkdb-{{site.version.full}}.tgz
$ tar xf rethinkdb-{{site.version.full}}.tgz
```

## Build RethinkDB ##

RethinkDB's `configure` script assumes the `python` executable exists
on the `PATH`.  It may be a symlink to `python3` or `python2`.
(Python 3 has been tested.)  For example,


```
$ export PATH="$PATH":~/bin
$ ln -s /usr/bin/python3 ~/bin/python
```

To run the build:

```bash
$ cd ~/rethinkdb-{{site.version.full}}
$ ./configure --dynamic jemalloc
$ make
```

Once successfully built, the `rethinkdb` binary may be found in the `build/release/` subdirectory.

To install RethinkDB globally:

```
$ cd ~/rethinkdb
# make install
```

{% include docs/install-next-step.md %}
