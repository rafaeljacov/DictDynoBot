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
    # Check if there is no word to define
    if not context.args:
        await update.message.reply_text('Please give me a word to define.')
        return None

    text = ' '.join(context.args).strip()
    response = requests.get(API + text)

    # Parse json response
    parsed = json.loads(response.text)

    if text not in context.user_data:
        # Validate data
        try:
            data = response_schema.validate(parsed)
            audio = ''
            definitions = []

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
            # Store to context
            context.user_data[text] = definitions

        except SchemaUnexpectedTypeError:  # No Definitions were found
            await update.message.reply_text(replies['no_definition'])
            return None

    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton('Next Definition',
                             # State for text, index, and action
                             callback_data=f'{text} 0 next'))

    # Reply Message
    reply = f'<b>{text.capitalize()}:</b>\t\t'
    reply += f'<i>{context.user_data[text][0].partOfSpeech}</i>\n'
    reply += f'\n<blockquote>{context.user_data[text][0].definition}</blockquote>'

    if context.user_data[text][0].example:
        reply += f'Example: <i>{context.user_data[text][0].example}</i>\n'

    reply += f'\n\n<i>1 of {len(context.user_data[text])}</i>'

    await update.message.reply_html(reply, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text, index, action = query.data.split()
    index = int(index)

    if action == 'prev':
        if index == 0:
            index = len(context.user_data[text]) - 1
        else:
            index -= 1
    elif action == 'next':
        if index == len(context.user_data[text]) - 1:
            index = 0
        else:
            index += 1

    keyboard = [
        [
            InlineKeyboardButton(
                'Prev Definition', callback_data=f'{text} {index} prev'),
            InlineKeyboardButton(
                'Next Definition', callback_data=f'{text} {index} next')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Reply Message
    reply = f'<b>{text.capitalize()}:</b>\t\t'
    reply += f'<i>{context.user_data[text][index].partOfSpeech}</i>\n'
    reply += f'\n<blockquote>{context.user_data[text][index].definition}</blockquote>'

    if context.user_data[text][index].example:
        reply += f'\n\nExample: <i>{context.user_data[text][index].example}</i>\n'

    reply += f'\n\n<b><i>{index + 1} of {len(context.user_data[text])}</i></b>'

    await query.edit_message_text(reply, reply_markup=reply_markup, parse_mode='HTML')
