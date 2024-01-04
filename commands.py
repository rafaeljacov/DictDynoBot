from reply import replies
import requests
import json

from telegram import Update
from telegram.ext import ContextTypes
from schema import Schema, Optional, SchemaUnexpectedTypeError


response_schema = Schema([
    {
        'word': str,
        Optional('phonetic'): str,
        'phonetics': [
            {
                Optional('text'): str,
                Optional('audio'): str,
                Optional('sourceUrl'): str,
                Optional('license'): {
                    'name': str,
                    'url': str
                },
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
        'license': {
            'name': str,
            'url': str
        },
        'sourceUrls': [str]
    }
])

API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(replies['start'])


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(replies['help'])


async def define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args).strip()
    response = requests.get(API + text)

    # Parse json response
    parsed = json.loads(response.text)

    # Validate data
    try:
        data = response_schema.validate(parsed)
    except SchemaUnexpectedTypeError:  # No Definitions were found
        await update.message.reply_text(replies['no_definition'])
