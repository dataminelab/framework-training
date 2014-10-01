javac -cp `hadoop classpath`:. -d java/target java/src/org/apache/WordCount.java
mkdir java/target
jar -cvf ./wordcount.jar -C java/target .

