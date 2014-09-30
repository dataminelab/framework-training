javac -cp `hadoop classpath`:. -d java/target java/src/org/apache/WordCount.java
jar -cvf ./wordcount.jar -C java/target .

