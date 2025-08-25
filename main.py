from dotenv import load_dotenv
import os
from pathlib import Path

from file_upload import upload_file
from ingest import read_file, clean_data
from load import load_table_data
from metadata import create_dataset_and_table
from utils import print_and_log, deco_print_and_log

load_dotenv()

upload_path = Path(os.environ.get("LOCAL_PATH") or "") 
project_id = os.environ.get('PROJECT_ID')

print("-----==========-----")
@deco_print_and_log('APP')
def main():
    # Run function for all files in upload folder:
    # [upload_file(x.name) for x in upload_path.iterdir()]

    # Create BigQuery metadata:
    dataset_id = 'fruit_export'     # Desired dataset name
    table_id = 'sars_export_data'   # Desired table name

    create_dataset_and_table(project_id, dataset_id, table_id)

    # Read excel file into DataFrame and clean it:
    #### df = read_file(r'd:\_Projects\Python\fruit_export_dashboard\_datasets\Report_2023.xlsx') # Read from local machine
    df = read_file('Report_2023.xlsx')  # Read from Cloud Storage

    df_clean = clean_data(df)

    # Load DataFrame into BigQuery table:
    dest_table_id = 'trepz-gcp-data-eng.fruit_export.sars_export_data'

    load_table_data(df_clean, dest_table_id)


# dataset
# dwh_fruit_stats
# raw_sars_data

# Tables:

if __name__ == '__main__':
    main()
