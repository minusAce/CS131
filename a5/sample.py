from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("CarEvaluation").getOrCreate()

data_file = "car.data"

df = (spark.read.format("csv")
      .option("inferSchema", "false") # Infer schema (data types)
      .option("header", "false") # No header in the CSV file
      .load(data_file)
)
df = df.toDF("buying", "maint", "doors", "persons", "lug_boot", "safety", "class")
print("Unbalanced Dataset")
df.groupBy("class").count().show()

unacc_df = df.filter(col('class') == 'unacc')
acc_df = df.filter(col('class') == 'acc')
good_df = df.filter(col('class') == 'good')
vgood_df = df.filter(col('class') == 'vgood')

oversampled_acc_df = acc_df.sample(withReplacement=True, fraction=3.15, seed=42)
oversampled_good_df = good_df.sample(withReplacement=True, fraction=17.3, seed=42)
oversampled_vgood_df = vgood_df.sample(withReplacement=True, fraction=17.9, seed=42)
balanced_df = unacc_df.union(oversampled_acc_df).union(oversampled_good_df).union(oversampled_vgood_df)
print("Balanced Dataset")
balanced_df.groupBy("class").count().show()

# How much of an effect does the price and maintenance cost have on acceptability?
# If a car has a lower price does that mean more people will accept it?
carDF_1 = balanced_df.select("buying", "maint", "class")
trainDF_1, testDF_1 = carDF_1.randomSplit([0.8, 0.2], seed=42)

indexers_1 = [
    StringIndexer(inputCol="buying", outputCol="buying_idx"),
    StringIndexer(inputCol="maint", outputCol="maint_idx"),
    StringIndexer(inputCol="class", outputCol="class_idx")
]

vecAssembler_1 = VectorAssembler(
    inputCols=["buying_idx", "maint_idx"],
    outputCol="features"
)

dt_1 = DecisionTreeClassifier(featuresCol="features", labelCol="class_idx")

labelConverter_1 = IndexToString(
    inputCol="prediction",
    outputCol="predicted_class",
    labels=indexers_1[-1].fit(carDF_1).labels
)

pipeline_1 = Pipeline(stages=indexers_1 + [vecAssembler_1, dt_1, labelConverter_1])
pipelineModel_1 = pipeline_1.fit(trainDF_1)

predDF_1 = pipelineModel_1.transform(testDF_1)
predDF_1.select("buying", "maint", "class", "predicted_class").show(10)

evaluator_1 = MulticlassClassificationEvaluator(
    labelCol="class_idx", predictionCol="prediction", metricName="accuracy"
)
accuracy_1 = evaluator_1.evaluate(predDF_1)
print(f"Accuracy (buying + maint): {accuracy_1}")

# How much do doors, persons, and luggage boot matter compared with safety?
# If a car has low utility but high safety does that make it more acceptable?
carDF_2 = balanced_df.select("doors", "persons", "lug_boot", "safety", "class")
trainDF_2, testDF_2 = carDF_2.randomSplit([0.8, 0.2], seed=42)

indexers_2 = [
    StringIndexer(inputCol="doors", outputCol="doors_idx"),
    StringIndexer(inputCol="persons", outputCol="persons_idx"),
    StringIndexer(inputCol="lug_boot", outputCol="lug_boot_idx"),
    StringIndexer(inputCol="safety", outputCol="safety_idx"),
    StringIndexer(inputCol="class", outputCol="class_idx")
]

vecAssembler_2 = VectorAssembler(
    inputCols=["doors_idx", "persons_idx", "lug_boot_idx", "safety_idx"],
    outputCol="features"
)

dt_2 = DecisionTreeClassifier(featuresCol="features", labelCol="class_idx")
labelConverter_2 = IndexToString(
    inputCol="prediction",
    outputCol="predicted_class",
    labels=indexers_2[-1].fit(carDF_2).labels
)

pipeline_2 = Pipeline(stages=indexers_2 + [vecAssembler_2, dt_2, labelConverter_2])
pipelineModel_2 = pipeline_2.fit(trainDF_2)

predDF_2 = pipelineModel_2.transform(testDF_2)
predDF_2.select("doors", "persons", "lug_boot", "safety", "class", "predicted_class").show(10)

evaluator_2 = MulticlassClassificationEvaluator(
    labelCol="class_idx", predictionCol="prediction", metricName="accuracy"
)
accuracy_2 = evaluator_2.evaluate(predDF_2)
print(f"Accuracy (doors + persons + lug_boot + safety): {accuracy_2}")

# Export predictions as CSV
predDF_1.select(
    "buying", 
    "maint", 
    "class", 
    "predicted_class"
).coalesce(1).write.csv("out/cost_eval", header=True, mode="overwrite")

predDF_2.select(
        "doors",
        "persons",
        "lug_boot",
        "safety",
        "class",
        "predicted_class"
).coalesce(1).write.csv("out/util_eval", header=True, mode="overwrite")

spark.stop()
