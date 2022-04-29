---
layout: documentation
title: Install RethinkDB on Ubuntu
title_image: /assets/images/docs/install-platforms/ubuntu.png
docs_active: install
permalink: docs/install/ubuntu/
---
{% include docs/install-docs-header.md %}

# With binaries #

We provide binaries for 64-bit Ubuntu Trusty and above (>= 14.04).

To install the server, you have to add the RethinkDB repository to
your list of repositories and install via `apt-get`. To do this, paste
the following lines into your terminal:

## Ubuntu 20.04 and above ##

(This set of instructions might also work on earlier Ubuntus, but that
has not been verified.)

```bash
# Download the public key.
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | \
    sudo gpg --dearmor -o /usr/share/keyrings/rethinkdb-archive-keyrings.gpg

# Add the repository.
echo "deb [signed-by=/usr/share/keyrings/rethinkdb-archive-keyrings.gpg] https://download.rethinkdb.com/repository/ubuntu-$(lsb_release -cs) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list

sudo apt-get update
sudo apt-get install rethinkdb

# Check installation.
rethinkdb --version
```

## Earlier Ubuntu versions ##

As of 22.04, you'll get deprecation warnings if you use `apt-key`.

```bash
source /etc/lsb-release && echo "deb https://download.rethinkdb.com/repository/ubuntu-$DISTRIB_CODENAME $DISTRIB_CODENAME main" | \
    sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb

# Check installation.
rethinkdb --version
```

If you followed the above instructions before July 2017 and want to upgrade to a newer version of RethinkDB, you will need to first download the new key (0742918E5C8DA04A):

```bash
$ wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -v -
```

{% include docs/debian-based-install-from-source.md %}

{% include docs/install-next-step.md %}
