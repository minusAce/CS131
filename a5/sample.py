from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder.appName("CarEvaulation").getOrCreate()

data_file = "car.data"

df = (spark.read.format("csv")
      .option("inferSchema", "true") # Infer schema (data types)
      .option("header", "false") # No header in the CSV file
      .load(data_file)
)
df = df.toDF("buying", "maint", "doors", "persons", "lug_boot", "safety", "class")

# How much of an effect does the 'buying' and 'safety' features have on the 'class'?
# Generally if a cars buying and safety ratings are high, the class will be better.
carDF_1 = df.select("buying", "safety", "class")
trainDF_1, testDF_1 = carDF_1.randomSplit([0.8, 0.2], seed=42)

indexers_1 = [
    StringIndexer(inputCol="buying", outputCol="buying_idx"),
    StringIndexer(inputCol="safety", outputCol="safety_idx"),
    StringIndexer(inputCol="class", outputCol="class_idx")
]

vecAssembler_1 = VectorAssembler(
    inputCols=["buying_idx", "safety_idx"],
    outputCol="features"
)

dt_1 = DecisionTreeClassifier(featuresCol="features", labelCol="class_idx")

labelConverter_1 = IndexToString(inputCol="prediction", outputCol="predicted_label", labels=indexers_1[-1].fit(carDF_1).labels)

pipeline_1 = Pipeline(stages=indexers_1 + [vecAssembler_1, dt_1, labelConverter_1])
pipelineModel_1 = pipeline_1.fit(trainDF_1)

predDF_1 = pipelineModel_1.transform(testDF_1)
predDF_1.select("buying", "safety", "class", "predicted_label").show(10)

evaluator_1 = MulticlassClassificationEvaluator(
    labelCol="class_idx", predictionCol="prediction", metricName="accuracy"
)
accuracy_1 = evaluator_1.evaluate(predDF_1)
print(f"Accuracy (buying + safety): {accuracy_1}")

# How much of an effect does the 'doors', 'persons', and 'lug_boot' features have on the 'class'?
# The amount of doors, persons, and the size of the lug_boot don't have a significant effect on the class.
carDF_2 = df.select("doors", "persons", "lug_boot", "class")
filteredDF_2 = carDF_2.filter(
    (carDF_2.doors == "2") | (carDF_2.persons == "2") | (carDF_2.lug_boot == "small")
)
trainDF_2, testDF_2 = filteredDF_2.randomSplit([0.8, 0.2], seed=42)

indexers_2 = [
    StringIndexer(inputCol="doors", outputCol="doors_idx"),
    StringIndexer(inputCol="persons", outputCol="persons_idx"),
    StringIndexer(inputCol="lug_boot", outputCol="lug_boot_idx"),
    StringIndexer(inputCol="class", outputCol="class_idx")
]

vecAssembler_2 = VectorAssembler(
    inputCols=["doors_idx", "persons_idx", "lug_boot_idx"],
    outputCol="features"
)

dt_2 = DecisionTreeClassifier(featuresCol="features", labelCol="class_idx")
labelConverter_2 = IndexToString(inputCol="prediction", outputCol="predicted_label", labels=indexers_2[-1].fit(filteredDF_2).labels)

pipeline_2 = Pipeline(stages=indexers_2 + [vecAssembler_2, dt_2, labelConverter_2])
pipelineModel_2 = pipeline_2.fit(trainDF_2)

predDF_2 = pipelineModel_2.transform(testDF_2)
predDF_2.select("doors", "persons", "lug_boot", "class", "predicted_label").show(10)

evaluator_2 = MulticlassClassificationEvaluator(
    labelCol="class_idx", predictionCol="prediction", metricName="accuracy"
)
accuracy_2 = evaluator_2.evaluate(predDF_2)
print(f"Accuracy (doors + persons + lug_boot): {accuracy_2}")