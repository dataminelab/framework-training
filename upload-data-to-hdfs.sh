hdfs dfs -copyFromLocal ./words.txt /user/root/words.txt
hdfs dfs -mkdir -p /user/training/pig-apache/input/
hdfs dfs -copyFromLocal ./data/access_log_0 /user/root/pig-apache/input/access_log_0
