# Linear regression - simple example from the official Spark repository 
# just to get familiar with the API

from pyspark.ml.regression import LinearRegression

# Load training data
data = spark.read.format("libsvm")\
    .load("sample_linear_regression_data.txt")
# or read it from a local disk (if working with a local Spark)
data = spark.read.format("libsvm")\
    .load("file:///Users/radek/src/github/spark/data/mllib/sample_linear_regression_data.txt")

# split into training and test data
(train, test) = data.randomSplit([0.7, 0.3])

lr = LinearRegression(maxIter=100, regParam=0.3, elasticNetParam=0.8)


# Fit the model
lrModel = lr.fit(train)

print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
# objective function (scaled loss + regularization) at each iteration
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
# Used to help if LR systematically over and under-predicts the data (bias)
trainingSummary.residuals.show()
# Root Mean Squared Error (RMSE) on test data
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
# R-squared = Explained variation / Total variation (between 0-100%)
# R-squared cannot determine whether the coefficient estimates and 
# predictions are biased, which is why you must assess the residual plots.
print("r2: %f" % trainingSummary.r2)


## NYC taxi data

wget https://github.com/Azure/Azure-MachineLearning-DataScience/blob/700f1f0d5dbb47eca9b6e7d4dbe11b91898febb3/Misc/KDDCup2016/Data/NYCTaxi/JoinedTaxiTripFare.Point1Pct.Test.tsv?raw=true -O taxi.tsv

# See for details:
# https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-spark-overview#the-nyc-2013-taxi-data

# pyspark.ml.regression
import numpy as np
from pyspark.ml.regression import LinearRegression
#from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.linalg import Vectors

# LOAD PYSPARK LIBRARIES
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


# IMPORT FILE FROM PUBLIC BLOB
taxi_train_file = sc.textFile("file:///Users/radek/spark/taxi.tsv")

# GET SCHEMA OF THE FILE FROM HEADER
schema_string = taxi_train_file.first()
fields = [StructField(field_name, StringType(), True) for field_name in schema_string.split('\t')]
fields[7].dataType = IntegerType() #Pickup hour
fields[8].dataType = IntegerType() # Pickup week
fields[9].dataType = IntegerType() # Weekday
fields[10].dataType = IntegerType() # Passenger count
fields[11].dataType = FloatType() # Trip time in secs
fields[12].dataType = FloatType() # Trip distance
fields[19].dataType = FloatType() # Fare amount
fields[20].dataType = FloatType() # Surcharge
fields[21].dataType = FloatType() # Mta_tax
fields[22].dataType = FloatType() # Tip amount
fields[23].dataType = FloatType() # Tolls amount
fields[24].dataType = FloatType() # Total amount
fields[25].dataType = IntegerType() # Tipped or not
fields[26].dataType = IntegerType() # Tip class
taxi_schema = StructType(fields)

# PARSE FIELDS AND CONVERT DATA TYPE FOR SOME FIELDS
taxi_header = taxi_train_file.filter(lambda l: "medallion" in l)
taxi_temp = taxi_train_file.subtract(taxi_header).map(lambda k: k.split("\t"))\
        .map(lambda p: (p[0],p[1],p[2],p[3],p[4],p[5],p[6],int(p[7]),int(p[8]),int(p[9]),int(p[10]),
                        float(p[11]),float(p[12]),p[13],p[14],p[15],p[16],p[17],p[18],float(p[19]),
                        float(p[20]),float(p[21]),float(p[22]),float(p[23]),float(p[24]),int(p[25]),int(p[26])))


# CREATE DATA FRAME
taxi_train_df = sqlContext.createDataFrame(taxi_temp, taxi_schema)

# CREATE A CLEANED DATA-FRAME BY DROPPING SOME UN-NECESSARY COLUMNS & FILTERING FOR UNDESIRED VALUES OR OUTLIERS
taxi_df_train_cleaned = taxi_train_df.drop('medallion').drop('hack_license').drop('store_and_fwd_flag').drop('pickup_datetime')\
    .drop('dropoff_datetime').drop('pickup_longitude').drop('pickup_latitude').drop('dropoff_latitude')\
    .drop('dropoff_longitude').drop('tip_class').drop('total_amount').drop('tolls_amount').drop('mta_tax')\
    .drop('direct_distance').drop('surcharge')\
    .filter("passenger_count > 0 and passenger_count < 8 AND payment_type in ('CSH', 'CRD') AND tip_amount >= 0 AND tip_amount < 30 AND fare_amount >= 1 AND fare_amount < 150 AND trip_distance > 0 AND trip_distance < 100 AND trip_time_in_secs > 30 AND trip_time_in_secs < 7200" )

# CACHE & MATERIALIZE DATA-FRAME IN MEMORY. GOING THROUGH AND COUNTING NUMBER OF ROWS MATERIALIZES THE DATA-FRAME IN MEMORY
taxi_df_train_cleaned.cache()
taxi_df_train_cleaned.count()

# REGISTER DATA-FRAME AS A TEMP-TABLE IN SQL-CONTEXT
taxi_df_train_cleaned.registerTempTable("taxi_train")


# FUNCTIONS FOR REGRESSION WITH TIP AMOUNT AS TARGET VARIABLE
def parseRowOneHotRegression(line):
	return (line.tip_amount, Vectors.dense([line.pickup_hour, line.weekday, line.passenger_count,
                                        line.trip_time_in_secs, line.trip_distance, line.fare_amount]))

samplingFraction = 0.25;
trainingFraction = 0.75; 
testingFraction = (1-trainingFraction);
seed = 1234;

# Prepare the final testing set
trainData, testData = taxi_df_train_cleaned.randomSplit([trainingFraction, testingFraction], seed=seed)

# FOR REGRESSION TRAINING AND TESTING
oneHotTRAINreg = trainData.rdd.map(parseRowOneHotRegression)
oneHotTESTreg = testData.rdd.map(parseRowOneHotRegression)

###  CV USING ELASTIC NET FOR LINEAR REGRESSION

# DEFINE ALGORITHM/MODEL
lr = LinearRegression()

# DEFINE GRID PARAMETERS
# 8 params to optimise 
paramGrid = ParamGridBuilder().addGrid(lr.regParam, (0.01, 0.1))\
                              .addGrid(lr.maxIter, (5, 10))\
                              .addGrid(lr.tol, (1e-4, 1e-5))\
                              .addGrid(lr.elasticNetParam, (0.25,0.75))\
                              .build() 

# DEFINE PIPELINE 
# SIMPLY THE MODEL HERE, WITHOUT TRANSFORMATIONS
pipeline = Pipeline(stages=[lr])

# DEFINE CV WITH PARAMETER SWEEP
# splitting the dataset into a set of folds which are used as separate training and test datasets
# generate 3 (training, test) dataset pairs, each of which uses 2/3 of 
# the data for training and 1/3 for testing
# 8 params x 3 folds
# See: https://spark.apache.org/docs/latest/ml-tuning.html#cross-validation
cv = CrossValidator(estimator= lr,
                    estimatorParamMaps=paramGrid,
                    evaluator=RegressionEvaluator(),
                    numFolds=3)

# CONVERT TO DATA FRAME, AS CROSSVALIDATOR WON'T RUN ON RDDS
#trainDataFrame = sqlContext.createDataFrame(oneHotTRAINreg, ["features", "label"])

# TRAIN WITH CROSS-VALIDATION
#cv_model = cv.fit(trainDataFrame)
cv_model = cv.fit(oneHotTRAINreg.toDF(['label','features']))


# EVALUATE MODEL ON TEST SET
#testDataFrame = sqlContext.createDataFrame(oneHotTESTreg, ["features", "label"])
testDataFrame = oneHotTESTreg.toDF(['label','features'])

# MAKE PREDICTIONS ON TEST DOCUMENTS
# cvModel uses the best model found (lrModel).
predictionAndLabels = cv_model.transform(testDataFrame)
predictionAndLabels.select("features", "label", "prediction").show()

# validate the results
# metric to measure how well a fitted Model does on held-out test data
evaluator = RegressionEvaluator(metricName="rmse")
rmse = evaluator.evaluate(predictionAndLabels)
print("Root-mean-square error = %s" % rmse)


#### LOGISTIC REGRESSION







