from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram import Update


def main_menu():
    keyboard = [
        [InlineKeyboardButton("Object Detection", callback_data="object_detection")],
        # Add additional buttons for future tasks here.
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_main_menu(update: Update, context: CallbackContext):
    reply_markup = main_menu()
    await update.message.reply_text("Choose your next task:", reply_markup=reply_markup)
