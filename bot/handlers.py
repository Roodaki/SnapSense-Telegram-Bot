import os
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


async def start_handler(update: Update, context: CallbackContext):
    keyboard = keyboards.main_menu()
    sent_msg = await update.message.reply_text(
        "Welcome to SnapSense! Choose an option below:", reply_markup=keyboard
    )
    # Store the start menu message as an intermediary message
    context.user_data["prev_message"] = sent_msg.message_id


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "object_detection":
        context.user_data["task"] = "object_detection"
        # Edit the message and store the edited message's ID
        edited_msg = await query.edit_message_text(
            text="You selected Object Detection | YOLOv11x. Please send a photo to proceed."
        )
        context.user_data["prev_message"] = edited_msg.message_id
    # Future tasks can be added as elif conditions


async def delete_prev_intermediary(update: Update, context: CallbackContext):
    """Delete the previous intermediary message if it exists."""
    prev_msg_id = context.user_data.get("prev_message")
    if prev_msg_id:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id, message_id=prev_msg_id
            )
        except Exception:
            pass  # Ignore if deletion fails
        context.user_data["prev_message"] = None


async def photo_handler(update: Update, context: CallbackContext):
    try:
        # Verify a task has been selected
        task = context.user_data.get("task")
        if not task:
            await update.message.reply_text(
                "Please select a task from the menu first using /start.",
                reply_to_message_id=update.message.message_id,
            )
            return

        # Delete any previous intermediary message
        await delete_prev_intermediary(update, context)

        # Reply to the photo with an intermediary message indicating processing has started
        ack_message = await update.message.reply_text(
            "Your photo has been received and is being processed. Please wait...",
            reply_to_message_id=update.message.message_id,
        )
        context.user_data["prev_message"] = ack_message.message_id

        # Download the photo
        photo = update.message.photo[-1]
        file = await photo.get_file()
        image_id = str(update.message.message_id)
        image_folder = os.path.join("database", image_id)
        os.makedirs(image_folder, exist_ok=True)

        original_image_path = os.path.join(image_folder, f"{image_id}.jpg")
        await file.download_to_drive(original_image_path)

        # Process the image based on the selected task
        if task == "object_detection":
            processed_image_path = await object_detection.process_image(
                original_image_path, image_folder, image_id
            )
            # Delete the previous intermediary message before sending a new one
            await delete_prev_intermediary(update, context)
            comp_message = await update.message.reply_text(
                "Object Detection is complete! Sending the result...",
                reply_to_message_id=update.message.message_id,
            )
            context.user_data["prev_message"] = comp_message.message_id

            with open(processed_image_path, "rb") as f:
                await update.message.reply_photo(
                    photo=f, reply_to_message_id=update.message.message_id
                )

        # Clear task data
        context.user_data["task"] = None

        # Delete any intermediary message before showing the main menu
        await delete_prev_intermediary(update, context)
        # Return to the main menu
        await keyboards.send_main_menu(update, context)

    except Exception as e:
        utils.logger.error(f"Error processing photo {update.message.message_id}: {e}")
        await update.message.reply_text(
            "Sorry, something went wrong while processing your photo. Please try again later.",
            reply_to_message_id=update.message.message_id,
        )


def register_handlers(app):
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
