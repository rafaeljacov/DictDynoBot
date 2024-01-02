import os
import logging

from commands import start, help, define
from dotenv import load_dotenv
from telegram.ext import MessageHandler, filters, CommandHandler, Application

load_dotenv()

API = os.getenv('API')
TOKEN = os.getenv('TOKEN')


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

    application.run_polling()


if __name__ == "__main__":
    main()
