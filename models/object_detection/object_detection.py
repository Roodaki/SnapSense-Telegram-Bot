import os
import torch
import asyncio
from pathlib import Path
from collections import Counter
from typing import Dict, Any
from ultralytics import YOLO
from bot.strings import Strings


def initialize_model(config: Dict[str, Any]) -> Dict[str, Any]:
    try:
        model_path = Path(config["model_path"])

        if not model_path.exists():
            raise FileNotFoundError(Strings.FILE_ERROR)

        device_str = config.get(
            "preferred_device", "cuda" if torch.cuda.is_available() else "cpu"
        )
        half_precision = config.get("half_precision", device_str == "cuda")

        model = YOLO(model_path)
        return {
            "model": model,
            "device": device_str,
            "half": half_precision,
            "model_name": Strings.MODEL_NAMES["object_detection"],
        }
    except Exception as e:
        raise RuntimeError(Strings.MODEL_INIT_ERROR.format("object detection")) from e


async def process_image(
    original_path: str,
    output_folder: str,
    image_id: str,
    model_data: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    try:
        detection_folder = Path(output_folder) / "object_detection"
        detection_folder.mkdir(exist_ok=True)

        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: model_data["model"](
                original_path,
                conf=config["conf"],
                iou=config["iou"],
                augment=config["augment"],
                device=model_data["device"],
                half=model_data["half"],
                save=config["save_result"],
                project=str(output_folder),
                name="object_detection",
                exist_ok=True,
            ),
        )

        return await _format_results(results[0], model_data)
    except Exception as e:
        raise RuntimeError(Strings.PROCESSING_ERROR.format("object detection")) from e


async def _format_results(result, model_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        class_counts = Counter(result.names[int(cls)] for cls in result.boxes.cls)
        detection_lines = [
            Strings.OBJECT_DETECTION_LINE.format(name, count)
            for name, count in class_counts.items()
        ]
        detection_summary = (
            "\n".join(detection_lines) if detection_lines else Strings.NO_OBJECTS
        )

        speed = result.speed
        speed_summary = Strings.format_speed_stats(
            preprocess=speed["preprocess"],
            inference=speed["inference"],
            postprocess=speed["postprocess"],
        )

        processed_path = Path(result.save_dir) / Path(result.path).name
        if not processed_path.exists():
            raise FileNotFoundError(Strings.FILE_ERROR)

        return {
            "image_path": str(processed_path),
            "detection_summary": detection_summary,
            "speed_summary": speed_summary,
            "model_name": model_data["model_name"],
        }
    except Exception as e:
        raise RuntimeError(Strings.RESULT_FORMAT_ERROR) from e
