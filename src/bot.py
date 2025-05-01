import os
import json

import commands

from dotenv import load_dotenv

from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from context import TheHabbitContext

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class TheHabbitBot():

    def __init__(self):
        load_dotenv()
        self._user_files = []
        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._app = ApplicationBuilder().token(TOKEN).context_types(ContextTypes(context=TheHabbitContext)).post_init(self._set_commands).build()
        self._app.add_handler(CommandHandler("start", commands.start))
        self._app.add_handler(CommandHandler("add_habit", commands.add_habit))
    
    def run(self):
        self._app.run_polling()
    
    async def _set_commands(self, app):
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("image", "Send a sample image"),
        ]
        await app.bot.set_my_commands(commands)
