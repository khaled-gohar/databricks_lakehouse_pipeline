# 🚴 Databricks Lakehouse Pipeline

### End-to-End Data Engineering Pipeline with Neon PostgreSQL & Databricks

An end-to-end **Lakehouse data engineering project** built with **Neon PostgreSQL, Databricks, PySpark, Delta Lake, and Unity Catalog**.

The project implements a **Bronze → Silver → Gold Medallion Architecture**, transforming raw PostgreSQL data into analytics-ready dimensional models.

---

<p align="center">

![Databricks](https://img.shields.io/badge/Databricks-EF3B24?style=for-the-badge\&logo=databricks\&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge\&logo=apachespark\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD8?style=for-the-badge\&logo=delta\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge\&logo=github\&logoColor=white)

</p>

---

## 📌 Overview

This project demonstrates how data can be ingested from a **Neon PostgreSQL database**, processed in **Databricks**, and transformed through multiple Lakehouse layers into a business-friendly **Star Schema**.

### Pipeline at a glance

```text
                  ┌──────────────────────┐
                  │   Neon PostgreSQL    │
                  │     Source DB        │
                  └──────────┬───────────┘
                             │
                             │ Spark JDBC
                             ▼
                  ┌──────────────────────┐
                  │       🥉 Bronze      │
                  │     Raw Delta Data   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       🥈 Silver      │
                  │ Cleaned & Transformed│
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │        🥇 Gold       │
                  │   Business Models    │
                  └──────────┬───────────┘
                             │
                    ┌────────┴────────┐
                    ▼        ▼        ▼
               Customers Products   Sales
```

---

## 🏗️ Architecture

The project follows the **Medallion Architecture** pattern.

|     Layer     | Purpose                                         | Output               |
| :-----------: | ----------------------------------------------- | -------------------- |
| 🥉 **Bronze** | Ingest raw data from PostgreSQL                 | Raw Delta Tables     |
| 🥈 **Silver** | Clean, standardize, validate and transform data | Refined Delta Tables |
|  🥇 **Gold**  | Build business-ready dimensional models         | Star Schema          |

### 🔄 Data Flow

```text
Neon PostgreSQL
      │
      ▼
┌───────────────┐
│     Bronze    │
│  Raw Ingestion│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     Silver    │
│ Transformation│
└───────┬───────┘
        │
        ▼
┌──────────────────────────────┐
│             Gold             │
│                              │
│  dim_customers               │
│  dim_products                │
│  fact_sales                  │
└──────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Technology             | Purpose                                |
| ---------------------- | -------------------------------------- |
| 🟠 **Databricks**      | Lakehouse processing and orchestration |
| 🐍 **Python**          | Pipeline and transformation logic      |
| ⚡ **PySpark**          | Distributed data processing            |
| 🐘 **Neon PostgreSQL** | Source database                        |
| 🔷 **Delta Lake**      | Lakehouse storage format               |
| 🔐 **Unity Catalog**   | Data and table governance              |
| 🔧 **Git / GitHub**    | Version control                        |
| 📊 **SQL / Spark SQL** | Data transformation and modeling       |

---

# ⚙️ Configuration & Environment Management

The project separates **environment-specific configuration** from **credentials and sensitive information** to keep the pipeline easier to maintain across development and production environments.

### 🗂️ YAML Configuration

Pipeline configuration is managed through **YAML files**, with separate configurations for different environments:

```text
config/
├── dev/
│   └── config.yaml
└── prod/
    └── config.yaml
```

The YAML configuration is used to define environment-specific settings such as:

* 🗄️ Catalog and schema names
* 📋 Source and target table configuration
* 🔄 Load behavior
* ⚙️ Pipeline parameters
* 🌍 Environment-specific settings

This allows the same pipeline code to be used across environments while changing configuration rather than modifying the application logic.

### 🔐 Environment Variables

Sensitive values are kept outside the source code using a `.env` file.

Examples include:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

The `.env` file is **not committed to GitHub** and should be included in `.gitignore.

This separation provides a simple structure:

```text
                 ┌─────────────────────┐
                 │   Pipeline Code     │
                 │   Python / PySpark  │
                 └──────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐             ┌──────────────┐
       │ YAML Config  │             │ Environment  │
       │              │             │ Variables    │
       │ DEV / PROD   │             │ Credentials  │
       └──────────────┘             └──────────────┘
```

### 🔒 Security Principle

The project follows a simple separation of concerns:

| Configuration Type         | Stored In                  | Examples                               |
| -------------------------- | -------------------------- | -------------------------------------- |
| 🛠️ Pipeline configuration | YAML                       | Catalog, schema, tables, load settings |
| 🌍 Environment settings    | YAML                       | DEV / PROD-specific values             |
| 🔑 Credentials             | `.env` / secret management | Username, password, connection details |
| 💻 Transformation logic    | Python / PySpark           | Ingestion and transformation code      |

> **Important:** `.env` files containing credentials should never be committed to version control. In a deployed Databricks environment, sensitive credentials should be managed through an appropriate secret-management mechanism.

---

# 🥉 Bronze Layer

The Bronze layer is responsible for ingesting data from the **Neon PostgreSQL source database**.

Data is read using **Spark JDBC** and stored as Delta tables in Databricks.

### Bronze responsibilities

* 🔌 Connect to PostgreSQL through JDBC
* 📥 Ingest configured source tables
* 🧾 Add ingestion metadata
* 💾 Store data as Delta tables
* ⚙️ Use configuration-driven ingestion

Additional metadata is added during ingestion:

| Column            | Purpose                          |
| ----------------- | -------------------------------- |
| `_load_timestamp` | Records when the data was loaded |
| `_source_system`  | Identifies the source system     |

### Bronze flow

```text
Neon PostgreSQL
      │
      │ JDBC
      ▼
   PySpark
      │
      ▼
Delta Bronze Tables
```

---

# 🥈 Silver Layer

The Silver layer transforms the raw Bronze datasets into cleaner and more consistent datasets.

Transformations are organized by source table.

### CRM Sources

| Table               | Purpose              |
| ------------------- | -------------------- |
| `crm_cust_info`     | Customer information |
| `crm_prd_info`      | Product information  |
| `crm_sales_details` | Sales transactions   |

### ERP Sources

| Table             | Purpose                         |
| ----------------- | ------------------------------- |
| `erp_cust_az12`   | Additional customer information |
| `erp_loc_a101`    | Customer location information   |
| `erp_px_cat_g1v2` | Product category information    |

### Silver transformations include

* 🧹 Data cleansing
* 🔍 Data validation
* ♻️ Deduplication
* 🔤 Standardization
* 🔗 Data enrichment
* 📐 Preparing datasets for dimensional modeling

Keeping each transformation in its own module makes the pipeline easier to maintain and extend.

---

# 🥇 Gold Layer

The Gold layer contains the final **analytics-ready dimensional model**.

The project uses a **Star Schema** consisting of two dimensions and one fact table.

```text
                    ┌──────────────────┐
                    │  dim_customers   │
                    └────────┬─────────┘
                             │
                             │
                       ┌─────▼─────┐
                       │ fact_sales│
                       └─────┬─────┘
                             │
                             │
                    ┌────────▼────────┐
                    │  dim_products   │
                    └─────────────────┘
```

---

## 👥 `dim_customers`

The customer dimension combines information from the CRM and ERP datasets.

### Key attributes

| Attribute         | Description                |
| ----------------- | -------------------------- |
| Customer ID       | Source customer identifier |
| Customer Number   | Business customer number   |
| First / Last Name | Customer name              |
| Country           | Customer country           |
| Gender            | Customer gender            |
| Marital Status    | Customer marital status    |
| Birthdate         | Customer date of birth     |
| Create Date       | Customer creation date     |

A surrogate **`customer_key`** is generated for the Gold model.

---

## 🚲 `dim_products`

The product dimension combines CRM product information with ERP category information.

### Key attributes

| Attribute      | Description               |
| -------------- | ------------------------- |
| Product ID     | Source product identifier |
| Product Number | Business product number   |
| Product Name   | Product description       |
| Category       | Product category          |
| Subcategory    | Product subcategory       |
| Product Line   | Product line              |
| Cost           | Product cost              |
| Start Date     | Product start date        |

A surrogate **`product_key`** is generated for the Gold model.

Current product records are selected for the dimension.

---

## 💰 `fact_sales`

The sales fact table contains the transactional sales data and connects transactions to the Gold dimensions.

### Key attributes

| Attribute     | Description                    |
| ------------- | ------------------------------ |
| Order Number  | Sales order                    |
| Product Key   | Foreign key to `dim_products`  |
| Customer Key  | Foreign key to `dim_customers` |
| Order Date    | Order date                     |
| Shipping Date | Shipping date                  |
| Due Date      | Required delivery date         |
| Sales Amount  | Transaction sales amount       |
| Quantity      | Quantity sold                  |
| Price         | Product price                  |

The fact table resolves the source identifiers into the surrogate keys used by the Gold dimensions.

---

# ⚙️ Pipeline Orchestration

The pipeline can be executed using **Databricks Jobs**, with the different stages organized as dependent tasks.

```text
┌───────────────┐
│     Bronze    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     Silver    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│      Gold     │
└───────────────┘
```

### 📸 Databricks Job

<p align="center">
  <img src="docs/images/databricks-job.png" alt="Databricks Job Workflow" width="900"/>
</p>

> **Databricks Job showing the pipeline workflow and task dependencies.**

---

# 📂 Project Structure

```text
databricks_lakehouse_pipeline/
│
├── 📁 bike_lakehouse/
│   │
│   ├── 📁 config/
│   │   └── 📁 dev/
│   │
│   ├── 📁 notebooks/
│   │   ├── bronze.ipynb
│   │   ├── Silver.ipynb
│   │   ├── clean_tables.ipynb
│   │   └── gold.ipynb
│   │
│   ├── 📁 src/
│   │   │
│   │   ├── 📁 bronze/
│   │   │   └── bronze_load.py
│   │   │
│   │   ├── 📁 silver/
│   │   │   ├── crm_cust_info.py
│   │   │   ├── crm_prd_info.py
│   │   │   ├── crm_sales_details.py
│   │   │   ├── erp_cust_az12.py
│   │   │   ├── erp_loc_a101.py
│   │   │   └── erp_px_cat_g1v2.py
│   │   │
│   │   ├── 📁 gold/
│   │   │   ├── dim_customers.py
│   │   │   ├── dim_products.py
│   │   │   └── fact_sales.py
│   │   │
│   │   └── 📁 utils/
│   │
│   └── 📁 tests/
│
├── 📁 docs/
│   └── 📁 images/
│       └── databricks-job.png
│
└── README.md
```

---

# 🧩 Key Data Engineering Concepts

This project demonstrates practical implementation of:

* 🏛️ Medallion / Lakehouse Architecture
* 🔌 PostgreSQL ingestion with Spark JDBC
* ⚡ PySpark data processing
* 🧹 Data cleansing and standardization
* 🔄 Configuration-driven ingestion
* 💾 Delta Lake
* 🔐 Unity Catalog
* ⭐ Dimensional modeling
* 🔑 Surrogate keys
* 📊 Star Schema
* 📦 Fact and dimension tables
* 🔗 Source-to-dimension key mapping
* ⚙️ Databricks Jobs
* 🌱 Git-based project structure

---

# 🚀 Future Improvements

The project can be extended with:

* 🔄 Incremental ingestion using watermarks
* 📝 Change Data Capture (CDC)
* 🧪 Automated data-quality testing
* 📋 Pipeline audit and monitoring tables
* 🔁 Slowly Changing Dimensions (SCD)
* 🚦 Improved error handling and retry logic
* 🔧 CI/CD with Databricks Asset Bundles or GitHub Actions

These are considered future enhancements rather than current pipeline capabilities.

---

# 👨‍💻 Author

**Khaled Gamal Eldin Gohar**

**Data Engineer | Analytics Engineer**

### Core Technologies

`Databricks` · `PySpark` · `Python` · `SQL` · `PostgreSQL` · `Delta Lake` · `Data Modeling` · `ETL` · `Power BI`

---

<p align="center">

⭐ If you found this project useful, feel free to explore the repository.

</p>
