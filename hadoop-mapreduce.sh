export HADOOP_HOME=/usr/lib/hadoop-0.20/contrib/
hadoop jar $HADOOP_HOME/streaming/hadoop-streaming*.jar -file ./mapper.py -mapper ./mapper.py -file ./reducer.py -reducer ./reducer.py -input /user/training/words.txt -output /user/training/words-output
