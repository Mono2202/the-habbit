import os

from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from commands import COMMANDS, HANDLERS
from utils import user_state

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class TheHabbitBot():
    def __init__(self):
        load_dotenv()
        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._app = ApplicationBuilder().token(TOKEN).post_init(self._set_commands).build()
    
    def run(self):
        self._app.run_polling()
    
    @staticmethod
    async def _set_commands(app: Application):
        bot_commands = []

        for handler in HANDLERS:
            app.add_handler(handler)

        for command in COMMANDS:
            app.add_handler(
                CommandHandler(
                    command.name,
                    command.function
                )
            )

            bot_commands.append(
                BotCommand(
                    command.name,
                    command.description
                )
            )

        await app.bot.set_my_commands(bot_commands)
