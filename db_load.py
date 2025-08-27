from dotenv import load_dotenv
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import os

from utils import print_and_log, deco_print_and_log

# Load environment variables
load_dotenv()

project_id = os.environ.get("PROJECT_ID")


@deco_print_and_log("Loading BigQuery table")
def load_table_data(df, table_id):

    print_and_log(f"Loading table {table_id}")
    try:
        # Initialize BigQuery:
        client = bigquery.Client(project=project_id)

        # Load Dataframe to BigQuery:
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            autodetect=True
        )
        client.load_table_from_dataframe(df, table_id, job_config=job_config)

    except GoogleAPIError as e:
        print_and_log(f"Error loading into table {table_id}: {e}")
