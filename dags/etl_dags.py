from dotenv import load_dotenv
import os
from google.cloud import bigquery
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import pandas as pd
from functions import fetch_data_from_postgres, create_dataset
import logging
import json
import constant  # Import the constants

# Load environment variables from .env file
load_dotenv()

# Get the path to the Google Cloud credentials file from the environment variable
GOOGLE_AUTH_FILE = os.getenv('GOOGLE_AUTH_FILE')
if not GOOGLE_AUTH_FILE:
    raise ValueError("The environment variable GOOGLE_AUTH_FILE is not set.")

# Set up logging
logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

# Define defaults for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG('etl_dags',
         default_args=default_args,
         description='DAG using Postgres data',
         schedule_interval=timedelta(days=30),
         start_date=datetime(2023, 1, 1),
         catchup=False,
) as dag:

    @task
    def fetch_data_task(table_name):
        try:
            logger.info(f'Starting to fetch data from table: {table_name}')
            df = fetch_data_from_postgres(table_name)
            logger.info(f'Successfully fetched data from table: {table_name}')
            # Convert DataFrame to JSON string for XCom
            return df.to_json()
        except Exception as e:
            logger.error(f'Error fetching data from table: {table_name} - {e}')
            raise

    @task
    def upload_to_bigquery_task(df_json, table_id):
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_AUTH_FILE

            bigquery_client = bigquery.Client()

            create_dataset(bigquery_client, constant.PROJECT_ID, constant.DATASET_ID)

            table_ref = bigquery_client.dataset(constant.DATASET_ID).table(table_id)

            df = pd.read_json(df_json)

            # Convert DataFrame to BigQuery format and upload
            job = bigquery_client.load_table_from_dataframe(df, table_ref)
            job.result()  # Wait for the job to complete

            logger.info(f'Successfully uploaded data to BigQuery table: {table_id}')
        except Exception as e:
            logger.error(f'Error uploading data to BigQuery table: {table_id} - {e}')
            raise

    # Define task dependencies for multiple tables
    tables = [
        'olist_orders_dataset',
        'olist_customers_dataset',
        'olist_geolocation_dataset',
        'olist_order_items_dataset',
        'olist_order_payments_dataset',
        'olist_order_reviews_dataset',
        'olist_products_dataset',
        'olist_sellers_dataset',
        'product_category_name_translation'
    ]

    for table in tables:
        df_json = fetch_data_task(table)
        upload_to_bigquery_task(df_json, table)
