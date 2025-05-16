import asyncio
from pathlib import Path
from typing import Dict, Any
from deepface import DeepFace
from bot.strings import Strings


async def process_image(
    original_path: str, output_folder: str, image_id: str, config: Dict[str, Any]
) -> Dict[str, Any]:
    try:
        emotion_folder = Path(output_folder) / "emotion_recognition"
        emotion_folder.mkdir(exist_ok=True)

        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: DeepFace.analyze(
                img_path=original_path,
                actions=config["emotion_actions"],
                detector_backend=config["emotion_detector_backend"],
                enforce_detection=config["emotion_enforce_detection"],
                silent=config["emotion_silent"],
            ),
        )

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
            "model_name": Strings.MODEL_NAMES["emotion_recognition"],
            "faces_detected": len(results),
        }
    except ValueError as e:
        if "No face detected" in str(e):
            return {
                "emotions": [],
                "model_name": Strings.MODEL_NAMES["emotion_recognition"],
                "faces_detected": 0,
            }
        raise RuntimeError(
            Strings.PROCESSING_ERROR.format("emotion recognition")
        ) from e
    except Exception as e:
        raise RuntimeError(
            Strings.PROCESSING_ERROR.format("emotion recognition")
        ) from e
