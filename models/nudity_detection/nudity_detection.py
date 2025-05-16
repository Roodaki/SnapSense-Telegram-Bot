import asyncio
from pathlib import Path
from typing import Dict, Any
from nudenet import NudeDetector
from bot.strings import Strings


def initialize_detector() -> NudeDetector:
    try:
        return NudeDetector()
    except Exception as e:
        raise RuntimeError(Strings.MODEL_INIT_ERROR.format("nudity detection")) from e


async def process_image(
    original_path: str,
    output_folder: str,
    image_id: str,
    detector: NudeDetector,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    try:
        detection_folder = Path(output_folder) / "nudity_detection"
        detection_folder.mkdir(exist_ok=True)
        censored_path = detection_folder / f"censored_{image_id}.jpg"
        nudity_classes = config["nudity_classes"]

        loop = asyncio.get_event_loop()
        detections = await loop.run_in_executor(
            None, lambda: detector.detect(original_path)
        )

        await loop.run_in_executor(
            None,
            lambda: detector.censor(
                original_path,
                output_path=str(censored_path),
                classes=nudity_classes,
            ),
        )

        detected_classes = {
            d["class"] for d in detections if d["class"] in nudity_classes
        }
        detection_summary = (
            Strings.NUDITY_DETECTED.format("\n• ".join(detected_classes))
            if detected_classes
            else Strings.NO_NUDITY
        )

        return {
            "image_path": str(censored_path),
            "detection_summary": detection_summary,
            "model_name": Strings.MODEL_NAMES["nudity_detection"],
        }
    except Exception as e:
        raise RuntimeError(Strings.PROCESSING_ERROR.format("nudity detection")) from e
