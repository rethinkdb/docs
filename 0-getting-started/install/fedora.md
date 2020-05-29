---
layout: documentation
title: Install RethinkDB on Fedora
title_image: /assets/images/docs/install-platforms/fedora.png
docs_active: install
permalink: docs/install/fedora/
---
{% include docs/install-docs-header.md %}
{% include docs/install-community-platform-warning.md %}

# With binaries #

The <a href="/docs/install/centos/">CentOS RPMs</a> are known to work with
Fedora.

To install the server, add the RethinkDB yum repository to your list of repositories and install:

```bash
sudo cat << EOF > /etc/yum.repos.d/rethinkdb.repo
[rethinkdb]
name=RethinkDB
enabled=1
baseurl=https://download.rethinkdb.com/repository/centos/8/x86_64/
gpgkey=https://download.rethinkdb.com/repository/raw/pubkey.gpg
gpgcheck=1
EOF

sudo yum install rethinkdb
```


# Compile from source #

The following instructions were tested on Fedora 20.

## Get the build dependencies ##

Install the main dependencies:

```bash
sudo yum install gcc-c++ protobuf-devel ncurses-devel jemalloc-devel \
         boost-static wget protobuf-compiler which zlib-devel \
         openssl-devel libcurl-devel make m4
```

## Get the source code ##

Download and extract the source tarball:

```bash
wget https://download.rethinkdb.com/repository/raw/dist/rethinkdb-{{site.version.full}}.tgz
tar xf rethinkdb-{{site.version.full}}.tgz
```

## Build RethinkDB ##

Kick off the build process:

```bash
cd rethinkdb-{{site.version.full}}
./configure --dynamic jemalloc
make
sudo make install
```

{% include docs/install-next-step.md %}
