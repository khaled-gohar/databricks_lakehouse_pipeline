from pyspark.sql.window import Window
from pyspark.sql import functions as F


erp_loc_a101_df = spark.sql("""
        SELECT
			REPLACE(cid, '-', '') AS cid, 
			CASE
				WHEN TRIM(cntry) = 'DE' THEN 'Germany'
				WHEN TRIM(cntry) IN ('US', 'USA') THEN 'United States'
				WHEN TRIM(cntry) = '' OR cntry IS NULL THEN 'n/a'
				ELSE TRIM(cntry)
			END AS cntry -- Normalize and Handle missing or blank country codes
		FROM bike_lakehouse.bronze.erp_loc_a101
                            """)

erp_loc_a101_df.write.mode("overwrite").saveAsTable("bike_lakehouse.silver.erp_loc_a101")