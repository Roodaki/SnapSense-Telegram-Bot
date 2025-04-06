from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


def main_menu():
    """Generate main menu keyboard"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔍 Object Detection", callback_data="object_detection"
                ),
                InlineKeyboardButton(
                    "😃 Emotion Recognition", callback_data="emotion_recognition"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🚫 Nudity Detection", callback_data="nudity_detection"
                ),
                InlineKeyboardButton(
                    "📝 Text Extraction", callback_data="text_extraction"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🎭 Background Removal", callback_data="background_removal"
                )
            ],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        ]
    )


async def send_main_menu(update: Update, context: CallbackContext):
    """Send or update to main menu"""
    try:
        reply_markup = main_menu()
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "Choose your next task:", reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "Choose your next task:", reply_markup=reply_markup
            )
    except Exception:
        await update.message.reply_text(
            "Choose your next task:", reply_markup=reply_markup
        )
