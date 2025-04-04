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
    # Use the keyboards module to get the main menu keyboard
    keyboard = keyboards.main_menu()
    await update.message.reply_text(
        "Welcome to SnapSense! Choose an option below:", reply_markup=keyboard
    )


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "object_detection":
        context.user_data["task"] = "object_detection"
        await query.edit_message_text(
            text="You selected Object Detection | YOLOv11x. Please send a photo to proceed."
        )
    # Future tasks can be added as elif conditions


async def photo_handler(update: Update, context: CallbackContext):
    try:
        # Verify a task has been selected
        task = context.user_data.get("task")
        if not task:
            await update.message.reply_text(
                "Please select a task from the menu first using /start."
            )
            return

        # Send an acknowledgment message that the photo is being processed
        await update.message.reply_text(
            "Your photo has been received and is being processed. Please wait..."
        )

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
            await update.message.reply_text(
                "Object Detection is complete! Sending the result..."
            )
            with open(processed_image_path, "rb") as f:
                await update.message.reply_photo(photo=f)

        # Clear task data
        context.user_data["task"] = None

        # Return to the main menu by calling the start command function again.
        await keyboards.send_main_menu(update, context)

    except Exception as e:
        utils.logger.error(f"Error processing photo {update.message.message_id}: {e}")
        await update.message.reply_text(
            "Sorry, something went wrong while processing your photo. Please try again later."
        )


def register_handlers(app):
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
