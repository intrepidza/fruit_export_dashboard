from dotenv import load_dotenv
import os
from pathlib import Path

from db_load import load_table_data
from file_upload import upload_file
from ingestion import read_file, clean_data
from metadata import create_dataset_and_table
from utils import deco_print_and_log

load_dotenv()

upload_path = Path(os.environ.get("LOCAL_PATH") or "") 
project_id = os.environ.get('PROJECT_ID')

print("-----==========-----")
@deco_print_and_log('APP')
def main():
    # Run function for all files in upload folder:
    [upload_file(x.name) for x in upload_path.iterdir()]

    # Create BigQuery metadata:
    dataset_id = 'fruit_export'     # Desired dataset name
    table_id = 'raw_sars_export_data'   # Desired table name

    # Create initial dataset and raw table:
    create_dataset_and_table(project_id, dataset_id, table_id)

    #### df = read_file(r'd:\_Projects\Python\fruit_export_dashboard\_datasets\Report_2023.xlsx') # Read from local machine
    
    # Read excel file into DataFrame, clean it and load into table:
    for file in ['Report_2023.xlsx', 'Report_2024.xlsx', 'Report_2025.xlsx']:
        df = read_file(file)  # Read from Cloud Storage
        df_clean = clean_data(df)

        dest_table_id = f'trepz-gcp-data-eng.{dataset_id}.{table_id}'
        load_table_data(df_clean, dest_table_id)


if __name__ == '__main__':
    main()
