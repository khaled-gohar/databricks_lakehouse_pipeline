from pyspark.sql.window import Window
from pyspark.sql import functions as F


erp_px_cat_g1v2_df = spark.sql("""
                               
        SELECT
			id,
			cat,
			subcat,
			maintenance
		FROM bike_lakehouse.bronze.erp_px_cat_g1v2
                               
                               """)


erp_px_cat_g1v2_df.write.mode("overwrite").saveAsTable("bike_lakehouse.silver.erp_px_cat_g1v2")