export HADOOP_HOME=/home/hadoop
hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming*.jar -file ./mapper.py -mapper ./mapper.py -file ./reducer.py -reducer ./reducer.py -input /user/training/words.txt -output /user/training/words-output
