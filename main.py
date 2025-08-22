from connections import upload_file
from pathlib import Path
from dotenv import load_dotenv
import os

from tools import print_and_log, deco_print_and_log

load_dotenv()

local_path = Path(os.environ.get("LOCAL_PATH"))


@deco_print_and_log('APP')
def main():
    
    # Run function for all files in upload folder:
    [upload_file(x.name) for x in local_path.iterdir()]


if __name__ == '__main__':
    main()
