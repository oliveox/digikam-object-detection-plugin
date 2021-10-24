import json
import filetype
import cv2

from config import VIDEO_FRAME_STEP, SUPPORTED_FILE_TYPES

class ObjectDetector:

    @classmethod
    def get_objects_in_file(cls, model, file_path):

        try:
            kind = filetype.guess(file_path)
        except FileNotFoundError as e:
            # file doesn't exist - TODO - fix support for multiple media collections
            print(f"File [{file_path}] doesn't exist. Check album folder validity.")
            return []
        except Exception as e:
            print(f'Unexpected error while getting file type of [{file_path}]')
            raise e

        if (kind.mime.startswith(SUPPORTED_FILE_TYPES.IMAGE)):
            # print(f'Analysing [image]')
            return cls.get_objects_in_image(model, file_path)
        elif (kind.mime.startswith(SUPPORTED_FILE_TYPES.VIDEO)):
            # print(f'Analysing [video]')
            cap=cv2.VideoCapture(file_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            objects = []
            # sample_rate = total_frames / 1
            for fno in range(0, total_frames, VIDEO_FRAME_STEP):
                cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
                _, image = cap.read()

                objects.extend(cls.get_objects_in_image(model, image))

            return set(objects)
        else:
            print(f'Unsupported type [{kind.mime}]. File: [{file_path}]')

    @classmethod
    def get_objects_in_image(cls, model, image):
        # image can be filepath or a frame

        results = model(image)            

        if results is None:
            print(f'Could not fetch objects for {image}')
            return []
        
        json_data = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
        return list(set(map(lambda x: x["name"], json_data)))
