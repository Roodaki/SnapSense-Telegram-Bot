import os
import asyncio
from pathlib import Path
from PIL import Image
import pytesseract
from typing import Dict, Any


async def process_image(
    original_path: str,
    output_folder: str,
    image_id: str,
) -> Dict[str, Any]:
    """Process image for text extraction"""
    try:
        text_folder = Path(output_folder) / "text_extraction"
        text_folder.mkdir(exist_ok=True)

        # Run OCR in executor
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, lambda: _extract_text(original_path))

        # Save text to file
        txt_path = text_folder / f"extracted_{image_id}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        return {"text": text, "text_path": str(txt_path), "model_name": "Tesseract OCR"}

    except Exception as e:
        raise RuntimeError(f"Text extraction failed: {e}") from e


def _extract_text(image_path: str) -> str:
    """Perform OCR with error handling"""
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img)
    except IOError:
        raise ValueError("Invalid image file")
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError("OCR engine not installed")
