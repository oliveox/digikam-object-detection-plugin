import json
import os
import filetype

class ObjectDetector:

    image_detector = None

    def is_valid_file(file_path):
        kind = filetype.guess(file_path)
        
        if kind is None:
            return False
        
        if kind.mime.startswith("image/"):
            return True
        else: 
            return False


    @classmethod
    def get_objects_in_image(cls, model, file_path):

        if cls.is_valid_file(file_path):
            results = model(file_path)            

            if results is None:
                print(f'Could not fetch objects for {file_path}')
                return []
            
            json_data = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
            return list(set(map(lambda x: x["name"], json_data)))
        else:
            return []
