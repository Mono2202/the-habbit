import os
import json

from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

USER_DATABASE_PATH = "db"

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def set_commands(app):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("image", "Send a sample image"),
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        user_file_path = [entry for entry in os.listdir(USER_DATABASE_PATH) if entry.startswith(str(user.id)) and os.path.isfile(entry)][0]
        await update.message.reply_text(f"Hello {user.name}! Welcome back :)")
    except IndexError:
        user_file_path = f"{USER_DATABASE_PATH}/{user.id}.json"
        await update.message.reply_text(f"Hi {user.name}! Welcome to your Habit Tracker! Let's start :)")
    
    with open(user_file_path, "a+") as user_file:
        json.dump(
            {
                "username": user.name,
                "join_date": datetime.today().strftime("%d/%m/%Y")
            },
            user_file,
            indent=4
        )
        

async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(".\\assets\\golbat.png", "rb") as img:
        await update.message.reply_photo(photo=img, caption="Here's your image!")

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(set_commands).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", send_image))
    app.run_polling()

if __name__ == "__main__":
    main()
