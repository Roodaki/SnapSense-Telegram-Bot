import asyncio
from pathlib import Path
from typing import Dict, Any
from deepface import DeepFace
import cv2


async def process_image(
    original_path: str,
    output_folder: str,
    image_id: str,
) -> Dict[str, Any]:
    """Process image for emotion analysis"""
    try:
        emotion_folder = Path(output_folder) / "emotion_recognition"
        emotion_folder.mkdir(exist_ok=True)

        # Run emotion analysis in executor
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: DeepFace.analyze(
                img_path=original_path,
                actions=["emotion"],
                detector_backend="opencv",
                enforce_detection=True,
                silent=True,
            ),
        )

        # Process multiple faces
        emotions = []
        for face in results:
            emotions.append(
                {
                    "dominant": face["dominant_emotion"],
                    "scores": face["emotion"],
                    "region": face["region"],
                }
            )

        return {
            "emotions": emotions,
            "model_name": "DeepFace Emotion",
            "faces_detected": len(results),
        }

    except ValueError as e:
        if "No face detected" in str(e):
            return {
                "emotions": [],
                "model_name": "DeepFace Emotion",
                "faces_detected": 0,
            }
        raise RuntimeError(f"Emotion analysis failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Emotion processing error: {e}") from e
