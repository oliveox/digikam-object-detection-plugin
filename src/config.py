import os
from dotenv import load_dotenv
load_dotenv()

DIGIKAM_DB_PATH=os.getenv("DIGIKAM_DB_PATH")
DIGIKAM_ALBUM_FOLDER=os.getenv("DIGIKAM_ALBUM_FOLDER")
PLUGIN_DB_PATH=os.getenv("PLUGIN_DB_PATH")