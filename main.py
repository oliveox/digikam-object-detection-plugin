from adapters import digikam
from adapters import db
from services import utils
import os
import traceback

if __name__ == "__main__":

    print(" #### Start program #### ")

    tags_root_pid = digikam.DigiKamAdapter.insert_tag(0, "objects")
    not_yet_analyzed_entities = utils.Utils.get_not_analyzed_entities()

    # detect all objects
    for row in not_yet_analyzed_entities:
        row_id = row[0]
        
        row_path = row[1]
        counter = 0
        for c in row_path:
            if c == "/":
                counter+=1
            else:
                break
        file_path = os.path.join("/digikam/album",row[1][counter:])

        file_hash = row[2]

        # TODO catch errors 
        try:

            # this import initializes Tensorflow, takes a lot of time, thats why its here
            from services import object_detection
            objects = object_detection.ObjectDetector.get_objects_in_image(file_path)

            # save to internal db
            id = db.InternalDB.insert_image_objects(row_id, file_hash, objects)

            print("################################")
            print("Inserted [{file_path}] in database!".format(file_path=file_path))

            if len(objects) > 0:
                # set because same objects may appear multiple times in the same image
                for obj in set(objects): 
                    try:
                        # create digikam tag
                        tag_id = digikam.DigiKamAdapter.insert_tag(tags_root_pid, obj)

                        # create association
                        image_tag_id = digikam.DigiKamAdapter.insert_image_tag(row_id, tag_id)

                    except Exception as err:    
                        traceback.print_exc()

                digikam.DigiKamAdapter.close_db_connection()

                print("File path: [{}]".format(file_path))
                print('Objects: [{}]'.format(', '.join(objects)))
            
            else:
                print("Invalid file or couldn't detect any objects. Skipping it ... ")
        except Exception as err:
            print("Error on analysing filepath: [{}]".format(file_path))
            print("Error message: [{}]".format(err))
            traceback.print_exc()
        finally:
            print("################################")
    
    print(" #### Analysis done #### ")
        