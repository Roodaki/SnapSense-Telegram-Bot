import os
from dotenv import load_dotenv
from telegram.ext import Application
from bot import handlers, utils


def main():
    # Load environment variables from .env file
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Clean and recreate the "database" folder
    utils.clean_database()

    # Build the application and register handlers
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    handlers.register_handlers(app)

    # Start the bot (this internally handles the event loop)
    app.run_polling()


if __name__ == "__main__":
    main()
