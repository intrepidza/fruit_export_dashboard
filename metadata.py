from google.cloud import bigquery

# from google.cloud.exceptions import GoogleCloudError
from google.api_core.exceptions import GoogleAPIError

from dotenv import load_dotenv
# import os

from utils import print_and_log, deco_print_and_log

# Load environment variables
# load_dotenv()


@deco_print_and_log("Creating dataset and table")
def create_dataset_and_table(project_id, dataset_id, table_id):
    try:
        # Initialize BigQuery:
        client = bigquery.Client(project=project_id)

        # Define dataset:
        dataset_ref = client.dataset(dataset_id)

        # Create dataset:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset = client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {dataset_id} created or already exists.")

        # Define schema:
        # schema = [
        #     bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
        #     bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
        #     bigquery.SchemaField("hs_code", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("hs_description", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("chapter_and_description", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("country_of_origin", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("country_of_origin_name", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("destination_country", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("destination_country_name", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("world_region", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("transport_code_description", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("unit", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("district_office_code", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("district_office_name", "STRING", mode="REQUIRED"),
        #     bigquery.SchemaField("value", "NUMERIC", mode="REQUIRED"),
        #     bigquery.SchemaField("quantity", "NUMERIC", mode="REQUIRED"),
        #     bigquery.SchemaField("created_at", "TIMESTAMP", mode="NULLABLE"),
        # ]

        schema = [
            bigquery.SchemaField('trade_type', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('district_office_code', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('district_office_name', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('country_of_origin', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('country_of_origin_name', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('country_of_destination', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('country_of_destination_name', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('tariff', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('statistical_unit', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('transport_code', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('transport_code_description', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('year_month', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('calendar_year', 'INT64', mode='REQUIRED'),
            bigquery.SchemaField('section', 'INT64', mode='REQUIRED'),
            bigquery.SchemaField('section_and_description', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('chapter', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('chapter_and_description', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('tariff_and_description', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('statistical_quantity', 'FLOAT64', mode='REQUIRED'),
            bigquery.SchemaField('customs_value', 'FLOAT64', mode='REQUIRED'),
            bigquery.SchemaField('world_region', 'STRING', mode='REQUIRED'),
        ]

        # Define table reference:
        table_ref = dataset_ref.table(table_id)

        # Create table:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table, exists_ok=True)
        print_and_log(f"Table {table_id} created or already exists in dataset {dataset_id}.")

    except GoogleAPIError as e:
        print_and_log(f"An error occurred: {e}")
        raise
