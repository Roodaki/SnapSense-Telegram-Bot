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
from bot.strings import Strings
from models.object_detection import object_detection
from models.nudity_detection import nudity_detection
from models.text_extraction import text_extraction
from models.background_removal import background_removal
from models.emotion_recognition import emotion_recognition


async def start_handler(update: Update, context: CallbackContext):
    """Handle /start command with clean state"""
    try:
        context.user_data.clear()
        keyboard = keyboards.main_menu()
        sent_msg = await update.message.reply_text(
            Strings.START_MESSAGE, reply_markup=keyboard
        )
        context.user_data["prev_message"] = sent_msg.message_id
    except Exception as e:
        utils.logger.error(f"Start handler error: {e}")
        await handle_error(update, context)


async def button_handler(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()
        task_id = query.data

        if task_id in Strings.MENU_ITEMS:
            _, _, task_message = Strings.MENU_ITEMS[task_id]
            context.user_data.update({"task": task_id, "task_message": task_message})

            edited_msg = await query.edit_message_text(
                text=Strings.TASK_SELECTION.format(task_message)
            )
            context.user_data["prev_message"] = edited_msg.message_id

    except Exception as e:
        utils.logger.error(f"Button handler error: {e}")
        await handle_error(update, context)


async def photo_handler(update: Update, context: CallbackContext):
    """Handle photo processing with state management"""
    try:
        if not (task := context.user_data.get("task")):
            await update.message.reply_text(
                Strings.INVALID_TASK_STATE,
                reply_to_message_id=update.message.message_id,
            )
            return

        await utils.delete_prev_messages(update, context)
        ack_message = await update.message.reply_text(
            Strings.PROCESSING, reply_to_message_id=update.message.message_id
        )
        context.user_data["prev_message"] = ack_message.message_id

        # Download photo
        photo_file = await update.message.photo[-1].get_file()
        image_id = str(update.message.message_id)
        image_folder = utils.create_image_folder(image_id)
        original_path = os.path.join(image_folder, f"original_{image_id}.jpg")
        await photo_file.download_to_drive(original_path)

        # Process image
        model_map = {
            "object_detection": (object_detection.process_image, "object_detection"),
            "nudity_detection": (nudity_detection.process_image, "nudity_detection"),
        }

        if task in model_map:
            processor, model_key = model_map[task]
            result = await processor(
                original_path, image_folder, image_id, context.bot_data[model_key]
            )
        elif task == "text_extraction":
            result = await text_extraction.process_image(
                original_path, image_folder, image_id
            )
        elif task == "background_removal":
            result = await background_removal.process_image(
                original_path, image_folder, image_id
            )
        elif task == "emotion_recognition":
            result = await emotion_recognition.process_image(
                original_path, image_folder, image_id
            )

        # Handle results
        result_handlers = {
            "text_extraction": utils.send_text_result,
            "emotion_recognition": utils.send_emotion_result,
        }

        if task in result_handlers:
            await result_handlers[task](
                update, result, context.user_data["task_message"]
            )
        else:
            await utils.send_processed_result(
                update, result, context.user_data["task_message"]
            )

        await utils.cleanup_operation(update, context)
        await keyboards.send_main_menu(update, context)

    except Exception as e:
        utils.logger.error(f"Photo processing error: {e}")
        await handle_error(update, context)
        await utils.cleanup_operation(update, context)


async def cancel_handler(update: Update, context: CallbackContext):
    """Handle operation cancellation"""
    await utils.cleanup_operation(update, context)
    await update.message.reply_text(Strings.OPERATION_CANCELLED)
    await keyboards.send_main_menu(update, context)


async def handle_error(update: Update, context: CallbackContext):
    """Centralized error handling"""
    if update.message:
        await update.message.reply_text(Strings.GENERIC_ERROR)
    elif update.callback_query:
        await update.callback_query.message.reply_text(Strings.GENERIC_ERROR)


def register_handlers(app):
    """Register all handlers with error handling"""
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("cancel", cancel_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_error_handler(lambda update, context: handle_error(update, context))
