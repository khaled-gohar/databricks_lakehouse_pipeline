from pyspark.sql.window import Window
from pyspark.sql import functions as F




dim_products_df = spark.sql("""
                                 
SELECT
    ROW_NUMBER() OVER (ORDER BY pn.prd_start_dt, pn.prd_key) AS product_key, -- Surrogate key
    pn.prd_id       AS product_id,
    pn.prd_key      AS product_number,
    pn.prd_nm       AS product_name,
    pn.cat_id       AS category_id,
    pc.cat          AS category,
    pc.subcat       AS subcategory,
    pc.maintenance  AS maintenance,
    pn.prd_cost     AS cost,
    pn.prd_line     AS product_line,
    pn.prd_start_dt AS start_date
FROM bike_lakehouse.silver.crm_prd_info pn
LEFT JOIN bike_lakehouse.silver.erp_px_cat_g1v2 pc
    ON pn.cat_id = pc.id
WHERE pn.prd_end_dt IS NULL; -- Filter out all historical data
                                 
                                 
                                 """)


dim_products_df.write.mode("overwrite").saveAsTable("bike_lakehouse.gold.dim_products")