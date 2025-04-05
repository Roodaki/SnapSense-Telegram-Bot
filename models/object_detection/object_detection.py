import os
from collections import Counter
from ultralytics import YOLO


async def process_image(original_image_path, image_folder, image_id):
    # Create a subfolder for object detection results
    detection_folder = os.path.join(image_folder, "object_detection")
    os.makedirs(detection_folder, exist_ok=True)

    # Load the YOLO model (consider caching outside for performance)
    model = YOLO("./models/object_detection/yolo11x.pt")

    # Run object detection and get results
    results = model(
        original_image_path,
        conf=0.3,
        iou=0.4,
        augment=True,
        device="cuda",
        imgsz=640,
        half=True,
        save=True,
        project=image_folder,
        name="object_detection",
        exist_ok=True,
    )

    result = results[0]

    # Extract detected class names
    class_ids = result.boxes.cls.tolist() if result.boxes is not None else []
    class_names = [model.names[int(cls_id)] for cls_id in class_ids]
    class_counts = Counter(class_names)

    # Format detected classes
    detection_summary = (
        "\n".join([f"🔹 {name}: {count}" for name, count in class_counts.items()])
        if class_counts
        else "No objects detected."
    )

    # Extract speed stats (in milliseconds)
    speed_stats = (
        result.speed
    )  # dict with keys: 'preprocess', 'inference', 'postprocess'

    # Format speed info
    speed_summary = (
        f"⚙️ *Speed Stats (ms)*\n"
        f"• Preprocessing: `{speed_stats['preprocess']:.2f}`\n"
        f"• Inference: `{speed_stats['inference']:.2f}`\n"
        f"• Postprocessing: `{speed_stats['postprocess']:.2f}`"
    )

    # Locate the saved processed image
    saved_images = [
        fname for fname in os.listdir(detection_folder) if fname.endswith(".jpg")
    ]
    if not saved_images:
        raise Exception("No processed image was found after running detection.")

    processed_image_path = os.path.join(detection_folder, saved_images[0])

    return {
        "image_path": processed_image_path,
        "detection_summary": detection_summary,
        "speed_summary": speed_summary,
    }
