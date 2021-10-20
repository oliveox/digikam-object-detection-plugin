from services.utils import Utils
from adapters.db import InternalDB
import traceback


if __name__ == "__main__":
    try:
        #initialise environment
        InternalDB.initialise_internal_db()

        # start analysis
        Utils.analyze_entities()
    except Exception as e:
        print(f'Analysis failed. Exception: {e}')