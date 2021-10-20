import os
from dotenv import load_dotenv
load_dotenv()

DIGIKAM_DB_PATH=os.getenv("INTERNAL_DIGIKAM_DB_PATH")
DIGIKAM_ALBUM_FOLDER=os.getenv("INTERNAL_DIGIKAM_ALBUM_FOLDER")
PLUGIN_DB_PATH=os.getenv("PLUGIN_DB_PATH")