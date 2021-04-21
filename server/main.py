import sys
import traceback
import redis
import json
from flask import Flask
from flask_cors import CORS
from flask_executor import Executor

from adapters import db
from services import utils
from config import REDIS_ANALYSED_COUNT, REDIS_ANALYSIS_MESSAGE, REDIS_TOTAL_TO_ANALYSE, REDIS_INSTANCE

app = Flask(__name__)
app.config["EXECUTOR_TYPE"] = "process"
app.config["EXECUTOR_MAX_WORKERS"] = 1
CORS(app)

# TODO initialise only on requirment (specific routes?)
executor = Executor(app)
OBJECT_DETECTION_PROCESS_KEY='object_detection'
def close_executor(arg):
    executor.futures.pop(OBJECT_DETECTION_PROCESS_KEY)
executor.add_default_done_callback(close_executor)



@app.route('/start-analysis')
def index():

    if len(executor.futures._futures) > 0 \
        and not executor.futures.done(OBJECT_DETECTION_PROCESS_KEY):
        return "analysis already running"

    REDIS_INSTANCE.set(REDIS_ANALYSED_COUNT, "0")
    executor.submit_stored(OBJECT_DETECTION_PROCESS_KEY, utils.Utils.analyze_entities)
    return "analysis started"

@app.route('/get-result')
def get_result():

    message = REDIS_INSTANCE.get(REDIS_ANALYSIS_MESSAGE)
    if len(executor.futures._futures) > 0 \
        and not executor.futures.done(OBJECT_DETECTION_PROCESS_KEY):
        # TODO - verify if any futures have been submitted
        # return jsonify({'status': executor.futures._state(OBJECT_DETECTION_PROCESS_KEY)})
        analysed = REDIS_INSTANCE.get(REDIS_ANALYSED_COUNT)
        total_to_analyse = REDIS_INSTANCE.get(REDIS_TOTAL_TO_ANALYSE)
        return json_response({
            "status": executor.futures._state(OBJECT_DETECTION_PROCESS_KEY),
            "total_to_analyse": total_to_analyse,
            "analysed": analysed,
            "message": message
        })
    
    return json_response({
        "status": "DONE",
        "message": message
    })

def initialise_server():                                                                
    print("Starting server ... ")
    app.run()
    print("Server started")

def json_response(payload, status=200):
  return (json.dumps(payload), status, {'content-type': 'application/json'})

if __name__ == "__main__":
    try:
        print(" #### Start program #### ")
        
        print("Checking internal database ... ")
        db.InternalDB.initialise_internal_db()

        initialise_server()
    except:
        traceback.print_exc()
        sys.exit(1)    