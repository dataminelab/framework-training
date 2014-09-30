hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -files ./mapper.py,./reducer.py -mapper ./mapper.py -reducer ./reducer.py -input /user/training/words.txt -output /user/training/words-output
