from pyspark.sql.window import Window
from pyspark.sql import functions as F



crm_cust_info_df = spark.sql("""
                             with remove_dup as (
                             SELECT * ,
                                    row_number() over(PARTITION BY cst_id ORDER BY _load_timestamp DESC) AS rn
                             FROM bike_lakehouse.bronze.crm_cust_info
                             WHERE cst_id IS NOT NULL
                             ),
                             string_cleaning as (
                     
                             SELECT cst_id,cst_key,
                                    trim(cst_firstname) as cst_firstname,
                                    trim(cst_lastname) as cst_lastname,
                                    case
                                          when upper(trim(cst_marital_status)) = 'S' then 'single'
                                          when upper(trim(cst_marital_status)) ='M'  then 'married'
                                          else 'n/a'
                                    end as cst_marital_status, -- Normalize marital status values to readable format
                                    case
                                          when upper(trim(cst_gndr)) = 'F' then 'female'
                                          when upper(trim(cst_gndr)) = 'M' then 'male'
                                          else 'n/a'
                                    end as cst_gndr, -- Normalize gender values to readable format
                                    cast(cst_create_date as date),
                                    _load_timestamp,_source_system
                             FROM remove_dup
                             WHERE rn = 1
                             )

                             SELECT * FROM string_cleaning
                             """)


crm_cust_info_df.write.mode("overwrite").saveAsTable("bike_lakehouse.silver.crm_cust_info")