mkdir java/target
export PATH=$PATH:/usr/lib/jvm/java-7-oracle/bin
javac -cp `hadoop classpath`:. -d java/target java/src/org/apache/WordCount.java
jar -cvf ./wordcount.jar -C java/target .

