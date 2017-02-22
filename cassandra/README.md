# Installation

sudo yum install jna

sudo vim /etc/yum.repos.d/datastax.repo

```
[datastax]
name = DataStax Repo for Apache Cassandra
baseurl = http://rpm.datastax.com/community
enabled = 1
gpgcheck = 0
```

sudo yum install dsc20

sudo service cassandra start

sudo service cassandra status

cqlsh

See: https://www.liquidweb.com/kb/how-to-install-cassandra-on-centos-6/

# Demo

== CQL ==

./cqlsh

-- "show keyspaces" equivalent
select * from system.schema_keyspaces;

-- replication strategy: http://www.datastax.com/docs/1.0/cluster_architecture/replication
CREATE KEYSPACE twissandra WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

USE twissandra;

-- data types: http://www.datastax.com/docs/1.1/references/cql/cql_data_types
CREATE TABLE users ( username text 
                           PRIMARY KEY, password text);
CREATE TABLE following ( username text, followed text, 
                           PRIMARY KEY(username, followed));

CREATE TABLE followers ( username text, following text, 
                           PRIMARY KEY(username, following));

-- uuid - 100 nanoseconds till 1582 + MAC adress, more granular than unixtimestamp, globally unique
CREATE TABLE tweets ( tweetid uuid 
                          PRIMARY KEY, username text, body text);

-- Materialized view of the tweets - user's timeline
-- Think in terms of your queries - don't be afraid of duplication (space is cheap)
-- Go wide - rows can have 2 billion columns
-- P.S. What you see is not what you get (c)
-- http://johnsanda.blogspot.co.uk/2012/10/why-i-am-ready-to-move-to-cql-for.html
CREATE TABLE timeline (
 username text,
 created_by text,
 tweetid timeuuid,
 body text,
 PRIMARY KEY(username, tweetid)
);

-- Denormalized view of userline (their tweets)
CREATE TABLE userline (
 username text,
 tweetid timeuuid,
 body text,
 PRIMARY KEY(username, tweetid)
);


-- TTL allows to delete old values (eg. older than 24h)
INSERT INTO users (username, password) VALUES ('jsmith', 'changeme') USING TTL 86400;

SELECT password FROM users WHERE username = 'jsmith';


ALTER TABLE users ADD country varchar;
CREATE INDEX country_key ON users (country);

INSERT INTO users (username, password, country) VALUES ('ted', 'changeme', 'UK');
INSERT INTO users (username, password, country) VALUES ('paul', 'changeme', 'US');

SELECT * FROM users WHERE country='UK';

-- Add testing data (notice the denormalisation)
INSERT INTO following (username, followed) VALUES ('jsmith', 'ted');
INSERT INTO following (username, followed) VALUES ('jsmith', 'paul');
INSERT INTO following (username, followed) VALUES ('paul', 'ted');

INSERT INTO followers (username, following) VALUES ('paul', 'jsmith');
INSERT INTO followers (username, following) VALUES ('ted', 'jsmith');
INSERT INTO followers (username, following) VALUES ('ted', 'paul');


-- Given a username, gets the usernames of the people that the user is following.
SELECT followed FROM following WHERE username = 'jsmith';

-- Given a username, gets the usernames of the people following that user
SELECT following FROM followers WHERE username = 'ted';

-- Add some tweets
INSERT INTO tweets (
 tweetid,
 username,
 body
) VALUES (
 60780342-90fe-11e2-8823-0026c650d722,
 'jsmith',
 'victory is mine!'
);

INSERT INTO userline (
 tweetid,
 username,
 body
) VALUES (
 60780342-90fe-11e2-8823-0026c650d722,
 'jsmith',
 'victory is mine!'
);

-- add the same tweet into all followers timelines
INSERT INTO timeline (
 tweetid,
 username,
 created_by,
 body
) VALUES (
 60780342-90fe-11e2-8823-0026c650d722,
 'paul',
 'jsmith',
 'victory is mine!'
);

-- Given a username, get their tweet timeline (tweets from people they follow).
SELECT tweetid, created_by, body FROM timeline
        WHERE username = 'paul' ORDER BY tweetid DESC LIMIT 10;


-- Given a username, get their userline (their tweets)
SELECT tweetid, body FROM userline
        WHERE username = 'jsmith' ORDER BY tweetid DESC LIMIT 20;

