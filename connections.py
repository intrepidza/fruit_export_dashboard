from google.cloud import storage
from dotenv import load_dotenv
import os

from utils import print_and_log, deco_print_and_log

# Load environment variables from .env file
load_dotenv()

upload_path = os.environ.get("LOCAL_PATH") or ""
bucket_name = os.environ.get("BUCKET_NAME")

@deco_print_and_log('Upload files')
def upload_file(source_file_name, bucket_name=bucket_name, local_path=upload_path):
    """Check if file exists and upload to GCP bucket."""
    date_part = source_file_name.split('.')[0][-4:]     # Extract Year from file
    full_path = local_path + '\\' + source_file_name
    destination_prefix = f'fruit_project/Datasets/exports/{date_part}'
    destination_blob_name = destination_prefix + '/' + source_file_name

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Construct list of names to check if file exists
    blob_list = [os.path.basename(blob.name) for blob in bucket.list_blobs(prefix='fruit_project/Datasets')]
    
    if source_file_name in blob_list:
        print_and_log(f"File {source_file_name} already exists in destination bucket {bucket_name}.")
        return

    blob = bucket.blob(destination_blob_name)

    try:
        print_and_log(f"Uploading {source_file_name} to: {full_path}...")
        blob.upload_from_filename(full_path)
        print_and_log(f"File {source_file_name} uploaded to destination bucket {bucket_name}.")
    except Exception as e:
        print_and_log(f"Error when uploading file/s: {e}")
