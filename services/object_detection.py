from imageai.Detection import ObjectDetection
import os
import filetype

executionPath = os.getcwd()

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
    def get_object_in_image(cls, file_path):

        if cls.is_valid_file(file_path):
            if ObjectDetector.image_detector == None:
                print("Initialising object detector ... ")
                ObjectDetector.image_detector = ObjectDetector.initialise_image_detector()

            detections = ObjectDetector.image_detector.detectObjectsFromImage(
                input_image=file_path, 
                output_image_path=os.path.join(executionPath, "media", "result.jpg"), 
                minimum_percentage_probability=30
            )
            
            objects = list(map(lambda x: x["name"], detections))
            return objects
        else:
            return []

    @classmethod
    def initialise_image_detector(cls):
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join
                (executionPath, "models", "resnet50_coco_best_v2.1.0.h5"))
        detector.loadModel(detection_speed = "flash")

        return detector

if __name__ == "__main__":
    objects = ObjectDetector.get_object_in_image("/digikam/album/a.jpg")
    print('{}'.format(', '.join(objects)))
