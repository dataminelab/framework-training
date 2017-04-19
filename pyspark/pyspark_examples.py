
## pyspark examples

# Start AWS cluster


# Highly recommended to run with iPython on AWS
sudo pip install ipython[all]

# Ipython - powerful python shell (tab-completion, debugging, and more)
# See for more details: https://ipython.org/

# Run it as:
PYSPARK_DRIVER_PYTHON=ipython pyspark

# It might be necessary to run it with more memory
PYSPARK_DRIVER_PYTHON=ipython pyspark --driver-memory 512m --executor-memory 512m

# Statistics
# Numpy - package for scientific computing with Python
# http://www.numpy.org/
import numpy as np

from pyspark.mllib.stat import Statistics

mat = sc.parallelize(
    [np.array([1.0, 10.0, 100.0]), np.array([2.0, 20.0, 200.0]), np.array([3.0, 30.0, 300.0])]
)  # an RDD of Vectors

# print the data
print(mat.collect()) # this could be a problem on large datasets
print(mat.take(10)) # collect with the limit


# Compute column summary statistics.
summary = Statistics.colStats(mat)
print(summary.mean())  # a dense vector containing the mean value for each column
print(summary.variance())  # column-wise variance
print(summary.numNonzeros())  # number of nonzeros in each column

# Data is available at: https://github.com/apache/spark.git
# Install git and clone example data
sudo yum -y install git
git clone https://github.com/apache/spark.git

# copy data from a local disk to HDFS
## old hadoop fs -put ./spark/data/mllib/ridge-data/lpsa.data /user/hadoop/lpsa.data
hadoop fs -put ./spark/data/mllib/sample_linear_regression_data.txt /user/hadoop/

# Classification - Random Forest

from pyspark.sql import SQLContext
from pyspark.sql.types import *
 
sqlContext = SQLContext(sc)
schema = StructType([ \
    StructField("state", StringType(), True), \
    StructField("account_length", DoubleType(), True), \
    StructField("area_code", StringType(), True), \
    StructField("phone_number", StringType(), True), \
    StructField("intl_plan", StringType(), True), \
    StructField("voice_mail_plan", StringType(), True), \
    StructField("number_vmail_messages", DoubleType(), True), \
    StructField("total_day_minutes", DoubleType(), True), \
    StructField("total_day_calls", DoubleType(), True), \
    StructField("total_day_charge", DoubleType(), True), \
    StructField("total_eve_minutes", DoubleType(), True), \
    StructField("total_eve_calls", DoubleType(), True), \
    StructField("total_eve_charge", DoubleType(), True), \
    StructField("total_night_minutes", DoubleType(), True), \
    StructField("total_night_calls", DoubleType(), True), \
    StructField("total_night_charge", DoubleType(), True), \
    StructField("total_intl_minutes", DoubleType(), True), \
    StructField("total_intl_calls", DoubleType(), True), \
    StructField("total_intl_charge", DoubleType(), True), \
    StructField("number_customer_service_calls", DoubleType(), True), \
    StructField("churned", StringType(), True)])
 
# Data from https://www.sgi.com/tech/mlc/db/churn.all
wget https://www.sgi.com/tech/mlc/db/churn.all
# task: upload to HDFS

churn_data = sqlContext.read \
    .format('com.databricks.spark.csv') \
    .load('file:///Users/radek/spark/churn.all', schema = schema) # or file:///Users/radek/spark/churn.all

from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
 
label_indexer = StringIndexer(inputCol = 'churned', outputCol = 'label')
plan_indexer = StringIndexer(inputCol = 'intl_plan', outputCol = 'intl_plan_indexed')
 
reduced_numeric_cols = ["account_length", "number_vmail_messages", "total_day_calls",
                        "total_day_charge", "total_eve_calls", "total_eve_charge",
                        "total_night_calls", "total_intl_calls", "total_intl_charge"]
 
assembler = VectorAssembler(
    inputCols = ['intl_plan_indexed'] + reduced_numeric_cols,
    outputCol = 'features')

# divide into a training and test subsets
(train, test) = churn_data.randomSplit([0.7, 0.3])

# assemble the pipeline

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
 
classifier = RandomForestClassifier(labelCol = 'label', featuresCol = 'features')
pipeline = Pipeline(stages=[plan_indexer, label_indexer, assembler, classifier])
model = pipeline.fit(train)

# evaluate the model

from pyspark.ml.evaluation import BinaryClassificationEvaluator

predictions = model.transform(test)
evaluator = BinaryClassificationEvaluator()
# 
auroc = evaluator.evaluate(predictions, {evaluator.metricName: "areaUnderROC"})

# See for more: http://blog.cloudera.com/blog/2016/02/how-to-predict-telco-churn-with-apache-spark-mllib/

#########################
# Logistic regression
# See: https://www.kaggle.com/c/titanic
# Data dictionary: https://www.kaggle.com/c/titanic/data

# Goal: Predict survival based on passenger characteristics

import pandas as pd
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/titanic.csv'
titanic = pd.read_csv(url, index_col='PassengerId')
titanic.head()

titanic.rename(columns={'Survived':'label'}, inplace=True)

dfTitanic = sqlContext.createDataFrame(titanic[["label", "Pclass", "Parch"]])

assembler = VectorAssembler(
    inputCols=["Pclass", "Parch"], # ["your", "independent", "variables"],
    outputCol="features")

transformed = assembler.transform(dfTitanic)

trainingData, testData = transformed.randomSplit([0.75, 0.25])

from pyspark.ml.classification import LogisticRegression

# Create initial LogisticRegression model
lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
print lr.explainParams()

# Train model with Training Data
lrModel = lr.fit(trainingData)

# Make predictions on test data using the transform() method.
# LogisticRegression.transform() will only use the 'features' column.
predictions = lrModel.transform(testData)
predictions.printSchema()

from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Print intercept and coefficients
print 'Model Intercept: ', lrModel.intercept
print 'Model weights: ', lrModel.coefficients

# Evaluate model
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
evaluator.evaluate(predictions)

# AUC
evaluator.getMetricName()
evaluator.evaluate(predictions)

# Other metrics
trainingSummary = lrModel.summary
trainingSummary.roc.show()
print("areaUnderROC: " + str(trainingSummary.areaUnderROC))


#### Bonus: Visualisation example

# Simple visualisations
sudo yum install gnuplot
sudo pip install gnuplotlib
sudo pip install pandas

# Python Data Analysis Library
# http://pandas.pydata.org/
import pandas as pd

import gnuplotlib as gp

roc = trainingSummary.roc.toPandas()

>>> gp.plot( (roc.FPR, roc.TPR),
...          _with    = 'lines',
...          terminal = 'dumb 80,40',
...          unset    = 'grid')

# See also: https://github.com/justmarkham/DAT8/blob/master/notebooks/12_titanic_confusion.ipynb
# and: https://github.com/justmarkham/DAT8#class-12-logistic-regression

# TODOs

PCA: https://www.coursera.org/learn/machine-learning/home/week/8

