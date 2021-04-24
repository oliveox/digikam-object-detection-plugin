import os

# docker container relative paths

INTERNAL_DIGIKAM_DB_PATH=os.getenv("INTERNAL_DIGIKAM_DB_PATH")
INTERNAL_DIGIKAM_ALBUM_FOLDER=os.getenv("INTERNAL_DIGIKAM_ALBUM_FOLDER")

REDIS_ANALYSED_COUNT="analysed_entities"
REDIS_TOTAL_TO_ANALYSE="to_analyse_entities"
REDIS_ANALYSIS_MESSAGE="analysis_message"

# TODO - maybe a smarter way to init only on usage
import redis
REDIS_INSTANCE=redis.Redis(charset="utf-8", decode_responses=True)