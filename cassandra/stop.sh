#!/bin/bash

if [ -f CASSANDRA_PID_DIR/cassandra.pid ];
then
    kill `cat CASSANDRA_PID_DIR/cassandra.pid`
    echo "OK"
fi




