---
layout: documentation
title: Install RethinkDB on CentOS
title_image: /assets/images/docs/install-platforms/centos.png
docs_active: install
permalink: docs/install/centos/
---
{% include docs/install-docs-header.md %}

# With binaries #

We provide binaries for 64-bit CentOS 7, 64-bit AlmaLinux 8, and 64-bit RockyLinux 8.

To install the server, first add the RethinkDB yum repository for [CentOS](https://download.rethinkdb.com/repository/centos), [AlmaLinux](https://download.rethinkdb.com/repository/alma), or [RockyLinux](https://download.rethinkdb.com/repository/rocky), to your list of repositories.

## For AlmaLinux 8

```bash
sudo cat << EOF > /etc/yum.repos.d/rethinkdb.repo
[rethinkdb]
name=RethinkDB
enabled=1
baseurl=https://download.rethinkdb.com/repository/alma/8/x86_64/
gpgkey=https://download.rethinkdb.com/repository/raw/pubkey.gpg
gpgcheck=1
EOF

sudo yum install rethinkdb
```

## For RockyLinux 8

```bash
sudo cat << EOF > /etc/yum.repos.d/rethinkdb.repo
[rethinkdb]
name=RethinkDB
enabled=1
baseurl=https://download.rethinkdb.com/repository/rocky/8/x86_64/
gpgkey=https://download.rethinkdb.com/repository/raw/pubkey.gpg
gpgcheck=1
EOF

sudo yum install rethinkdb
```

## For CentOS 7

```bash
sudo cat << EOF > /etc/yum.repos.d/rethinkdb.repo
[rethinkdb]
name=RethinkDB
enabled=1
baseurl=https://download.rethinkdb.com/repository/centos/7/x86_64/
gpgkey=https://download.rethinkdb.com/repository/raw/pubkey.gpg
gpgcheck=1
EOF

sudo yum install rethinkdb
```

## For CentOS 6

To get a 2.4.2 or later package, please complain on the [RethinkDB issue
tracker](https://github.com/rethinkdb/rethinkdb/issues).

```bash
sudo cat << EOF > /etc/yum.repos.d/rethinkdb.repo
[rethinkdb]
name=RethinkDB
enabled=1
baseurl=https://download.rethinkdb.com/repository/centos/6/x86_64/
gpgkey=https://download.rethinkdb.com/repository/raw/pubkey.gpg
gpgcheck=1
EOF

sudo yum install rethinkdb
```

# Compile from source on CentOS 7 #

## Get the build dependencies ##

Install the main dependencies:

```
sudo yum install openssl-devel libcurl-devel wget tar m4 git-core \
                 gcc-c++ which make zlib-devel \
                 protobuf-devel bzip2 patch
```

### Install optional build dependencies ###

Additional build dependencies are available in the EPEL
repository.

```bash
sudo yum install epel-release
sudo yum install protobuf-devel protobuf-static jemalloc-devel
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
./configure --allow-fetch
make
sudo make install
```

# Compile from source on CentOS 6 #

These instructions have been tested on CentOS 6.5.

**These instructions have not been tested for RethinkDB 2.4.2 or later.**

## Get the build dependencies ##

The version of GCC included with CentOS 6 is too old to compile RethinkDB. A newer version can be installed using devtoolset:

```bash
rpm --import http://ftp.scientificlinux.org/linux/scientific/5x/x86_64/RPM-GPG-KEYs/RPM-GPG-KEY-cern
sudo wget -O /etc/yum.repos.d/slc6-devtoolset.repo http://linuxsoft.cern.ch/cern/devtoolset/slc6-devtoolset.repo
```

Install the main dependencies:

```bash
sudo yum install devtoolset-2 ncurses-devel boost-static openssl-devel \
                 libcurl-devel wget tar which m4
```

### Install optional build dependencies ###

CentOS provides neither a protobuf-devel package nor a jemalloc-devel
package. Installing these dependencies from the EPEL repositories will
allow RethinkDB to build more quickly:

```bash
sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo yum install protobuf-devel jemalloc-devel
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
scl enable devtoolset-2 -- ./configure --dynamic jemalloc --allow-fetch
scl enable devtoolset-2 -- make
sudo make install
```

{% include docs/install-next-step.md %}
