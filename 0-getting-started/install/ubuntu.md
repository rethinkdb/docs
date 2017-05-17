---
layout: documentation
title: Install RethinkDB on Ubuntu
title_image: /assets/images/docs/install-platforms/ubuntu.png
docs_active: install
permalink: docs/install/ubuntu/
---
{% include docs/install-docs-header.md %}

# With binaries #

We provide binaries for both 32-bit and 64-bit Ubuntu Precise and above (>= 12.04).

To install the server, you have to add the [RethinkDB
repository](http://download.rethinkdb.com/apt) to your list of
repositories and install via `apt-get`.
To do this, paste the
following lines into your terminal:

```bash
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

{% include docs/debian-based-install-from-source.md %}

{% include docs/install-next-step.md %}

A step-by-step tutorial on how to install RethinkDB on Ubuntu can be found [here](https://www.rosehosting.com/blog/install-rethinkdb-on-ubuntu-14-04/)
