import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application
from bot import handlers, utils
from models.object_detection import object_detection
from models.nudity_detection import nudity_detection
from models.image_segmentation import image_segmentation

# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    try:
        load_dotenv()
        TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment")

        utils.clean_database()

        # Initialize models
        object_model = object_detection.initialize_model()
        nudity_detector = nudity_detection.initialize_detector()
        segmentation_model = image_segmentation.initialize_model()

        # Create application
        app = (
            Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
        )

        # Store models
        app.bot_data.update(
            {
                "object_detection": object_model,
                "nudity_detection": nudity_detector,
                "image_segmentation": segmentation_model,
            }
        )

        handlers.register_handlers(app)

        logger.info("Starting bot in polling mode...")
        app.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


async def post_init(app: Application):
    """Post-initialization tasks"""
    from bot.strings import Strings

    await app.bot.set_my_commands(Strings.COMMANDS)


if __name__ == "__main__":
    main()
