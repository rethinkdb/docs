---
layout: documentation
title: Building RethinkDB from source
active: docs
docs_active: install
permalink: docs/build/
---

These are generic build instructions. Take a look at the [install page](/docs/install/)
if you are looking for a specific platform.

# Building from source #

## Get the build dependencies ##

There are a number of packages required for the build process. Most
should be available for your operating system's repository. These packages are:

- [GCC (g++)](https://gcc.gnu.org/) or [Clang](http://clang.llvm.org/)
- [Protocol Buffers](https://github.com/google/protobuf/)
- [jemalloc](http://www.canonware.com/jemalloc/)
- [Ncurses](https://www.gnu.org/software/ncurses/)
- [Boost](http://www.boost.org/)
- [Python 2 or 3](https://www.python.org/)
- [libcurl](http://curl.haxx.se/libcurl/)
- [libcrypto](https://www.openssl.org/)

On Ubuntu, you can install the build dependencies with apt-get, [following the instructions here](/docs/install/ubuntu/).

The `./configure` script can install some of these dependencies if they are missing.

## Get the source code ##

Download and extract the archive:

```bash
wget https://download.rethinkdb.com/repository/raw/dist/rethinkdb-{{site.version.full}}.tgz
tar xf rethinkdb-{{site.version.full}}.tgz
```

## Build the server ##

Kick off the build process:

```bash
cd rethinkdb-{{site.version.full}}
./configure --allow-fetch
make
```

# Building from git #

The git version of RethinkDB contains unreleased and unstable
changes. It is meant for developers and contributors.

## Get the source code ##

Clone the development branch:

```bash
git clone https://github.com/rethinkdb/rethinkdb.git
```

Check out the branch or tag you want:

```bash
git checkout v2.4.x
```

## Build RethinkDB ##

Kick off the build process:

```bash
cd rethinkdb
./configure --allow-fetch
make -j8
```

You'll find the `rethinkdb` binary in the `build/release/` subfolder.
