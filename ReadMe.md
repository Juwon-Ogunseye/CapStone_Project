# Brazilian E-Commerce ETL Project

## Project Overview

This project demonstrates an end-to-end ETL process using the Brazilian E-Commerce dataset from Kaggle. The objective is to help data end users answer analytical questions by leveraging tools like PostgreSQL, Docker, Docker Compose, Airflow, dbt, and BigQuery. The project covers data ingestion, orchestration, transformation, and analysis.

## Project Steps

### Step 1: Data Ingestion into PostgreSQL

**Download the Dataset:**
- The Brazilian E-Commerce dataset was downloaded from Kaggle.

**Setup PostgreSQL Database:**
- PostgreSQL was set up using Docker and Docker Compose.
- A new database named `ecommerce` was created.

**Create Tables:**
- Tables were created in the PostgreSQL database corresponding to each CSV file in the dataset.

**Ingest Data:**
- Data was ingested into the tables using custom Python ETL scripts.

### Step 2: Setting up Apache Airflow

**Install Airflow:**
- Airflow was added to the Docker Compose setup.

**Create Airflow DAG:**
- A Directed Acyclic Graph (DAG) was created in Airflow to orchestrate the ETL process.
- The DAG includes tasks to extract data from PostgreSQL and load it into Google BigQuery.

### Step 3: Loading Data from PostgreSQL to BigQuery

**Setup Google BigQuery:**
- A new project was created in Google Cloud Platform (GCP).
- BigQuery API was enabled.
- A dataset was created in BigQuery to hold the e-commerce data.

**Load Data Using Airflow:**
- Airflow operators were used to extract data from PostgreSQL, transform it if necessary, and load it into the BigQuery dataset.

### Step 4: Transforming and Modeling Data with dbt

**Setup dbt:**
- dbt was installed and a new dbt project was initialized.

**Configure dbt:**
- dbt was configured to connect to the BigQuery dataset.

**Create Models:**
- dbt models were created to transform the raw data into a clean and usable format.

### Step 5: Answering Analytical Questions

Based on the domain knowledge of the Brazilian E-Commerce dataset, the following analytical questions were addressed:

1. **Which product categories have the highest sales?**
   - Data was modeled to aggregate sales by product category.

2. **What is the average delivery time for orders?**
   - Data was modeled to calculate the time difference between order purchase and delivery.

3. **Which states have the highest number of orders?**
   - Data was modeled to count the number of orders per state.

### Data Modeling with dbt

**dbt Models:**

**Staging Models:**
- `stg_orders.sql`: Raw orders data with necessary joins.
- `stg_products.sql`: Raw product data.

**Intermediate Models:**
- `int_sales_by_category.sql`: Aggregated sales data by product category.
- `int_avg_delivery_time.sql`: Calculated average delivery time for each order.
- `int_orders_by_state.sql`: Count of orders per state.

**Final Models:**
- `fct_sales_by_category.sql`: Final sales by category model.
- `fct_avg_delivery_time.sql`: Final average delivery time model.
- `fct_orders_by_state.sql`: Final orders by state model.

### Example dbt Model: `int_sales_by_category.sql`

```sql
with sales as (
    select
        product_id,
        sum(order_items.price * order_items.quantity) as total_sales
    from
        {{ ref('stg_orders') }} as orders
    join
        {{ ref('stg_order_items') }} as order_items
    on
        orders.order_id = order_items.order_id
    group by
        product_id
)

select
    products.category,
    sum(sales.total_sales) as total_sales
from
    sales
join
    {{ ref('stg_products') }} as products
on
    sales.product_id = products.product_id
group by
    products.category
