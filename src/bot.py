import os
import json

from functools import wraps
from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

import commands

from user import User

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

USER_DATABASE_PATH = "./db"

class TheHabbitBot():
    def __init__(self):
        load_dotenv()
        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._app = ApplicationBuilder().token(TOKEN).post_init(self._set_commands).build()
        self._app.add_handler(CommandHandler("start", self.user_state(commands.start)))
        self._app.add_handler(CommandHandler("add_habit", commands.add_habit))
    
    def run(self):
        self._app.run_polling()
    
    async def _set_commands(self, app):
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("add_habit", "Send a sample image"),
        ]
        await app.bot.set_my_commands(commands)

    @staticmethod
    def user_state(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user = TheHabbitBot._get_user_data(update.effective_user.id, update.effective_user.name)
            context.user = user
            return_value = await func(update, context, *args, **kwargs)
            TheHabbitBot._save_user_data(user) 
            return return_value
        return wrapper

    @staticmethod
    def _save_user_data(user: User):
        user_file_path = f"{USER_DATABASE_PATH}/{user.id}.json"
        with open(user_file_path, "w") as user_fd:
            user_fd.write(user.model_dump_json(indent=4))

    @staticmethod
    def _get_user_data(user_id: int, user_name: str):
        user_file_path = f"{USER_DATABASE_PATH}/{user_id}.json"
        if not os.path.exists(user_file_path):
            user = User(
                id=user_id,
                username=user_name,
                join_date=datetime.today().strftime("%d/%m/%Y")
            )
            TheHabbitBot._save_user_data(user)
            return user

        with open(user_file_path, "r") as user_fd:
            user_data = json.load(user_fd)
        return User(**user_data)
