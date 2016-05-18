"""SimpleApp.py"""
from pyspark import SparkContext

logFile = "s3://testbucket-radek/hamlet.txt"  # Should be some file on your system
sc = SparkContext("local", "Simple App")

logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'Hamlet' in s).count()
numBs = logData.filter(lambda s: 'King' in s).count()

print("Lines with Hamlet: %i, lines with King: %i" % (numAs, numBs))
