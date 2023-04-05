# Databricks notebook source
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.sql import functions as f
from pyspark.ml.feature import IndexToString


# COMMAND ----------


# Azure storage access info
blob_account_name = "azureopendatastorage"
blob_container_name = "censusdatacontainer"
blob_relative_path = "release/us_population_county/"
blob_sas_token = r""

# COMMAND ----------

# Allow SPARK to read from Blob remotely
wasbs_path = 'wasbs://%s@%s.blob.core.windows.net/%s' % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set(
  'fs.azure.sas.%s.%s.blob.core.windows.net' % (blob_container_name, blob_account_name),
  blob_sas_token)
print('Remote blob path: ' + wasbs_path)

# COMMAND ----------

# SPARK read parquet, note that it won't load any data yet by now
df_source = spark.read.parquet(wasbs_path)
print('Register the DataFrame as a SQL temporary view: source')
df_source.createOrReplaceTempView('source')

# COMMAND ----------

# Display top 10 rows in SQL
print('Displaying top 10 rows: ')
display(spark.sql('SELECT * FROM source LIMIT 10'))

# COMMAND ----------

# display in data frame
display(df_source)

# COMMAND ----------

#Run basic stats on our data
df_source.summary().show()

# COMMAND ----------

df_source.select('year').distinct().collect()

# COMMAND ----------

# check nulls - cause trouble on the way
df_source.filter(f.isnull('race')).count()


# COMMAND ----------

# let's deal with those sucker NULLs and empty strings
string_col = [item[0] for item in df_source.dtypes if item[1].startswith('string')]
big_int_col = [item[0] for item in df_source.dtypes if item[1].startswith('bigint')]
double_col = [item[0] for item in df_source.dtypes if item[1].startswith('double')]
int_col = [item[0] for item in df_source.dtypes if item[1].startswith('int')]

df_source_null = (df_source.fillna('N/A', subset = string_col)
        .fillna(0, subset = big_int_col)
        .fillna(0, subset = int_col)
        .fillna(0.0, subset = double_col))

# COMMAND ----------

df_source_null.show()

# COMMAND ----------



# COMMAND ----------

# list of string columns from above - to make features we need to make vectors
#TODO how to do thi dynamically?

array_list_string_col = ['stateName', 'countyName', 'race', 'sex']
array_list_indexed_string_col = [name+"_index" for name in array_list_string_col]
indexer = StringIndexer(inputCols=array_list_string_col, outputCols=array_list_indexed_string_col, handleInvalid='error', stringOrderType='frequencyDesc').setHandleInvalid("keep")
indexer_model = indexer.fit(df_source_null)
df_source_null_indexed = indexer_model.transform(df_source_null)
df_source_null_indexed.show()

# COMMAND ----------

# let's build our vectors

list_col_to_vector = array_list_indexed_string_col+ ['minAge', 'maxAge']
vectors = VectorAssembler(inputCols=list_col_to_vector, outputCol='features')
df_vector = vectors.transform(df_source_null_indexed)

# COMMAND ----------

df_vector.show(5)

# COMMAND ----------

df_train = df_vector.where(f.col("year")==2000)
df_test = df_vector.where(f.col("year")!=2000)

# random split example
# (df_train, df_test) = df_source.randomSplit([0.8, 0.2])

# COMMAND ----------

# While we could say something like this...
# clean_df = df_out.select(['features', 'population'])
# I want to rename the 'PRICE' column to 'label' as well
df_train_clean = (df_train
#                   .select(['features', f.col('population')])
                 )
df_test_clean = (df_test
#                  .select(['features', f.col('population')])
                )


# COMMAND ----------

df_train_clean.show(5)
df_train_clean.describe().show()

# COMMAND ----------

df_test_clean.show(5)
df_train_clean.describe().show()

# COMMAND ----------

# creating an instance of a linear regression model
lr_model = LinearRegression(featuresCol='features',labelCol='population')

# COMMAND ----------

# fitting the model to the train set
fit_model = lr_model.fit(df_train_clean)

# COMMAND ----------

print("Coefficients: " + str(fit_model.coefficients))
print("Intercept: " + str(fit_model.intercept))


# COMMAND ----------

test_results = fit_model.evaluate(df_test_clean)

# COMMAND ----------

print("RMSE: %f" % test_results.rootMeanSquaredError)
print("r2: %f" % test_results.r2)
print("r2_adjusted: %f" % test_results.r2adj)
print("degreesOfFreedom: %f" % test_results.degreesOfFreedom)

# COMMAND ----------

residuals = test_results.residuals
display(residuals)

# COMMAND ----------

df_prediction_test = test_results.predictions

# COMMAND ----------

df_prediction_train = fit_model.transform(df_train_clean)

# COMMAND ----------

# Lets get some predictions

# df_prediction = fit_model.transform(df_test_clean)

# COMMAND ----------

# MAGIC %md lets see how we score on the training data

# COMMAND ----------


display(df_prediction_train.select("population","prediction"))

# COMMAND ----------

display(df_prediction_test.select("population","prediction"))

# COMMAND ----------

# MAGIC %md Let's have a look at residuals

# COMMAND ----------

df_predictions_with_residuals = df_prediction.withColumn("residual", (f.col("population") - f.col("prediction")))
display(df_predictions_with_residuals.agg({'residual': 'mean'}))

# COMMAND ----------

display(df_predictions_with_residuals.select("population", "residual"))

# COMMAND ----------

evaluator = RegressionEvaluator(predictionCol="prediction",  labelCol="population", metricName="r2")
print("Train R2:", evaluator.evaluate(df_prediction_train))
print("Test R2:", evaluator.evaluate(df_prediction_test))
