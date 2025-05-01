import os
import json

from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from the_habbit import TheHabbitContext

USER_DATABASE_PATH = "db"

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def set_commands(app):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("image", "Send a sample image"),
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: TheHabbitContext):
    context.user_data["id"] = update.effective_user.id
    context.user_data["name"] = update.effective_user.name
    await update.message.reply_text(f"Welcome {context.user_name} to The Habbit!")

async def add_habit(update: Update, context: TheHabbitContext):
    print(context.user_file)

def main():
    app = ApplicationBuilder().token(TOKEN).context_types(ContextTypes(context=TheHabbitContext)).post_init(set_commands).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_habit", add_habit))
    # TODO: TheHabbitBot class with destructor for closing all of the fds
    # app.post_shutdown()
    app.run_polling()

if __name__ == "__main__":
    main()
