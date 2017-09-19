# Make sure to setup 
# export SPARK_HOME=/usr/lib/spark
# export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
# export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH

"""SimpleApp.py"""
from pyspark import SparkContext

sc = SparkContext("local", "Simple App")

words = sc.textFile('s3://radek-training/hamlet.txt')

wordcounts = words \
        .map( lambda x: x.replace(',',' ').replace('.',' ').replace('-',' ').lower()) \
        .flatMap(lambda x: x.split()) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda x,y:x+y) \
        .map(lambda x:(x[1],x[0])) \
        .sortByKey(False) 

wordcounts.saveAsTextFile("s3://radek-training/wordcount-hamlet")
