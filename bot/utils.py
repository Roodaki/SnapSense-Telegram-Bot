import os
import shutil
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.helpers import escape_markdown
from bot.strings import Strings

logger = logging.getLogger(__name__)


def clean_database():
    """Initialize clean database folder"""
    try:
        if os.path.exists("database"):
            shutil.rmtree("database")
        os.makedirs("database", exist_ok=True)
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")
        raise


def create_image_folder(image_id: str) -> str:
    """Create unique image processing folder"""
    image_folder = os.path.join("database", image_id)
    os.makedirs(image_folder, exist_ok=True)
    return image_folder


async def delete_prev_messages(update: Update, context: CallbackContext):
    """Delete previous bot messages"""
    try:
        if prev_msg_id := context.user_data.get("prev_message"):
            await context.bot.delete_message(
                chat_id=update.effective_chat.id, message_id=prev_msg_id
            )
            context.user_data["prev_message"] = None
    except Exception as e:
        logger.warning(f"Message deletion failed: {e}")


async def send_processed_result(update: Update, result: dict, task_name: str):
    """Send formatted processing result"""
    try:
        safe_task = escape_markdown(task_name, version=2)
        safe_model = escape_markdown(result.get("model_name", "Unknown"), version=2)

        base_caption = Strings.RESULT_HEADER.format(safe_task)
        base_caption += Strings.MODEL_INFO.format(safe_model)

        if "detection_summary" in result:
            safe_summary = escape_markdown(result["detection_summary"], version=2)
            base_caption += f"\n\n{safe_summary}"

        if "speed_summary" in result:
            safe_speed = escape_markdown(result["speed_summary"], version=2)
            base_caption += f"\n\n{safe_speed}"

        with open(result["image_path"], "rb") as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=base_caption,
                parse_mode="MarkdownV2",
                reply_to_message_id=update.message.message_id,
            )

    except Exception as e:
        logger.error(f"Failed to send result: {e}")
        await update.message.reply_text(Strings.GENERIC_ERROR)


async def send_emotion_result(update: Update, result: dict, task_name: str):
    """Send formatted emotion analysis result"""
    try:
        safe_task = escape_markdown(task_name, version=2)
        faces = result["faces_detected"]
        base_msg = Strings.EMOTION_HEADER.format(safe_task)

        if faces == 0:
            base_msg += "No faces detected in the image"
        else:
            base_msg += Strings.FACES_DETECTED.format(faces, "s" if faces > 1 else "")

            for idx, emotion in enumerate(result["emotions"], 1):
                scores = "\n".join(
                    f"{k}: {v:.1f}%" for k, v in emotion["scores"].items()
                )
                base_msg += Strings.EMOTION_FORMAT.format(
                    idx,
                    escape_markdown(emotion["dominant"], version=2),
                    escape_markdown(scores, version=2),
                )

        await update.message.reply_text(
            base_msg,
            parse_mode="MarkdownV2",
            reply_to_message_id=update.message.message_id,
        )

    except Exception as e:
        logger.error(f"Emotion result error: {e}")
        await update.message.reply_text(Strings.GENERIC_ERROR)


async def send_text_result(update: Update, result: dict, task_name: str):
    """Send formatted text extraction result"""
    try:
        text = result.get("text", "No text could be extracted")
        safe_text = escape_markdown(text, version=2)
        safe_task = escape_markdown(task_name, version=2)
        safe_model = escape_markdown(result.get("model_name", "Unknown"), version=2)

        message = Strings.TEXT_RESULT.format(safe_task, safe_text, safe_model)

        if len(message) > 4096:
            message = message[:4000] + "\n... (truncated)"

        await update.message.reply_text(
            message,
            parse_mode="MarkdownV2",
            reply_to_message_id=update.message.message_id,
        )

    except Exception as e:
        logger.error(f"Text result error: {e}")
        await update.message.reply_text(Strings.GENERIC_ERROR)


async def cleanup_operation(update: Update, context: CallbackContext):
    """Cleanup resources and user state"""
    try:
        await delete_prev_messages(update, context)
        context.user_data.pop("task", None)
        context.user_data.pop("task_message", None)
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
