STREAMING_JAR=/home/hadoop/.versions/1.0.3/share/hadoop/contrib/streaming/hadoop-streaming.jar
hadoop jar $STREAMING_JAR -files ./mapper.py,./reducer.py -mapper ./mapper.py -reducer ./reducer.py -input /user/root/words.txt -output /user/root/words-output
