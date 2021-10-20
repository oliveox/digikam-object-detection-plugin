import os
import traceback
import torch

from adapters import db, digikam
from config import DIGIKAM_ALBUM_FOLDER
from services.object_detection import ObjectDetector

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

        not_yet_analyzed_entities = cls.get_not_analyzed_entities()
        if not len(not_yet_analyzed_entities) > 0:
            print("All Digikam imported entities are already analyzed")
            return 0
        
        model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

        # detect all objects
        for _ , row in enumerate(not_yet_analyzed_entities):

            row_id = row[0]
            
            row_path = row[1]
            counter = 0
            for c in row_path:
                if c == "/":
                    counter+=1
                else:
                    break
            file_path = os.path.join(DIGIKAM_ALBUM_FOLDER,row[1][counter:])

            file_hash = row[2]

            try:
                objects = ObjectDetector.get_objects_in_image(model, file_path)

                # save to internal db
                id = db.InternalDB.insert_image_objects(row_id, file_hash, objects)

                print("################################")
                print(f'Inserted [{file_path}] in database!"')

                if not len(objects) > 0:
                    print("Invalid file or couldn't detect any objects. Skipping it ... ")

                # using 'set' collection because same objects can appear multiple times 
                # in the same image
                for obj in set(objects): 
                    try:
                        # create digikam tag
                        tag_id = digikam.DigiKamAdapter.insert_tag(tags_root_pid, obj)

                        # create association
                        image_tag_id = digikam.DigiKamAdapter.insert_image_tag(row_id, tag_id)
                    except Exception as e:    
                        print(f'Error while persisting object [{obj}] for file {file_path}')
                        traceback.print_exc()

                digikam.DigiKamAdapter.close_db_connection()

                print(f'File path: [{file_path}]')
                print(f'Objects: [{", ".join(objects)}]')
                
            except Exception as e:
                print(f'Error while analysing filepath: [{file_path}]. Exception: [{e}]')
                traceback.print_exc()
            finally:
                print("################################")

        return 0

if __name__ == "__main__":
    result = Utils.get_not_analyzed_entities()
