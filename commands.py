from reply import replies
import requests
import json

from telegram import Update
from telegram.ext import ContextTypes
from schema import Schema, And, Use, Optional


response_schema = Schema([
    {
        'word': str,
        'phonetic': str,
        Optional('phonetics'): [
            {
                Optional('text'): str,
                Optional('audio'): str,
                Optional('sourceUrl'): str,
                Optional('license'): dict,
            }
        ],
        'meanings': [
            {

                'partOfSpeech': str,
                'definitions': [
                    {
                        'definition': str,
                        'synonyms': [str],
                        'antonyms': [str],
                        Optional('example'): str
                    }
                ],
                'synonyms': [str],
                'antonyms': [str]
            }
        ],
        Optional('license'): dict,
        Optional('sourceUrls'): list
    }
])

API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(replies['start'])


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(replies['help'])


async def define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # text = ' '.join(context.args).strip()
    text = "mark"
    response = requests.get(API + text)

    # Parse json response
    data = json.loads(response)
