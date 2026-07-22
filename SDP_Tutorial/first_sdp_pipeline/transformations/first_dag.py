from pyspark import pipelines as dp
from pyspark.sql.functions import *


@dp.materialized_view(name="src_sales")
def src_sales():
    df_sales = spark.read.table("sdp_catalog.sources.sales")
    df_sales = df_sales.withColumn("creation_date",current_timestamp())
    return df_sales