import os
import logging
import yaml
from dotenv import load_dotenv
from telegram.ext import Application
from bot import handlers, utils
from models.object_detection import object_detection
from models.nudity_detection import nudity_detection
from models.image_segmentation import image_segmentation

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def main():
    try:
        load_dotenv()
        TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment")

        config = load_config()

        utils.clean_database(config)

        object_model_data = object_detection.initialize_model(
            config["models"]["object_detection"]
        )
        nudity_detector = (
            nudity_detection.initialize_detector()
        )  # NudeDetector init doesn't take config directly
        segmentation_model = image_segmentation.initialize_model(
            config["models"]["image_segmentation"]
        )

        app = (
            Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
        )

        app.bot_data.update(
            {
                "config": config,
                "object_detection_model_data": object_model_data,
                "nudity_detection_detector": nudity_detector,
                "image_segmentation_model": segmentation_model,
            }
        )

        handlers.register_handlers(app)

        logger.info("Starting bot in polling mode...")
        app.run_polling(drop_pending_updates=config["app"]["drop_pending_updates"])

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


async def post_init(app: Application):
    from bot.strings import Strings

    await app.bot.set_my_commands(Strings.COMMANDS)


if __name__ == "__main__":
    main()
