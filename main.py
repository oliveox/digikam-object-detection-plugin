from adapters import digikam
from services import object_detection
from adapters import db
from services import utils

import os

if __name__ == "__main__":
    tags_root_pid = digikam.DigiKamAdapter.insert_tag(0, "objects")
    all_entities_to_analyse = utils.Utils.get_entities_to_analyse()
    all_detected_objects = []

    # detect all objects
    for row in all_entities_to_analyse:
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
            objects = object_detection.ObjectDetector.get_object_in_image(file_path)

            # save to internal db
            id = db.InternalDB.insert_image_objects((row_id, file_hash, ' '.join(objects)))

            if len(objects) > 0:
                for obj in objects:

                    try:
                        # create digikam tag
                        tag_id = digikam.DigiKamAdapter.insert_tag(tags_root_pid, obj)

                        # create association
                        image_tag_id = digikam.DigiKamAdapter.insert_image_tag(row_id, tag_id)

                    except Exception as err:    
                        print("Error: {}".format(err))

                digikam.DigiKamAdapter.close_db_connection()

            print("################################")
            print("Inserted in database!")
            print("Image path: {}".format(file_path))
            print('Objects: {}'.format(', '.join(objects)))
            print("################################")
        except Exception as err:
            print("Error on analysing filepath: {}".format(file_path))
            print("Error message: {}".format(err))