from google.cloud import storage

from dotenv import load_dotenv
from io import BytesIO
import os
import pandas as pd

from utils import print_and_log, deco_print_and_log

# Load environment variables from .env file
load_dotenv()


upload_path = os.environ.get("LOCAL_PATH") or ""
bucket_name = os.environ.get("BUCKET_NAME")


@deco_print_and_log("Read and convert to DataFrame")
def read_file(file_name):
    print_and_log(f"Reading contents of file {file_name}")
    try:
        storage_client = storage.Client()     

        # Bucket and file:
        # file_path = f'fruit_project/Datasets/exports/2023/'

        bucket = storage_client.bucket(bucket_name)
        # blob = bucket.blob(file_path)

        blobs = bucket.list_blobs()

        blob = [blob for blob in blobs if blob.name.endswith(file_name)]

        if len(blob) != 1:
            print_and_log("Issue finding file.")

        data = blob[0].download_as_bytes()

        return pd.read_excel(BytesIO(data), na_filter=False).convert_dtypes()
    except Exception as e:
         print_and_log(f"Error while reading file as DataFrame: {e}")

    # return pd.read_excel(file_name, na_filter=False).convert_dtypes() # na_filter is important to not drop Namibia Country Code
    

@deco_print_and_log("Clean up DataFrame")
def clean_data(df):   
    # Normalize columns
    try:
        print_and_log("Normalizing column names")
        normalize_columns = []
        for x in df.columns:
            x = ''.join(['_' + y if y.isupper() else y for y in x]) # Add underscore infront of capital letters
            x = x.replace('_', '', 1)
            x = x.lower()
            normalize_columns.append(x)

        df.columns = normalize_columns
    except Exception as e:
        print_and_log(f"Error while normalizing column names: {e}")

    # Convert dtypes
    try:
        print_and_log("Converting dtypes")
        df['tariff'] = df['tariff'].astype('string')
        df['transport_code'] = df['transport_code'].astype('string')
        df['chapter'] = df['chapter'].astype('string')
        df['customs_value'] = df['customs_value'].astype('Float64')
    except Exception as e:
            print_and_log(f"Error while converting dtypes: {e}")

    return df
