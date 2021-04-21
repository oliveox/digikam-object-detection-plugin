# docker container relative paths
DIGIKAM_DB_PATH="/digikam/db/digikam4.db"
DIGIKAM_ALBUM_FOLDER= "/digikam/album"

REDIS_ANALYSED_COUNT="analysed_entities"
REDIS_TOTAL_TO_ANALYSE="to_analyse_entities"
REDIS_ANALYSIS_MESSAGE="analysis_message"

# TODO - maybe a smarter way to init only on usage
import redis
REDIS_INSTANCE=redis.Redis(charset="utf-8", decode_responses=True)