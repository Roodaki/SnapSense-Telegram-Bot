import os
import asyncio
from pathlib import Path
from typing import Dict, Any
from nudenet import NudeDetector


def initialize_detector() -> NudeDetector:
    """Initialize NudeNet detector once during startup"""
    try:
        return NudeDetector()
    except Exception as e:
        raise RuntimeError(f"Nudity detector initialization failed: {e}") from e


async def process_image(
    original_path: str, output_folder: str, image_id: str, detector: NudeDetector
) -> Dict[str, Any]:
    """Process image for nudity detection and censorship"""
    try:
        detection_folder = Path(output_folder) / "nudity_detection"
        detection_folder.mkdir(exist_ok=True)

        # Generate output paths
        censored_path = detection_folder / f"censored_{image_id}.jpg"

        # Define classes to censor
        censor_classes = [
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "FEET_EXPOSED",
            "ARMPITS_EXPOSED",
            "BELLY_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
        ]

        # Run detection and censorship in executor
        loop = asyncio.get_event_loop()
        detections = await loop.run_in_executor(
            None, lambda: detector.detect(original_path)
        )

        await loop.run_in_executor(
            None,
            lambda: detector.censor(
                original_path, output_path=str(censored_path), classes=censor_classes
            ),
        )

        # Format detection summary
        detected_classes = {d["class"] for d in detections}
        detection_summary = (
            "🚫 Detected sensitive content:\n"
            + "\n".join(f"• {cls}" for cls in detected_classes)
            if detected_classes
            else "✅ No sensitive content detected"
        )

        return {
            "image_path": str(censored_path),
            "detection_summary": detection_summary,
            "model_name": "NudeNet v2.0",
        }

    except Exception as e:
        raise RuntimeError(f"Nudity processing failed: {e}") from e
