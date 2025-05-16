"""Centralized string management for the Telegram bot"""


class Strings:
    # ======================
    # Application Constants
    # ======================
    MODEL_NAMES = {
        "object_detection": "YOLO",
        "nudity_detection": "NudeNet",
        "text_extraction": "Tesseract OCR",
        "background_removal": "Rembg",
        "emotion_recognition": "DeepFace Emotion",
        "image_segmentation": "SAM (Segment Anything)",
    }

    BOT_ID = "@SnapSenseBot"
    BOT_ID_SUFFIX = "\n\n🆔 {}"

    # ======================
    # User Interaction
    # ======================
    START_MESSAGE = "👋 Welcome to SnapSense Bot!\n\n📸 I can help you analyze images using various AI models.\n\n👇 Choose an option to get started:"

    COMMANDS = [("start", "Start the bot"), ("cancel", "Cancel current operation")]

    MAIN_MENU_HEADER = "📸 *SnapSense Menu*\n\n👇 Select an analysis option:"

    MENU_ITEMS = {
        "object_detection": (
            "🔎 Detect Objects",
            "object_detection",
            "Object Detection",
        ),
        "emotion_recognition": (
            "😊 Analyze Emotions",
            "emotion_recognition",
            "Emotion Recognition",
        ),
        "nudity_detection": (
            "🔞 Check for Sensitive Content",
            "nudity_detection",
            "Nudity Detection",
        ),
        "text_extraction": (
            "📝 Extract Text (OCR)",
            "text_extraction",
            "Text Extraction",
        ),
        "background_removal": (
            "✂️ Remove Background",
            "background_removal",
            "Background Removal",
        ),
        "image_segmentation": (
            "🧩 Segment Image",
            "image_segmentation",
            "Image Segmentation",
        ),
    }

    # ======================
    # System Messages
    # ======================
    GENERIC_ERROR = (
        "❌ Oops! Something went wrong.\n\nPlease use /start to begin a new task."
    )
    OPERATION_CANCELLED = (
        "❌ Operation cancelled.\n\n🤔 What would you like to do next?"
    )
    PROCESSING = "✅ Got it!\n\n⏳ Processing your photo now..."

    TASK_SELECTION = (
        "✅ Task selected: {}.\n\n👇 Now, please send me the photo you want to analyze."
    )

    INVALID_TASK_STATE = "👋 Hey there!\n\n🤔 It looks like you sent a photo without selecting a task first.\n\nPlease use /start to choose an option from the menu."
    FILE_ERROR = "⚠️ A file error occurred 📂, possibly during model loading."
    FILE_OPERATION_ERROR = (
        "⚠️ Failed to perform a file operation 💾 (e.g., save or delete)."
    )

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
    TEXT_RESULT = "📝 *{} Result*\n\n" "🧠 *Model:* {}\n\n" "```\n{}\n```\n\n"

    # Nudity Detection
    NUDITY_DETECTED = "🚫 Detected sensitive content:\n• {}"
    NO_NUDITY = "✅ No sensitive content detected"

    # Image Segmentation
    SEGMENTATION_SUMMARY = "🔍 Detected {} distinct segments"

    # ======================
    # Specific Errors/Messages within Results
    # ======================
    MODEL_INIT_ERROR = "❌ {} model initialization failed 😟"
    PROCESSING_ERROR = "❌ Error processing {} 😥"
    RESULT_FORMAT_ERROR = "❌ Error formatting detection results 💔"
    OBJECT_DETECTION_LINE = "🔹 {}: {}"
    NO_OBJECTS = "👁️‍🗨️ No objects detected."
    NO_TEXT = "❌📄 No text could be extracted."
    INVALID_IMAGE = "⚠️ Invalid image file 🖼️."
    MISSING_DEPENDENCY = "⚠️ Required component not found: {} 🛠️."

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
