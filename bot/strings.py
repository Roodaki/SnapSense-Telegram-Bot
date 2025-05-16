# strings.py
"""Centralized string management for the Telegram bot"""


class Strings:
    # ======================
    # Application Constants
    # ======================
    MODEL_NAMES = {
        "object_detection": "YOLOv11x",
        "nudity_detection": "NudeNet v2.0",
        "text_extraction": "Tesseract OCR",
        "background_removal": "Rembg",
        "emotion_recognition": "DeepFace Emotion",
        "image_segmentation": "SAM (Segment Anything)",
    }

    # NUDITY_CLASSES moved to config.yaml

    # ======================
    # User Interaction
    # ======================
    START_MESSAGE = "📸 Welcome to SnapSense! Choose an option below:"
    COMMANDS = [("start", "Start the bot"), ("cancel", "Cancel current operation")]

    MENU_ITEMS = {
        "object_detection": (
            "🔍 Object Detection",
            "object_detection",
            "Object Detection | YOLOv11x",
        ),
        "emotion_recognition": (
            "😃 Emotion Recognition",
            "emotion_recognition",
            "Emotion Recognition | DeepFace",
        ),
        "nudity_detection": (
            "🚫 Nudity Detection",
            "nudity_detection",
            "Nudity Detection | NudeNet v2.0",
        ),
        "text_extraction": (
            "📝 Text Extraction",
            "text_extraction",
            "Text Extraction | Tesseract OCR",
        ),
        "background_removal": (
            "🎭 Background Removal",
            "background_removal",
            "Background Removal | Rembg",
        ),
        "image_segmentation": (
            "🔲 Image Segmentation",
            "image_segmentation",
            "Image Segmentation | SAM",
        ),
    }

    # ======================
    # System Messages
    # ======================
    GENERIC_ERROR = "⚠️ An error occurred. Please try again."
    OPERATION_CANCELLED = "❌ Operation cancelled."
    PROCESSING = "⏳ Processing your photo..."
    TASK_SELECTION = "🎯 You selected {}. Please send a photo to proceed."
    INVALID_TASK_STATE = "⚠️ Please select a task from the menu first using /start."
    FILE_ERROR = "⚠️ File operation failed. Please try again."

    # ======================
    # Result Templates
    # ======================
    RESULT_HEADER = "📸 *{} Result*\n\n"
    MODEL_INFO = "🧠 *Model:* {}"
    SPEED_STATS = (
        "⚙️ *Speed Stats (ms)*\n"
        "• Preprocessing: `{preprocess:.2f}`\n"
        "• Inference: `{inference:.2f}`\n"
        "• Postprocessing: `{postprocess:.2f}`"
    )

    # Emotion Recognition
    EMOTION_HEADER = "😃 *{} Result*\n\n"
    FACES_DETECTED = "Detected {} face{}:\n\n"
    EMOTION_FORMAT = "*Face {}:*\n🎭 Dominant Emotion: {}\n```\n{}\n```\n\n"

    # Text Extraction
    TEXT_RESULT = "📝 *{} Result*\n\n" "```\n{}\n```\n\n" "🧠 *OCR Engine:* {}"

    # Nudity Detection
    NUDITY_DETECTED = "🚫 Detected sensitive content:\n• {}"
    NO_NUDITY = "✅ No sensitive content detected"

    # Image Segmentation
    SEGMENTATION_SUMMARY = "Detected {} distinct segments"

    # ======================
    # Error Messages
    # ======================
    MODEL_INIT_ERROR = "❌ {} model initialization failed"
    PROCESSING_ERROR = "❌ Error processing {}"
    RESULT_FORMAT_ERROR = "❌ Error formatting detection results"
    OBJECT_DETECTION_LINE = "🔹 {}: {}"
    NO_OBJECTS = "No objects detected."
    NO_TEXT = "No text could be extracted"
    INVALID_IMAGE = "Invalid image file"
    MISSING_DEPENDENCY = "Required component not found: {}"
    FILE_OPERATION_ERROR = "File operation failed"

    # ======================
    # Formatting Helpers
    # ======================
    @classmethod
    def format_speed_stats(
        cls, preprocess: float, inference: float, postprocess: float
    ) -> str:
        """Format speed statistics using centralized template"""
        return cls.SPEED_STATS.format(
            preprocess=preprocess, inference=inference, postprocess=postprocess
        )

    @classmethod
    def format_plural(cls, count: int) -> str:
        """Return plural suffix when needed"""
        return "s" if count > 1 else ""
