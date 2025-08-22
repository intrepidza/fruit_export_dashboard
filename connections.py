from google.cloud import storage
from dotenv import load_dotenv
import os

from tools import print_and_log, deco_print_and_log

# Load environment variables from .env file
load_dotenv()

local_path = os.environ.get("LOCAL_PATH")
bucket_name = os.environ.get("BUCKET_NAME")

@deco_print_and_log('Upload files')
def upload_file(source_file_name, bucket_name=bucket_name, local_path=local_path):
    """Check if file exists and upload to GCP bucket."""
    full_path = local_path + '\\' + source_file_name
    destination_prefix = 'fruit_project/Datasets'
    destination_blob_name = destination_prefix + '/' + source_file_name

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Construct list of names to check if file exists
    blob_list = [os.path.basename(blob.name) for blob in bucket.list_blobs(prefix='fruit_project/Datasets')]

    if source_file_name in blob_list:
        print(f"File {source_file_name} already exists in destination bucket {bucket_name}.")
        return

    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_filename(full_path)
        print(f"File {source_file_name} uploaded to destination bucket {bucket_name}.")
    except Exception as e:
        print_and_log(f"Error when uploading file/s: {e}")
