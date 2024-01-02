import requests
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import MessageHandler, filters, CommandHandler

load_dotenv()

API = os.getenv('API')
TOKEN = os.getenv('TOKEN')

print(API, TOKEN)
