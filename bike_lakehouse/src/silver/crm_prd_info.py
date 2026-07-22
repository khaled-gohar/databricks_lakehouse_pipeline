from pyspark.sql.window import Window
from pyspark.sql import functions as F


crm_prd_info_df = spark.sql("""
                            
        SELECT
			prd_id,
			REPLACE(SUBSTRING(prd_key, 1, 5), '-', '_') AS cat_id, -- Extract category ID
			SUBSTRING(prd_key, 7, LEN(prd_key)) AS prd_key,        -- Extract product key
			prd_nm,
			coalesce(prd_cost, 0) AS prd_cost,
			CASE 
				WHEN UPPER(TRIM(prd_line)) = 'M' THEN 'Mountain'
				WHEN UPPER(TRIM(prd_line)) = 'R' THEN 'Road'
				WHEN UPPER(TRIM(prd_line)) = 'S' THEN 'Other Sales'
				WHEN UPPER(TRIM(prd_line)) = 'T' THEN 'Touring'
				ELSE 'n/a'
			END AS prd_line, -- Map product line codes to descriptive values
            CAST(prd_start_dt AS DATE) AS prd_start_dt,
            date_sub(
                LEAD(cast(prd_start_dt as DATE)) OVER (PARTITION BY prd_key ORDER BY cast(prd_start_dt as DATE)),
                1
            ) AS prd_end_dt -- Calculate end date as one day before the next start date
		FROM bike_lakehouse.bronze.crm_prd_info
                            
                            
                            
                            """)


crm_prd_info_df.write.mode("overwrite").saveAsTable("bike_lakehouse.silver.crm_prd_info")