hdfs dfs -mkdir /user/training
hdfs dfs -copyFromLocal ./words.txt /user/training/words.txt
hdfs dfs -mkdir -p /user/training/pig-apache/input/
hdfs dfs -copyFromLocal ./data/access_log_0 /user/training/pig-apache/input/access_log_0
