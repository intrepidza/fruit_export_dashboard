from dotenv import load_dotenv
from google.cloud import storage
from io import BytesIO
import os
import pandas as pd

from utils import print_and_log, deco_print_and_log

# Load environment variables from .env file
load_dotenv()


upload_path = os.environ.get("LOCAL_PATH") or ""
bucket_name = os.environ.get("BUCKET_NAME")


@deco_print_and_log("Read and convert GCP file to DataFrame")
def gcp_read_file(file_name, sheet_name, dtype_override={}):
    """Checks that file exists in bucket, reads it and returns a DataFrame."""

    print_and_log(f"Reading contents of file {file_name} in Google Cloud Storage")
    try:
        storage_client = storage.Client()     

        # Bucket and file:

        bucket = storage_client.bucket(bucket_name)

        blobs = bucket.list_blobs()

        blob = [blob for blob in blobs if blob.name.endswith(file_name)]

        if len(blob) != 1:
            print_and_log("Issue finding file.")

        data = blob[0].download_as_bytes()

        return pd.read_excel(BytesIO(data), sheet_name=sheet_name, dtype=dtype_override, na_filter=False).convert_dtypes()
    except Exception as e:
         print_and_log(f"Error while reading file as DataFrame: {e}")


@deco_print_and_log("Read and convert local file to DataFrame")
def local_read_file(file_name, sheet_name, dtype_override={}):
    """Reads local file and returns a DataFrame."""

    print_and_log(f"Reading contents of file {file_name} in local Storage")
    try:
        # Bucket and file:
        return pd.read_excel(file_name, sheet_name=sheet_name, dtype=dtype_override).convert_dtypes()
    except Exception as e:
         print_and_log(f"Error while reading file as DataFrame: {e}")


@deco_print_and_log("Clean up DataFrame")
def clean_data(df):
    """Normalizes column naming and converts data types"""
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
        df['transport_code'] = df['transport_code'].astype('string')
        df['year_month'] = df['year_month'].astype('string')
        df['chapter'] = df['chapter'].astype('string')
        df['customs_value'] = df['customs_value'].astype('Float64')
    except Exception as e:
            print_and_log(f"Error while converting dtypes: {e}")

    return df
