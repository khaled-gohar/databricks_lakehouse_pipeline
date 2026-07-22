import sys

sys.path.append("/Workspace/Users/kahledtrojan@gmail.com/databricks_lakehouse_pipeline_de/bike_lakehouse")



from pyspark.sql.functions import current_timestamp, lit
from src.utils.config_reader import read_config
from src.utils.postgres_connection import get_postgres_properties


base_path = "/Workspace/Users/kahledtrojan@gmail.com/databricks_lakehouse_pipeline_de/bike_lakehouse/config"
environment = "dev"

jdbc_url,properties = get_postgres_properties()

config = read_config(base_path,environment)


def load_to_bronze(tables,source_system):

    for table,table_mode in tables.items():
        mode = table_mode.get("load_mode","append")
        
        df = (
            spark.read
            .jdbc(
                url=jdbc_url,
                table=F"{source_system}_{table}",
                properties=properties
            )
        )

        df = df.withColumn("_load_timestamp",current_timestamp()).withColumn("_source_system",lit(source_system))

        df.write.mode(mode).saveAsTable(f"bike_lakehouse.bronze.{source_system}_{table}")


for source_system,details in config["source_systems"].items():

    load_to_bronze(details["tables"],source_system)
