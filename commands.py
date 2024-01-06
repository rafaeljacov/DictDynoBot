import requests
import json

from reply import replies
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from schema import Schema, Optional, SchemaUnexpectedTypeError


# For /define command
class Definition:
    def __init__(self, audio, partOfSpeech, definition, example):
        self.audio = audio
        self.partOfSpeech = partOfSpeech
        self.definition = definition
        self.example = example


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
        definitions = []
        audio = ''

        for result in data:
            for item in result['phonetics']:
                if item['audio']:
                    audio = item['audio']
                    break

            for meaning in result['meanings']:
                partOfSpeech = meaning['partOfSpeech']
                for item in meaning['definitions']:
                    # Initialize example if it exists in the dictionary
                    example = item['example'] if 'example' in item else ''

                    definitions.append(
                        Definition(
                            audio,
                            partOfSpeech,
                            item['definition'],
                            example
                        ))

    except SchemaUnexpectedTypeError:  # No Definitions were found
        await update.message.reply_text(replies['no_definition'])
