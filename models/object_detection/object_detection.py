import os
import torch
import asyncio
from pathlib import Path
from collections import Counter
from ultralytics import YOLO
from typing import Dict, Any


def initialize_model() -> Dict[str, Any]:
    """Initialize model once during startup"""
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_path = Path("./models/object_detection/yolo11x.pt")

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")

        model = YOLO(model_path)
        return {
            "model": model,
            "device": device,
            "half": device == "cuda",
            "model_name": "YOLOv11x",
        }
    except Exception as e:
        raise RuntimeError(f"Model initialization failed: {e}") from e


async def process_image(
    original_path: str, output_folder: str, image_id: str, model_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Process image with proper async handling"""
    try:
        detection_folder = Path(output_folder) / "object_detection"
        detection_folder.mkdir(exist_ok=True)

        # Run inference in executor
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: model_data["model"](
                original_path,
                conf=0.3,
                iou=0.4,
                augment=True,
                device=model_data["device"],
                half=model_data["half"],
                save=True,
                project=str(output_folder),
                name="object_detection",
                exist_ok=True,
            ),
        )

        result = results[0]
        return await _format_results(result, model_data)

    except Exception as e:
        raise RuntimeError(f"Image processing failed: {e}") from e


async def _format_results(result, model_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format detection results"""
    try:
        # Detection summary
        class_counts = Counter(result.names[int(cls)] for cls in result.boxes.cls)
        detection_summary = (
            "\n".join(f"🔹 {name}: {count}" for name, count in class_counts.items())
            if class_counts
            else "No objects detected."
        )

        # Speed statistics
        speed = result.speed
        speed_summary = (
            f"⚙️ *Speed Stats (ms)*\n"
            f"• Preprocessing: `{speed['preprocess']:.2f}`\n"
            f"• Inference: `{speed['inference']:.2f}`\n"
            f"• Postprocessing: `{speed['postprocess']:.2f}`"
        )

        # Path handling with validation
        processed_path = Path(result.save_dir) / Path(result.path).name
        if not processed_path.exists():
            raise FileNotFoundError(f"Processed image not found at {processed_path}")

        return {
            "image_path": str(processed_path),
            "detection_summary": detection_summary,
            "speed_summary": speed_summary,
            "model_name": model_data["model_name"],
        }

    except AttributeError as e:
        raise RuntimeError(f"Result formatting error: {e}") from e
    except KeyError as e:
        raise RuntimeError(f"Missing expected result data: {e}") from e
