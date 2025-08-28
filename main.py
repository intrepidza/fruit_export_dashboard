from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd

from load_db import load_table_data
from file_upload import upload_file
from load_file import gcp_read_file, local_read_file, clean_data
from metadata import create_dataset_and_table, schemas
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

    # # Create initial dataset and raw table:
    create_dataset_and_table(project_id, dataset_id, table_id, schemas[0][table_id])
  
    final_df = pd.DataFrame()
    # Read excel files into DataFrame, clean it and load into table:
    for file in ['Report_2023.xlsx', 'Report_2024.xlsx', 'Report_2025.xlsx']:
        df = gcp_read_file(file, 0, {'Tariff': str})  # Read from Cloud Storage
        df_clean = clean_data(df)

        final_df = pd.concat([final_df, df_clean], ignore_index=True)

    dest_table_id = f'trepz-gcp-data-eng.{dataset_id}.{table_id}'
    load_table_data(final_df, dest_table_id, "WRITE_TRUNCATE")

    # Once-off Lookup table creation and upload:
    lkp_table_id = 'lkp_hs_code_data'
    create_dataset_and_table(project_id, dataset_id, lkp_table_id, schemas[0][lkp_table_id])
    
    df_lkp = local_read_file('.\\_documents\\hs_codes_formatted.xlsx', "final", {'hs_code': str})
    dest_lkp_table_id = f'trepz-gcp-data-eng.{dataset_id}.{lkp_table_id}'
    load_table_data(df_lkp, dest_lkp_table_id, "WRITE_TRUNCATE")


if __name__ == '__main__':
    main()
