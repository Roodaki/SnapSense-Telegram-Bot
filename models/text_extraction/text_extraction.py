import asyncio
from pathlib import Path
from PIL import Image
import pytesseract
from typing import Dict, Any
from bot.strings import Strings


async def process_image(
    original_path: str, output_folder: str, image_id: str
) -> Dict[str, Any]:
    """Process image for text extraction"""
    try:
        text_folder = Path(output_folder) / "text_extraction"
        text_folder.mkdir(exist_ok=True)

        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, lambda: _extract_text(original_path))

        txt_path = text_folder / f"extracted_{image_id}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text or Strings.NO_TEXT)

        return {
            "text": text,
            "text_path": str(txt_path),
            "model_name": Strings.MODEL_NAMES["text_extraction"],
        }
    except Exception as e:
        raise RuntimeError(Strings.PROCESSING_ERROR.format("text extraction")) from e


def _extract_text(image_path: str) -> str:
    """Perform OCR with centralized error handling"""
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img)
    except IOError:
        raise ValueError(Strings.INVALID_IMAGE)
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(Strings.MISSING_DEPENDENCY.format("Tesseract OCR"))
