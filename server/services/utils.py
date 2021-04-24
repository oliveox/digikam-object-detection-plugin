import os
import traceback

from adapters import db, digikam
from config import INTERNAL_DIGIKAM_ALBUM_FOLDER, INTERNAL_DIGIKAM_DB_PATH, REDIS_TOTAL_TO_ANALYSE, REDIS_ANALYSED_COUNT, REDIS_INSTANCE, REDIS_ANALYSIS_MESSAGE


class Utils:

    @classmethod
    def get_not_analyzed_entities(cls):
        
        # get all internal db external image ids
        all_external_ids = db.InternalDB.get_all_external_ids()

        # get all digikam image ids
        all_image_ids = digikam.DigiKamAdapter.get_all_image_ids()

        # get list difference
        to_analyse_entity_ids = list(set(all_image_ids) - set(all_external_ids))

        # get entities to be analyzed
        not_analyzed_entities = digikam.DigiKamAdapter.get_imported_entities_with_specific_ids(to_analyse_entity_ids)

        return not_analyzed_entities

    @classmethod
    def analyze_entities(cls):
        tags_root_pid = digikam.DigiKamAdapter.insert_tag(0, "objects")

        REDIS_INSTANCE.set(REDIS_ANALYSIS_MESSAGE, "Fetching not yet analysed entities")
        not_yet_analyzed_entities = cls.get_not_analyzed_entities()

        if len(not_yet_analyzed_entities) > 0:
            REDIS_INSTANCE.set(REDIS_TOTAL_TO_ANALYSE, "{}".format(len(not_yet_analyzed_entities)))

            # this import initializes Tensorflow, takes a lot of time, thats why its here
            from services import object_detection

            # detect all objects
            for index, row in enumerate(not_yet_analyzed_entities):
                REDIS_INSTANCE.set(REDIS_ANALYSED_COUNT, "{}".format(index))

                row_id = row[0]
                
                row_path = row[1]
                counter = 0
                for c in row_path:
                    if c == "/":
                        counter+=1
                    else:
                        break
                file_path = os.path.join(INTERNAL_DIGIKAM_ALBUM_FOLDER,row[1][counter:])
                REDIS_INSTANCE.set(REDIS_ANALYSIS_MESSAGE, "Analysing file: {}".format(file_path))

                file_hash = row[2]

                try:
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

            REDIS_INSTANCE.set(REDIS_ANALYSIS_MESSAGE, "Analysis ended")
        else:
            print("All Digikam imported entities are already analyzed")
            REDIS_INSTANCE.set(REDIS_ANALYSIS_MESSAGE, "All Digikam imported entities are already analyzed")

        return 0

if __name__ == "__main__":
    result = Utils.get_not_analyzed_entities()
