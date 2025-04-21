from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


def main_menu():
    """Generate main menu keyboard with vertical layout"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔍 Object Detection", callback_data="object_detection"
                )
            ],
            [
                InlineKeyboardButton(
                    "😃 Emotion Recognition", callback_data="emotion_recognition"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 Nudity Detection", callback_data="nudity_detection"
                )
            ],
            [
                InlineKeyboardButton(
                    "📝 Text Extraction", callback_data="text_extraction"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎭 Background Removal", callback_data="background_removal"
                )
            ],
        ]
    )


async def send_main_menu(update: Update, context: CallbackContext):
    """Send or update to main menu"""
    try:
        reply_markup = main_menu()
        message_text = "📸 *SnapSense Menu*\nSelect an analysis option:"

        if update.callback_query:
            await update.callback_query.edit_message_text(
                message_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
            )
        else:
            await update.message.reply_text(
                message_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
            )
    except Exception:
        await update.message.reply_text(
            message_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
        )
