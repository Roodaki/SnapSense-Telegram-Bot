import os
from ultralytics import YOLO


async def process_image(original_image_path, image_folder, image_id):
    # Create a subfolder for object detection results
    detection_folder = os.path.join(image_folder, "object_detection")
    os.makedirs(detection_folder, exist_ok=True)

    # Define where the processed image will be saved
    processed_image_path = os.path.join(detection_folder, f"{image_id}.jpg")

    # Load the YOLO model (you can cache it if needed)
    model = YOLO("./models/object_detection/yolo11x.pt")

    # Run object detection
    model(
        original_image_path,
        conf=0.3,
        iou=0.4,
        augment=True,
        device="cuda",
        imgsz=640,
        half=True,
        save=True,
        project=image_folder,  # The image folder as base
        name="object_detection",  # Subfolder name for object detection results
        exist_ok=True,
    )

    # Find the saved output image
    saved_images = [
        fname for fname in os.listdir(detection_folder) if fname.endswith(".jpg")
    ]
    if saved_images:
        processed_image_path = os.path.join(detection_folder, saved_images[0])
    else:
        raise Exception("No processed image was found after running detection.")

    return processed_image_path
