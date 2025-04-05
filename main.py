import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, ContextTypes
from bot import handlers, utils
from models.object_detection import object_detection

# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Simplified custom context without overriding __init__
class CustomContext(ContextTypes.DEFAULT_TYPE):
    @property
    def model_data(self):
        return self.application.bot_data.get("model_data")


def main():
    """Main application entry point"""
    try:
        load_dotenv()
        TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment")

        utils.clean_database()

        # Initialize model during startup
        model_data = object_detection.initialize_model()

        # Create application with custom context
        context_types = ContextTypes(context=CustomContext)
        app = (
            Application.builder()
            .token(TELEGRAM_BOT_TOKEN)
            .post_init(post_init)
            .context_types(context_types)
            .build()
        )

        # Store model in bot_data
        app.bot_data["model_data"] = model_data

        handlers.register_handlers(app)

        logger.info("Starting bot in polling mode...")
        app.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


async def post_init(app: Application):
    """Post-initialization tasks"""
    await app.bot.set_my_commands(
        [("start", "Start the bot"), ("cancel", "Cancel current operation")]
    )


if __name__ == "__main__":
    main()
