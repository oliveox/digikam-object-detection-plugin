from imageai.Detection import ObjectDetection, VideoObjectDetection
import cv2
import os

executionPath = os.getcwd()

class ObjectDetector:

    image_detector = None

    @classmethod
    def get_object_in_image(cls, file_path):

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
