import asyncio
import numpy as np
import cv2
import torch
from pathlib import Path
from typing import Dict, Any
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from bot.strings import Strings


def initialize_model(config: Dict[str, Any]) -> SamAutomaticMaskGenerator:
    try:
        checkpoint_path = config["checkpoint_path"]
        model_type = config["model_type"]
        device = config.get(
            "preferred_device", "cuda" if torch.cuda.is_available() else "cpu"
        )

        sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
        sam.to(device=device)

        return SamAutomaticMaskGenerator(sam)
    except Exception as e:
        raise RuntimeError(Strings.MODEL_INIT_ERROR.format("image segmentation")) from e


async def process_image(
    original_path: str,
    output_folder: str,
    image_id: str,
    mask_generator: SamAutomaticMaskGenerator,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    try:
        seg_folder = Path(output_folder) / "image_segmentation"
        seg_folder.mkdir(exist_ok=True)
        output_path = seg_folder / f"segmentation_{image_id}.png"

        loop = asyncio.get_event_loop()

        image_bgr = await loop.run_in_executor(None, lambda: cv2.imread(original_path))
        image_rgb = await loop.run_in_executor(
            None, lambda: cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        )

        masks = await loop.run_in_executor(
            None, lambda: mask_generator.generate(image_rgb)
        )

        segmentation_image = np.zeros(image_rgb.shape, dtype=np.uint8)
        for mask in masks:
            color = np.random.randint(0, 256, size=3)
            segmentation_image[mask["segmentation"]] = color

        await loop.run_in_executor(
            None,
            lambda: cv2.imwrite(
                str(output_path), cv2.cvtColor(segmentation_image, cv2.COLOR_RGB2BGR)
            ),
        )

        return {
            "image_path": str(output_path),
            "model_name": Strings.MODEL_NAMES["image_segmentation"],
            "detection_summary": Strings.SEGMENTATION_SUMMARY.format(len(masks)),
        }
    except Exception as e:
        raise RuntimeError(Strings.PROCESSING_ERROR.format("image segmentation")) from e
