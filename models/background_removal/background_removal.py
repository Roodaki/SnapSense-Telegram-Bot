import asyncio
from pathlib import Path
from PIL import Image
from rembg import remove
from typing import Dict, Any
from bot.strings import Strings


async def process_image(
    original_path: str, output_folder: str, image_id: str
) -> Dict[str, Any]:
    try:
        bgremoval_folder = Path(output_folder) / "background_removal"
        bgremoval_folder.mkdir(exist_ok=True)
        output_path = bgremoval_folder / f"nobg_{image_id}.png"

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: _remove_bg(original_path, output_path))

        return {
            "image_path": str(output_path),
            "model_name": Strings.MODEL_NAMES["background_removal"],
        }
    except Exception as e:
        raise RuntimeError(Strings.PROCESSING_ERROR.format("background removal")) from e


def _remove_bg(input_path: str, output_path: Path):
    try:
        with Image.open(input_path) as img:
            output = remove(img)
            output.save(output_path, "PNG")
    except IOError:
        raise ValueError(Strings.INVALID_IMAGE)
