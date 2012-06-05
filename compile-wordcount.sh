export HADOOP_HOME=/usr/lib/hadoop-0.20
javac -classpath ${HADOOP_HOME}/hadoop-*-core.jar -d java/target java/src/org/apache/WordCount.java
jar -cvf ./wordcount.jar -C java/target .