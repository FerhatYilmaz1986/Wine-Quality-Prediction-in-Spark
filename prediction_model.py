import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import sys

#Create and connect to spark session, read data given in docker command
spark = SparkSession.builder.master('local[*]').appName('Predict_model').getOrCreate()
test_set =spark.read.csv(sys.argv[-1], header=True, inferSchema= True, sep=';')

# Create feature vector
assembler = VectorAssembler(inputCols=[test_set.columns[0],
 test_set.columns[1],
 test_set.columns[2],
 test_set.columns[3],
 test_set.columns[4],
 test_set.columns[5],
 test_set.columns[6],
 test_set.columns[7],
 test_set.columns[8],
 test_set.columns[9],
 test_set.columns[10]],outputCol = 'features')
test_assembled = assembler.transform(test_set)
test_assembled = test_assembled.select(test_assembled.columns[-1], test_assembled.columns[-2])

# Load trained classification model
rfp = RandomForestClassificationModel.load('RF_model')

#Predict classes of new data
predictions = rfp.transform(test_assembled)

#Evaluate model performance
multi_evaluator = MulticlassClassificationEvaluator(labelCol = test_assembled.columns[-1], metricName = 'f1')
print('F-1 Score of the classification model:', multi_evaluator.evaluate(predictions))
