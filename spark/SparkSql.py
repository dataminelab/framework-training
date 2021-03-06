"""SparkSql.py"""
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *

wikiFile = "s3://support.elasticmapreduce/bigdatademo/sample/wiki"
# no need when running from pyspark to create new sc
sc = SparkContext("local", "Simple App")
sqlContext = SQLContext(sc)

wikiRdd = sc.textFile(wikiFile).map(lambda line: line.split(" "))

wikiDf = wikiRdd.toDF(['projectcode','pagename','pageviews','pagesize'])

wikiDf.registerTempTable("wikistats")

pageStats = sqlContext.sql("""
    select pagename, sum(pageviews) c from wikistats group by pagename order by c desc limit 10
""")

pageStats.rdd.saveAsTextFile(
    path="s3://radek-training/page-stats/"
)
