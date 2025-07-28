from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import PipelineModel

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
oneNT = df.select("buying", "safety", "class")
indexers_oneNT = [
    StringIndexer(inputCol="buying", outputCol="buying_idx"),
    StringIndexer(inputCol="safety", outputCol="safety_idx"),
    StringIndexer(inputCol="class", outputCol="class_idx")
]

vecAssembler_oneNT = VectorAssembler(
    inputCols=["buying_idx", "safety_idx"],
    outputCol="features"
)
dt_oneNT = DecisionTreeClassifier(featuresCol="features", labelCol="class_idx")

pipeline_oneNT = Pipeline(stages=indexers_oneNT + [vecAssembler_oneNT, dt_oneNT])
model_oneNT = pipeline_oneNT.fit(oneNT)

predictions_oneNT = model_oneNT.transform(oneNT)
predictions_oneNT.show(10)

evaluator_oneNT = MulticlassClassificationEvaluator(labelCol="class_idx", predictionCol="prediction", metricName="accuracy")
accuracy_oneNT = evaluator_oneNT.evaluate(predictions_oneNT)
print(f"Accuracy (buying + safety): {accuracy_oneNT}")

# How much of an effect does the 'doors', 'persons', and 'lug_boot' features have on the 'class'?
# The amount of doors, persons, and the size of the lug_boot don't have a significant effect on the class.
twoNT = df.select("doors", "persons", "lug_boot", "class")
twoNT_filtered = twoNT.filter(
    ((twoNT.doors == "2") | (twoNT.persons == "2")) | (twoNT.lug_boot == "small")
)
twoNT_filtered.show(10)
indexers_twoNT = [
    StringIndexer(inputCol="doors", outputCol="doors_idx"),
    StringIndexer(inputCol="persons", outputCol="persons_idx"),
    StringIndexer(inputCol="lug_boot", outputCol="lug_boot_idx"),
    StringIndexer(inputCol="class", outputCol="class_idx")
]

assembler_twoNT = VectorAssembler(
    inputCols=["doors_idx", "persons_idx", "lug_boot_idx"],
    outputCol="features"
)
dt_twoNT = DecisionTreeClassifier(labelCol="class_idx", featuresCol="features")

pipeline_twoNT = Pipeline(stages=indexers_twoNT + [assembler_twoNT, dt_twoNT])
model_twoNT = pipeline_twoNT.fit(twoNT_filtered)

predictions_twoNT = model_twoNT.transform(twoNT_filtered)
predictions_twoNT.show(10)

evaluator_twoNT = MulticlassClassificationEvaluator(labelCol="class_idx", predictionCol="prediction", metricName="accuracy")
accuracy_twoNT = evaluator_twoNT.evaluate(predictions_twoNT)
print(f"Accuracy (doors + persons + lug_boot): {accuracy_twoNT}")
