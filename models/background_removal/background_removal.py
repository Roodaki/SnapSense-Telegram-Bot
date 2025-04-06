import os
import asyncio
from pathlib import Path
from PIL import Image
from rembg import remove
from typing import Dict, Any


async def process_image(
    original_path: str,
    output_folder: str,
    image_id: str,
) -> Dict[str, Any]:
    """Process image for background removal"""
    try:
        bgremoval_folder = Path(output_folder) / "background_removal"
        bgremoval_folder.mkdir(exist_ok=True)

        output_path = bgremoval_folder / f"nobg_{image_id}.png"

        # Run background removal in executor
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: _remove_bg(original_path, output_path))

        return {"image_path": str(output_path), "model_name": "Rembg 1.0"}

    except Exception as e:
        raise RuntimeError(f"Background removal failed: {e}") from e


def _remove_bg(input_path: str, output_path: Path):
    """Perform background removal with error handling"""
    try:
        with Image.open(input_path) as img:
            output = remove(img)
            output.save(output_path, "PNG")
    except IOError:
        raise ValueError("Invalid image file")
