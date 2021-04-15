import sys
import traceback

from adapters import db
from services import utils

if __name__ == "__main__":
    try:
        print(" #### Start program #### ")
        
        print("Checking internal database ... ")
        db.InternalDB.initialise_internal_db()

        utils.Utils.analyze_entities()
        print(" #### Analysis done #### ")
    except:
        traceback.print_exc()
        sys.exit(1)
        

    
        