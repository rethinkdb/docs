---
layout: documentation
title: Install RethinkDB on Debian
title_image: /assets/images/docs/install-platforms/debian.png
docs_active: install
permalink: docs/install/debian/
---
{% include docs/install-docs-header.md %}

# With binaries #

We provide binaries for 64-bit Debian versions.

To install the server, you have to add the repository to your list of
repositories and install via `apt-get`. To do this, paste the
following lines into your terminal:

```bash
# Download the public key.
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | \
    sudo gpg --dearmor -o /usr/share/keyrings/rethinkdb-archive-keyrings.gpg

# Add the repository.
echo "deb [signed-by=/usr/share/keyrings/rethinkdb-archive-keyrings.gpg] https://download.rethinkdb.com/repository/debian-$(lsb_release -cs) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list

sudo apt-get update
sudo apt-get install rethinkdb

# Check installation.
rethinkdb --version
```

## Earlier Debian versions ##

As of Debian Trixie, `apt-key` is no longer available.

```bash
export CODENAME=`lsb_release -cs`
echo "deb https://download.rethinkdb.com/repository/debian-$CODENAME $CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

If you followed the above instructions before July 2017 and want to upgrade to a newer version of RethinkDB, you will need to first download the new key (0742918E5C8DA04A):

```bash
$ wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -v -
```

{% include docs/debian-based-install-from-source.md %}

{% include docs/install-next-step.md %}
