from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from bot.strings import Strings


def main_menu():
    buttons = [
        [InlineKeyboardButton(text, callback_data=cb_data)]
        for text, cb_data, _ in Strings.MENU_ITEMS.values()
    ]
    return InlineKeyboardMarkup(buttons)


async def send_main_menu(update: Update, context: CallbackContext):
    reply_markup = main_menu()
    # Use the new MAIN_MENU_HEADER constant from Strings
    message_text = Strings.MAIN_MENU_HEADER

    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
            )
        else:
            await update.message.reply_text(
                message_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
            )
    except Exception:
        # Fallback in case edit fails (e.g., message too old)
        await update.message.reply_text(
            message_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
        )
