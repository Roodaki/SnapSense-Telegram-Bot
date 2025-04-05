import os
import asyncio
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from bot import keyboards, utils
from models.object_detection import object_detection
from collections.abc import Coroutine
from models.nudity_detection import nudity_detection


async def start_handler(update: Update, context: CallbackContext):
    """Handle /start command with clean state"""
    try:
        context.user_data.clear()
        keyboard = keyboards.main_menu()
        sent_msg = await update.message.reply_text(
            "📸 Welcome to SnapSense! Choose an option below:", reply_markup=keyboard
        )
        context.user_data["prev_message"] = sent_msg.message_id
    except Exception as e:
        utils.logger.error(f"Start handler error: {e}")
        await handle_error(update, context)


async def button_handler(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "object_detection":
            context.user_data.update(
                {
                    "task": "object_detection",
                    "task_message": "Object Detection | YOLOv11x",
                }
            )
        elif query.data == "nudity_detection":
            context.user_data.update(
                {
                    "task": "nudity_detection",
                    "task_message": "Nudity Detection | NudeNet v2.0",
                }
            )

        edited_msg = await query.edit_message_text(
            text=f"🎯 You selected {context.user_data['task_message']}. Please send a photo to proceed."
        )
        context.user_data["prev_message"] = edited_msg.message_id

    except Exception as e:
        utils.logger.error(f"Button handler error: {e}")
        await handle_error(update, context)


async def photo_handler(update: Update, context: CallbackContext):
    """Handle photo processing with state management"""
    try:
        # State validation
        if not (task := context.user_data.get("task")):
            await update.message.reply_text(
                "⚠️ Please select a task from the menu first using /start.",
                reply_to_message_id=update.message.message_id,
            )
            return

        # Cleanup previous messages
        await utils.delete_prev_messages(update, context)

        # Acknowledge photo receipt
        ack_message = await update.message.reply_text(
            "⏳ Processing your photo...", reply_to_message_id=update.message.message_id
        )
        context.user_data["prev_message"] = ack_message.message_id

        # Download photo
        photo_file = await update.message.photo[-1].get_file()
        image_id = str(update.message.message_id)
        image_folder = utils.create_image_folder(image_id)

        original_path = os.path.join(image_folder, f"original_{image_id}.jpg")
        await photo_file.download_to_drive(original_path)

        # Process image based on task
        if task == "object_detection":
            result = await object_detection.process_image(
                original_path,
                image_folder,
                image_id,
                context.bot_data["object_detection"],
            )
        elif task == "nudity_detection":
            result = await nudity_detection.process_image(
                original_path,
                image_folder,
                image_id,
                context.bot_data["nudity_detection"],
            )

        # Send results
        await utils.send_processed_result(
            update, result, context.user_data["task_message"]
        )

        # Cleanup and reset state
        await utils.cleanup_operation(update, context)
        await keyboards.send_main_menu(update, context)

    except Exception as e:
        utils.logger.error(f"Photo processing error: {e}")
        await handle_error(update, context)
        await utils.cleanup_operation(update, context)


async def cancel_handler(update: Update, context: CallbackContext):
    """Handle operation cancellation"""
    await utils.cleanup_operation(update, context)
    await update.message.reply_text("❌ Operation cancelled.")
    await keyboards.send_main_menu(update, context)


async def handle_error(update: Update, context: CallbackContext):
    """Centralized error handling"""
    error_msg = "⚠️ An error occurred. Please try again."
    if update.message:
        await update.message.reply_text(error_msg)
    elif update.callback_query:
        await update.callback_query.message.reply_text(error_msg)


def register_handlers(app):
    """Register all handlers with error handling"""
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("cancel", cancel_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    # Error handler
    app.add_error_handler(lambda update, context: handle_error(update, context))
