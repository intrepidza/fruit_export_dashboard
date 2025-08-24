from connections import upload_file
from dotenv import load_dotenv
import os
from pathlib import Path

from metadata import create_dataset_and_table
from transform import read_file, clean_data
from utils import print_and_log, deco_print_and_log


load_dotenv()


upload_path = Path(os.environ.get("LOCAL_PATH") or "") 
project_id = os.environ.get('PROJECT_ID')


@deco_print_and_log('APP')
def main():
    # Create BigQuery metadata:

    dataset_id = 'raw_sars'         # Desired dataset name
    table_id = 'sars_export_data'   # Desired table name

    create_dataset_and_table(project_id, dataset_id, table_id)

    df = read_file(r'd:\_Projects\Python\fruit_export_dashboard\_datasets\Report_2023.xlsx')
    df_clean = clean_data(df)

    # print(df_clean)
    # print(df_clean.info())
    # df_clean.to_excel('temp.xlsx')

    # print(df_clean.to_string())

    # Run function for all files in upload folder:
    # [upload_file(x.name) for x in upload_path.iterdir()]


# dataset
# dwh_fruit_stats
# raw_sars_data

# Tables:

if __name__ == '__main__':
    main()
