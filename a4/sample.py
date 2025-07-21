from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.pipeline import PipelineModel
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.sql import SparkSession # Create a SparkSession

spark = SparkSession.builder.appName("MYAPP").getOrCreate()

csv_file = "2019-04.csv"

# Task 1: Create a dataset that only contains passenger_count (4th col), pulocationid (8th col), dolocationid (9th col),
# and total_amount (17th col) based on the 2019-04.csv dataset.
# Show the first 10 entries in the created dataset.
df = (spark.read.format("csv")
      .option("inferSchema", "true") # Infer schema (data types)
      .option("header", "true")
      .load(csv_file)
)
taxiDF = df.select("passenger_count", "pulocationid", "dolocationid", "total_amount")
taxiDF.show(10)

# Task 2: Create trainDF and testDF.
# I filtered out passenger counts that were equal to 0
taxiDF_filtered = taxiDF.filter(taxiDF.passenger_count != 0)
trainDF, testDF = taxiDF_filtered.randomSplit([.8, .2], seed=42)
print(f"There are {trainDF.count()} rows in the training set and {testDF.count()} in the test set")

# 2b. Transform the data
vecAssembler = VectorAssembler(
      inputCols=["passenger_count", "pulocationid", "dolocationid"],
      outputCol="features"
)
vecTrainDF = vecAssembler.transform(trainDF)
vecTrainDF.select("passenger_count", "pulocationid", "dolocationid", "features", "total_amount").show(10)

# 3. Create a decision tree regressor to predict total_amount from the other three features.
dtr = DecisionTreeRegressor(featuresCol="features", labelCol="total_amount")

# 4. Create a pipeline.
pipeline = Pipeline(stages=[vecAssembler, dtr])

# 5. Train the model.
dtrModel = dtr.fit(vecTrainDF)
pipelineModel = pipeline.fit(trainDF)

# 6. Show the predicted results along with the three features in the notebook. (Show the first 10 entries.)
predDF = pipelineModel.transform(testDF)
predDF.select("passenger_count", "pulocationid", "dolocationid", "features", "total_amount", "prediction").show(10)

# 7. Evaluate the model with RMSE. (The RMSE value should be in the notebook.)
regressionEvaluator = RegressionEvaluator(
      predictionCol="prediction",
      labelCol="total_amount",
      metricName="rmse"
)
rmse = regressionEvaluator.evaluate(predDF)
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Saves the pipeline model then loads it
pipelinePath = "/tmp/lr-pipeline-model"
pipelineModel.write().overwrite().save(pipelinePath)
savedPipelineModel = PipelineModel.load(pipelinePath)