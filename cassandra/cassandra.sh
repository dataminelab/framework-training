#!/bin/bash

HOST="localhost"
CASSANDRA_PID_DIR=/tmp/

mkdir -p target
cd target
rm -fR ./cassandra

# download cassandra
version="apache-cassandra-2.0.0"
file=${version}-bin.tar.gz
wget -c http://archive.apache.org/dist/cassandra/2.0.0/${file}

# extract
tar xzf ./${file}
mv ./${version} ./cassandra

cd ..

# change configs
sed -e "s/listen_address: localhost/listen_address: $HOST/" \
    -e "s/rpc_address: localhost/rpc_address: $HOST/" \
    -e "s/seeds: "127.0.0.1"/seeds: "$HOST"/" \
        < ./conf/cassandra.yaml > ./target/cassandra/conf/cassandra.yaml

cp ./conf/cassandra-env.sh ./target/cassandra/conf/cassandra-env.sh
cp ./conf/log4j-server.properties ./target/cassandra/conf/log4j-server.properties

sed -e "s@CASSANDRA_PID_DIR@$CASSANDRA_PID_DIR@" \
                ./start.sh > ./target/cassandra/bin/start.sh
chmod +x ./target/cassandra/bin/start.sh

sed -e "s@CASSANDRA_PID_DIR@$CASSANDRA_PID_DIR@" \
        < ./stop.sh > ./target/cassandra/bin/stop.sh
chmod +x ./target/cassandra/bin/stop.sh

