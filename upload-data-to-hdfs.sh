hadoop dfs -copyFromLocal ./words.txt /user/root/words.txt
hadoop dfs -mkdir -p /user/root/pig-apache/input/
hadoop dfs -copyFromLocal ./data/access_log_0 /user/root/pig-apache/input/access_log_0
