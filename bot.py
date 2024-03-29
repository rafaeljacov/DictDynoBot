import os
import logging

from commands import start, help, define, button, synonym, antonym
from dotenv import load_dotenv
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    Application)

load_dotenv()

TOKEN = os.getenv('TOKEN') or ''


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger('__name__')


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('define', define))
    application.add_handler(CommandHandler('synonym', synonym))
    application.add_handler(CommandHandler('antonym', antonym))

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == "__main__":
    main()
