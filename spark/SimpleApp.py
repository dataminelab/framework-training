# Make sure to setup 
# export SPARK_HOME=/usr/lib/spark
# export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
# export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH

"""SimpleApp.py"""
from pyspark import SparkContext

logFile = "s3://test-radek123/hamlet.txt"  # Should be some file on your system
sc = SparkContext("local", "Simple App")

logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'Hamlet' in s).count()
numBs = logData.filter(lambda s: 'King' in s).count()

print("Lines with Hamlet: %i, lines with King: %i" % (numAs, numBs))
