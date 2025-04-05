import os
import shutil
import logging
from typing import Dict, Any
from telegram import Update
from telegram.ext import CallbackContext

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


async def send_processed_result(update: Update, result: Dict[str, Any], task_name: str):
    """Send formatted processing result"""
    caption = (
        f"📸 *{task_name} Result*\n\n"
        f"🔍 *Detected Objects:*\n{result['detection_summary']}\n\n"
        f"{result['speed_summary']}"
    )

    with open(result["image_path"], "rb") as photo_file:
        await update.message.reply_photo(
            photo=photo_file,
            caption=caption,
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id,
        )


async def cleanup_operation(update: Update, context: CallbackContext):
    """Cleanup resources and user state"""
    try:
        await delete_prev_messages(update, context)
        context.user_data.pop("task", None)
        context.user_data.pop("task_message", None)
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
