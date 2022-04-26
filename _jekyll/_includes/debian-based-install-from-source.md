# Compile from source #

## Get the build dependencies ##

Install the dependencies (use `python` on older systems -- Python 2 works):

```bash
sudo apt-get install build-essential protobuf-compiler \
                     python3 python-is-python3 \
                     libprotobuf-dev libcurl4-openssl-dev \
                     libboost-all-dev m4 g++ libssl-dev \
                     libjemalloc-dev
```

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
./configure --allow-fetch --fetch boost
make -j8
sudo make install
```

