import requests
import json

from telegram import Update
from telegram.ext import ContextTypes

API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('''
                            🤖 DictDynoBot - Your Ultimate Dictionary Companion!
Welcome to DictDynoBot, the intelligent bot designed to elevate your language skills and enhance your word knowledge. 📚✨

Key Features:

🔍 Define Words: Use /define <word> to instantly access accurate and concise definitions for any word in the English language.

🔄 Thesaurus Exploration: Discover a world of synonyms by typing /synonym <word> and expand your vocabulary with precision.

🔀 Antonym Adventure: Seek the opposite meaning by trying /antonym <word>, perfect for diversifying your word choices.

🔎 Full-Text Search: Conduct comprehensive searches across our extensive database by using /search <query>. Whether you're looking for specific terms or exploring broad topics, DictDynoBot has you covered.

DictDynoBot is your go-to language companion, making learning and exploring the English language an engaging experience. Start your word journey now! 🌐📖
                            ''')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update.message.reply_text('''
            I am DictDynoBot, your reliable dictionary companion. 📚✨

Here's how I can assist you:

1️⃣ Search Definitions: Type /define <word> to get the definition of a specific word.

2️⃣ Thesaurus Mode: Use /synonym <word> to explore synonyms for a chosen word.

3️⃣ Antonym Hunt: Try /antonym <word> to find antonyms and expand your vocabulary.

4️⃣ull-Text Search: Conduct comprehensive searches across a vast word database by using /search <query>. Explore topics or find specific terms effortlessly!

To get started, simply type one of the commands above. Happy exploring! 🌐🔍
                              ''')


async def define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args).strip()
    response = requests.get(API + text)
    data = json.loads(response)
    
