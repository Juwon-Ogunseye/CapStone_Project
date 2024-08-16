from dotenv import load_dotenv
import psycopg2
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
from google.api_core.exceptions import NotFound
import logging
import json
import constant

def fetch_data_from_postgres(table_name):
    # Define your database connection URL
    DATABASE_URL = 'postgresql://airflow:airflow@postgres:5432/airflow'
    
    # Connect to the database using psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    
    # Define your SQL query
    query = f"SELECT * FROM {table_name}"
    
    # Fetch data into a pandas DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Close the connection
    conn.close()
    
    # Display the DataFrame
    print(df)
    
    return df

# Set project and dataset details
project_id = constant.PROJECT_ID
dataset_id = constant.DATASET_ID
table_id = constant.TABLE_ID
load_dotenv()
def create_dataset(client: bigquery.Client, project_id: str, dataset_id: str) -> None:
    dataset_ref = client.dataset(dataset_id)
    try:
        dataset = client.get_dataset(dataset_ref)
        logging.info(f"Dataset {dataset_id} already exists.")
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = client.create_dataset(dataset)
        logging.info(f"Created dataset {dataset_id}.")