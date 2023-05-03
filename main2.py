# Import required libraries
import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np

# Define start and end points of a line
LINE_START = sv.Point(320, 0)
LINE_END = sv.Point(320, 480)

# Define main function
def main():
    # Create a line zone object
    line_counter = sv.LineZone(start=LINE_START, end=LINE_END)
    
    # Create a line zone annotator object
    line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=1, text_scale=0.5)
    
    # Create a box annotator object
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
    )

    # Load YOLO model
    model = YOLO("yolov8l.pt")

    # Loop through video frames
    for result in model.track(source=0, show=True, stream=True, agnostic_nms=True):
        # Get original image from YOLO result
        frame = result.orig_img
        
        # Convert YOLO detections to supervisely format
        detections = sv.Detections.from_yolov8(result)

        # Add tracker IDs to detections
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        # Filter out all objects except for people, cars, trucks, bikes and motorbikes.
        detections = detections[(detections.class_id == 0) | (detections.class_id == 1)|(detections.class_id == 2)|(detections.class_id == 3)|(detections.class_id == 7)]

        # Generate labels for the detected objects
        labels = [
            f"{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, tracker_id
            in detections
        ]

        # Annotate bounding boxes on the original frame
        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        # Trigger line crossing event
        line_counter.trigger(detections=detections)

        # Annotate line counter on the original frame
        line_annotator.annotate(frame=frame, line_counter=line_counter)

        # Display annotated frame
        cv2.imshow("yolov8", frame)

        # Break out of the loop when ESC key is pressed
        if (cv2.waitKey(30) == 27):
            break

# Run the main function if this script is being run directly
if __name__ == "__main__":
    main()

